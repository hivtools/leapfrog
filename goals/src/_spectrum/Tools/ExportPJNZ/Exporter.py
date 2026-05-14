import csv

from zipfile import ZipFile, ZIP_DEFLATED

from uuid import uuid4
from io import BytesIO, StringIO
from collections import namedtuple
import ast

from Tools.ExportPJNZ.DP.ExportDP import *
from Tools.ExportPJNZ.ExportPJN import *

from SpectrumCommon.Util.AM.AMUncertaintyAnalysisRW import writeDPUAFile, writeDPUADFile, writeDPUAD_AUAFile

from AvenirCommon.Database import *
from SpectrumCommon.Const.GB import *
from SpectrumCommon.Const.DP import *
from SpectrumCommon.Const.PJ import *

import requests
import json

def downloadPJNZ(pjn, modvars, epp_files, shiny90=None):
    projectionName = pjn[PJN_TitleTag]
    countryISO = pjn[PJN_ISO3NumericTag]
    country = pjn[PJN_ISO3AlphaTag]
    firstYear = pjn[PJN_FirstYearTag]
    finalYear = pjn[PJN_FinalYearTag]

    params = createProjectionParams(fileName=projectionName, country=country, countryISO=countryISO, firstYear=firstYear, finalYear=finalYear)

    pjnList = writePJN(params)
    dpList = writeDP(params, modvars)

    def list_to_csv(data_2d):
        # Find the maximum row length
        max_cols = max(len(row) for row in data_2d)
        # Pad each row to max_cols with empty strings
        padded_data = [row + [''] * (max_cols - len(row)) for row in data_2d]
        output = StringIO()
        writer = csv.writer(output)
        writer.writerows(padded_data)
        output.seek(0)
        return output

    pjnBuffer = list_to_csv(pjnList)
    dpBuffer = list_to_csv(dpList)

    outBuffer = BytesIO()

    with ZipFile(outBuffer, 'a', ZIP_DEFLATED) as zipObjWrite:
        zipObjWrite.writestr(str(params.fileName) + '.PJN', pjnBuffer.getvalue())
        zipObjWrite.writestr(str(params.fileName) + '.DP', dpBuffer.getvalue())

        if (GB_UA in modvars[PJN_ModulesTag]):
            DPUABuffer = list_to_csv(writeDPUAFile(modvars))
            zipObjWrite.writestr('DPUA/' + str(params.fileName) + '.DPUA', DPUABuffer.getvalue(), compress_type=ZIP_DEFLATED)
            DPUADBuffer = list_to_csv(writeDPUADFile(params, modvars))
            zipObjWrite.writestr('DPUA/' + str(params.fileName) + '.DPUAD', DPUADBuffer.getvalue(), compress_type=ZIP_DEFLATED)
            DPUAD_AUABuffer = list_to_csv(writeDPUAD_AUAFile(params, modvars))
            zipObjWrite.writestr('DPUA/' + str(params.fileName) + '.DPUAD_AUA', DPUAD_AUABuffer.getvalue(), compress_type=ZIP_DEFLATED)

        if len(epp_files) > 0:
            original_name = ""
            for filename, data in epp_files.items():
                if (filename.endswith('.SPT') or 
                    filename.endswith('.SPU') or
                    filename.endswith('.TYP') or
                    filename.endswith('.ep1') or
                    filename.endswith('.ep3') or
                    filename.endswith('.ep4') or
                    filename.endswith('.ep5') or
                    filename.endswith('.xml') ):
                    original_name = filename[4:-4]
                    break
				
            for filename, data in epp_files.items():
                new_filename = filename.replace(original_name, str(params.fileName))
                zipObjWrite.writestr(new_filename, data)

        if shiny90 is not None:
            zipObjWrite.writestr(shiny90["name"], shiny90["file"])
        zipObjWrite.close()

    outBuffer.seek(0)
    return outBuffer


# spectrumWebURL = 'http://localhost'    #'https://api2.spectrumweb.org'
# url = spectrumWebURL + "/JSON/"
url = 'https://api1.delphi.spectrumweb.org/'

def getPJNZProjection(countryISO, firstYear, finalYear, projName):

    link_token = container_login()

    loginResponse = doServiceCall(
		link_token,
		'{'
            + '"username" : "guest", '
            + '"password" : 123456, '
            + '"appID" : "AIM"'
        + '}',
        "GBLoginService.Login"
	)
    # loginData = {
    #     "id": "{12345678-0000-0000-0000-000000000000}",
    #     "method": "GBLoginService.Login",
    #     "params": {
    #         "jsonMesg": '{"username" : "guest", '
    #         + '"password" : 123456, '
    #         + '"appID" : "AIM"}'
    #     },
    # }

    # loginResponse = requests.post(url, json=loginData)
    createProjResponse = doServiceGetCall(
		link_token,
        '{"countryISO": '
        + str(countryISO)
        + ', '
        + '"firstYear" : '
        + str(firstYear)
        + ', '
        + '"finalYear" : '
        + str(finalYear)
        + ', '
        + '"modList"   : [1, 4], '
        + '"fileName"  : '
        + '"'
        + str(projName)
        + '" }',
		"GBSpectrumService.CreateProjection"
	)
    # createProjData = {
    #     "id": "{12345678-0000-0000-0000-000000000000}",
    #     "method": "GBSpectrumService.CreateProjection",
    #     "params": {
    #         "jsonMesg": '{"countryISO": '
    #         + str(countryISO)
    #         + ", "
    #         + '"firstYear" : '
    #         + str(firstYear)
    #         + ", "
    #         + '"finalYear" : '
    #         + str(finalYear)
    #         + ", "
    #         + '"modList"   : [1, 4], '
    #         + '"fileName"  : '
    #         + '"'
    #         + str(projName)
    #         + '" }'
    #     },
    # }

    # createProjResponse = requests.post(url, json=createProjData)

    saveProjResponse = doServiceGetCall(
		link_token,
        '{"proj" : 1,' + '"fileTitle" :' + '"' + str(projName) + '" }',
		"GBSpectrumService.SaveProjection"
	)
    # saveProjData = {
    #     "id": "{12345678-0000-0000-0000-000000000000}",
    #     "method": "GBSpectrumService.SaveProjection",
    #     "params": {
    #         "jsonMesg": '{"proj" : 1,' + '"fileTitle" :' + '"' + str(projName) + '" }'
    #     },
    # }

    # saveProjResponse = requests.post(url, json=saveProjData)


    downloadProjResponse = doServiceGetCall(
		link_token,
        '{"fileTitle" :' + '"' + str(projName) + '" }',
		"GBSpectrumService.DownloadProjection"
	)
    # downloadProjData = {
    #     "id": "{12345678-0000-0000-0000-000000000000}",
    #     "method": "GBSpectrumService.DownloadProjection",
    #     "params": {"jsonMesg": '{"fileTitle" :' + '"' + str(projName) + '" }'},
    # }

    # downloadProjResponse = requests.post(url, json=downloadProjData)

    path = json.loads(json.loads(downloadProjResponse.text)["result"]["Result"])[
        "result"
    ]

    file = requests.get(url + "/" + path)

    buffer = BytesIO(file.content)

    return buffer

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#                                                                                                                                                                      #
#                                                                             Login                                                                                    #
#                                                                                                                                                                      #
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

def login():
	password = 'Exporter'+uuid4().hex

	payload = {'password': password}
	headers = {'content-type': 'application/json'}
	url_service = url+'/api/v1/session/guest?password='+password

	response = requests.post(url_service, data=payload, headers=headers)

	if response.status_code == 200:
		token = response.json()['token']

		# print(['token ', token])
		return response.status_code, token
	else:
		print('Failed to log in')

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#                                                                                                                                                                      #
#                                                                         Get Link Token                                                                               #
#                                                                                                                                                                      #
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

def get_link_token(token, max_call=10):
	headers = {'content-type': 'application/json', 'SpecW-Auth': 'token ' + token}
	url_service = url+'/api/v1/server/'+token

	response = requests.post(url_service, headers=headers)

	if (response.status_code==200) and (max_call>0):
		# print(response.json())
		if response.json()['ready']:
			link_token = response.json()['linkToken']
			return response.status_code, link_token
		else:
			get_link_token(token, max_call-1)
	else:
		print('Failed to retrieve link token')
		return response.status_code, None

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#                                                                                                                                                                      #
#                                                                        Container Login                                                                               #
#                                                                                                                                                                      #
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#

def container_login():
	(status, token) = login()
	if status==200:
		(status, link_token) = get_link_token(token)
	return link_token

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#                                                                                                                                                                      #
#                                                                      Get Intervention List                                                                           #
#                                                                                                                                                                      #
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------#
def doServiceGetCall(link_token, msg, method):
	# json_msg = json.dumps(msg)

	headers = {'content-type': 'application/json'}
	payload = {
	    "id": "{12345678-0000-0000-0000-000000000000}",
		"method":method,
		"params":{"jsonMesg": msg}
	}

	payloadJO = json.dumps(payload)

	return requests.get(url+'/r/'+link_token+'/JSON', data=payloadJO, headers=headers)#, params=payload, headers=headers)


def doServiceCall(link_token, msg, method):
	# json_msg = json.dumps(msg)

	headers = {'content-type': 'application/json'}
	payload = {
	    "id": "{12345678-0000-0000-0000-000000000000}",
		"method":method,
		"params":{"jsonMesg": msg}
	}

	payloadJO = json.dumps(payload)

	return requests.post(url+'/r/'+link_token+'/JSON', data=payloadJO, headers=headers)#, params=payload, headers=headers)

def ParseJSONIntoObj(input, ClassName):
	data = json.loads(input, object_hook=lambda d: namedtuple(ClassName, d.keys())(*d.values())).result

	if len(data) == 1:
		data = data[0]

	return data

def getResponseResult(response):
	decodedString = response.content.decode("UTF-8")
	return ast.literal_eval(decodedString)['result']['Result']

def spectrum_getIntervList():
	response = doServiceCall(container_login(), {}, "RESTService.GetIntervList")

	if response.status_code == 200:
		data = ParseJSONIntoObj(getResponseResult(response), 'CS_TIVObj')
		return response.status_code, data
	else:
		print('Failed to get intervention list')
		print(response)

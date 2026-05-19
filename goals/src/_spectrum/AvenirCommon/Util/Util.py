import math
from os import path
from inspect import getframeinfo
import re
from uuid import uuid4

# from Logger import log
import logging


GB_Nan = "NAN"
GB_FloatDiff = 0.00001
GB_NOT_FOUND = -1


def getYear(t, firstYear):
    return t + firstYear


def GBRange(first, last, step=1):
    return range(first, last + 1, step)


def GBDownRange(first, last, step=-1):
    return range(first, last - 1, step)


def GBGetKeyValue(d, key, default):
    if key in d:
        return d[key]
    else:
        return default


def formatCountryFName(ISO3A, version, subnatCode=0):
    if subnatCode in [0, 1]:  # [GB_EntireCountry, GB_CustomSubnatRegion]
        fName = ISO3A + "_" + version + ".JSON"
    else:
        fName = ISO3A + "_" + str(subnatCode) + "_" + version + ".JSON"
    return fName


def getTagRow(sheet, tag, tagCol=0):
    tagRow = GB_Nan
    for row in range(0, len(sheet)):
        if str(sheet[row][tagCol]).lower() == tag.lower():
            tagRow = row
    return tagRow


def getAllTags(sheet, tagCol=0):
    tags = {}
    for row in range(0, len(sheet)):
        tag = str(sheet[row][tagCol])
        if (len(tag) > 0) and (tag[0] == "<"):
            tags[tag] = row
    return tags


def getYearIndexFromT(dataFirstYear, dataFinalYear, year):
    result = year - dataFirstYear  # //raw index, no filtering
    result = max(result, 0)  # //account for negative indices
    result = min(
        result, dataFinalYear - dataFirstYear
    )  # //account for positive indices that exceed
    return result


def getDataYear(dataFirstYear, dataFinalYear, year):
    result = max(dataFirstYear, year)  # //account for negative indices
    result = min(dataFinalYear, result)  # //account for positive indices that exceed
    return result


def GetIndexFromT(dataFirstYear, dataFinalYear, year):
    yr = getDataYear(dataFirstYear, dataFinalYear, year)
    return yr - dataFirstYear


def linearInterpolate(values):
    startVal = values[0]
    endVal = values[len(values) - 1]
    diff = endVal - startVal
    # (* current value = first value + ((final value - first value) /
    #     (final index - first index)) * (current index - first index) *)
    for i in GBRange(1, (len(values) - 2)):
        NewVal = startVal + (diff / (len(values) - 1)) * i
        values[i] = NewVal


def GBNormalize(values=list, total=100):
    #   (* Sum will hold the sum of all the values in values that we want to
    #      normalize. *)
    sum = 0.0

    #   (* Sum all values in the array. *)
    for i in GBRange(0, len(values) - 1):
        sum = sum + values[i]

    #   (* If the values sum to 0, we will multiply them all by 0. Otherwise, we
    #   will multiply them all by what we want them to sum to divided by their actual sum. *)
    if GBEqual(sum, 0.0, GB_FloatDiff):
        multiplier = 0
    else:
        multiplier = total / sum

    # (* Multiply each value by our multiplier. *)
    for i in GBRange(0, len(values) - 1):
        values[i] = values[i] * multiplier


def GBEqual(a, b, tolerance=GB_FloatDiff):
    return math.isclose(a, b, abs_tol=tolerance)


def GBClamp(value, lower, upper):
    if value < lower:
        return lower
    elif value > upper:
        return upper
    else:
        return value


def GB_traceback(exc: Exception):
    logging.debug("Exception made!")
    first_arg = exc.args[0] if len(exc.args) >= 1 else "No arg passed in exc.args"
    status = 500

    tb = exc.__traceback__
    if tb is None:
        return {
            "status": status,
            "error": first_arg,
        }

    trace = []
    while tb is not None:
        info = getframeinfo(tb.tb_frame)
        try:
            line = (
                info.code_context[0].strip()
                if info.code_context
                else "No source line available"
            )
        except Exception:
            line = "Failed to get line from frame"

        trace.append(
            {
                "file": path.basename(info.filename),
                "row": info.lineno,
                "method": info.function,
                "line": line,
            }
        )
        tb = tb.tb_next

    return {"status": status, "error": first_arg, "trace": trace}


def slugify(name, ensure_uniqueness=False):
    result = re.sub(r"(?<!^)(?=[A-Z])", "-", name).lower()
    result = re.sub(r"[^a-z0-9]", "-", result)
    result = re.sub(r"-+", "-", result)
    result = result.strip("-")

    if ensure_uniqueness:
        result = result + "-" + str(uuid4()).replace("-", "")

    return result

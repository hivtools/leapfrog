import numpy as np


def findTagRow(sheet, tag: str = "", column: int = 0) -> int:
    if type(sheet) is list:
        for row in range(len(sheet)):
            if len(sheet[row]) <= column:
                continue
            if sheet[row][column] == tag:
                return row
        raise Exception("Tag " + tag + " not found")
    else:
        whereArr = np.where(sheet[:, column] == tag)
        row = int(whereArr[0][0]) if (len(whereArr[0]) > 0) else -1
        if row < 0:
            raise Exception("Tag " + tag + " not found")
        return row


def findTagCol(sheet, tag=str, row=0):
    whereArr = np.where(sheet[row, :] == tag)
    row = int(whereArr[0][0]) if (len(whereArr[0]) > 0) else -1
    if row < 0:
        raise Exception("Tag " + tag + " not found")
    return row

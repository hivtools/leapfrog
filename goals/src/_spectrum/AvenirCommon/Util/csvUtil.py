import io
import csv
import numpy as np


def gb_read_csv_sheet(file_obj):
    if isinstance(file_obj, io.TextIOBase):
        rows = list(csv.reader(file_obj))
    else:
        text_stream = io.TextIOWrapper(file_obj, encoding="utf-8", newline="")
        rows = list(csv.reader(text_stream))

    max_cols = max((len(row) for row in rows), default=0)
    normalized_rows = [row + [""] * (max_cols - len(row)) for row in rows]
    return np.array(normalized_rows, dtype=object)

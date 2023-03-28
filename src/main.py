from json import dump

import numpy as np
import numpy.typing as npt
from config import *
from scipy.signal import resample
from wfdb import Record
from wfdb.io import dl_database
from wfdb.io import rdheader
from wfdb.io import rdrecord


def get_record() -> Record:
    """Get the record."""

    # Download the database if it doesn't exist.
    dl_database(db_dir, dl_dir, records=[record_name])

    # Read the header and get the sampling frequency.
    header = rdheader(record_path)
    fs = header.fs

    # Read and return the record.
    # We only need the first 10 minutes and the first two channels (I, II).
    return rdrecord(record_path, sampto=fs * output_len_s, channels=[0, 1])


def record_to_array(record: Record) -> npt.NDArray[np.float64]:
    return resample(record.p_signal, output_len_s * output_fs)


def array_to_obj(array: npt.NDArray[np.float64]) -> list[dict[str, float | int]]:
    return [
        {
            "millisecondsSinceStart": i * 1000 // output_fs,
            "leadI": leads[0],
            "leadII": leads[1],
        }
        for i, leads in enumerate(array)
    ]


def main():
    record = get_record()
    array = record_to_array(record)
    obj = array_to_obj(array)

    with open("../assets/data.json", "w") as f:
        dump(obj, f, indent=2)


if __name__ == "__main__":
    main()

import numpy as np
import numpy.typing as npt
from scipy.signal import resample
from wfdb import Record
from wfdb.io import dl_database, rdheader, rdrecord

from config import *


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


def main():
    record = get_record()
    array = record_to_array(record)

    # False positives: https://youtrack.jetbrains.com/issue/PY-34337/numpy.savetxt-has-incorrect-type-hints
    # noinspection PyTypeChecker
    np.savetxt("../assets/lead I.txt", array[:, 0], "%.15f")
    # noinspection PyTypeChecker
    np.savetxt("../assets/lead II.txt", array[:, 1], "%.15f")


if __name__ == "__main__":
    main()

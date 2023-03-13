from wfdb import Record
from wfdb.io import dl_database, rdheader, rdrecord
import numpy as np
import numpy.typing as npt
from scipy.signal import resample

db_dir = "cebsdb"
dl_dir = "../downloads/"
record_name = "m001"
record_path = dl_dir + record_name
output_len_min = 10
output_len_s = output_len_min * 60
output_fs = 125


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
    np.savetxt("../assets/lead I.txt", array[:, 0])
    # noinspection PyTypeChecker
    np.savetxt("../assets/lead II.txt", array[:, 1])


if __name__ == "__main__":
    main()

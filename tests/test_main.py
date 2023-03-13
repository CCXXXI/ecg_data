import numpy as np
from main import get_record
from main import output_fs
from main import output_len_s
from main import record_to_array
from pytest import fixture


@fixture
def record():
    return get_record()


@fixture
def array(record):
    return record_to_array(record)


@fixture
def saved_array():
    return np.column_stack((
        np.loadtxt("../assets/lead I.txt"),
        np.loadtxt("../assets/lead II.txt"),
    ))


def test_get_record(record):
    assert record.fs >= output_fs
    assert record.sig_len // record.fs >= output_len_s
    assert record.sig_name == ["I", "II"]


def test_record_to_array(array):
    assert array.shape == (output_len_s * output_fs, 2)


def test_saved_array(saved_array, array):
    assert np.allclose(saved_array, array)

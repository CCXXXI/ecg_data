from json import load
from math import isclose

from pytest import fixture

from main import get_record, array_to_obj
from main import output_fs
from main import output_len_s
from main import record_to_array


@fixture
def record():
    return get_record()


@fixture
def array(record):
    return record_to_array(record)


@fixture
def obj(array):
    return array_to_obj(array)


@fixture
def saved_obj():
    with open("../assets/data.json") as f:
        return load(f)


def test_get_record(record):
    assert record.fs >= output_fs
    assert record.sig_len // record.fs >= output_len_s
    assert record.sig_name == ["I", "II"]


def test_record_to_array(array):
    assert array.shape == (output_len_s * output_fs, 2)


def test_saved_obj(saved_obj, obj):
    for saved_point, point in zip(saved_obj, obj):
        assert saved_point["millisecondsSinceStart"] == point["millisecondsSinceStart"]
        assert isclose(saved_point["leadI"], point["leadI"])
        assert isclose(saved_point["leadII"], point["leadII"])

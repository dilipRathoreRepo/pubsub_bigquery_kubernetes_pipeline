import pytest
import pubsub-pipe-image.utils as utils


@pytest.fixture
def lst():
    lst = [["a", ["x", "y", ["z1", "z2"]], "c"], ["e", "f"], [1, 2, 3]]
    return lst

def test_flatten(lst):
    val = utils.flatten(lst)
    list1 = []
    for e in val:
        list1.append(e)

    assert ['a', 'x', 'y', 'z1', 'z2', 'c', 'e', 'f', 1, 2, 3] == list1

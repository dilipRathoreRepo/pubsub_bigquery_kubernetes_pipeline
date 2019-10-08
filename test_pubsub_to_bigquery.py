import pytest
from pubsub-pipe-image.pubsub-to-bigquery import fqrn


@pytest.fixture
def lst():
    lst = ['subscriptions', 'rising-minutia-254502', 'mypubsub']
    return lst


def test_fqrn(lst):
    resource_type, project, topic_name = [lst[i] for i in range(0,len(lst))]
    returned_value = fqrn(resource_type, project, topic_name)
    assert "projects/{}/{}/{}".format(project, resource_type, topic_name) == returned_value

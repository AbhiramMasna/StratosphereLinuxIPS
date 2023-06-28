"""Unit test for modules/update_manager/update_manager.py"""
from tests.module_factory import ModuleFactory
import json

def test_getting_header_fields(mocker, mock_db):
    update_manager = ModuleFactory().create_update_manager_obj(mock_db)
    url = 'google.com/play'
    mock_requests = mocker.patch("requests.get")
    mock_requests.return_value.status_code = 200
    mock_requests.return_value.headers = {'ETag': '1234'}
    mock_requests.return_value.text = ""
    response = update_manager.download_file(url)
    assert update_manager.get_e_tag(response) == '1234'


def test_check_if_update_based_on_update_period(mock_db):
    mock_db.get_TI_file_info.return_value = {'time': float('inf')}
    update_manager = ModuleFactory().create_update_manager_obj(mock_db)
    url = 'abc.com/x'
    # update period hasn't passed
    assert update_manager.check_if_update(url, float('inf')) is False

def test_check_if_update_based_on_e_tag(mocker, mock_db):
    update_manager = ModuleFactory().create_update_manager_obj(mock_db)

    # period passed, etag same
    etag = '1234'
    url = 'google.com/images'
    mock_db.get_TI_file_info.return_value =  {'e-tag': etag}

    mock_requests = mocker.patch("requests.get")
    mock_requests.return_value.status_code = 200
    mock_requests.return_value.headers = {'ETag': '1234'}
    mock_requests.return_value.text = ""
    assert update_manager.check_if_update(url, float('-inf')) is False


    # period passed, etag different
    etag = '1111'
    url = 'google.com/images'
    mock_db.get_TI_file_info.return_value =  {'e-tag': etag}
    mock_requests = mocker.patch("requests.get")
    mock_requests.return_value.status_code = 200
    mock_requests.return_value.headers = {'ETag': '2222'}
    mock_requests.return_value.text = ""
    assert update_manager.check_if_update(url, float('-inf')) is True

def test_check_if_update_based_on_last_modified(database, mocker, mock_db):
    update_manager = ModuleFactory().create_update_manager_obj(mock_db)

    # period passed, no etag, last modified the same
    url = 'google.com/photos'

    mock_db.get_TI_file_info.return_value = {'Last-Modified': 10.0}
    mock_requests = mocker.patch("requests.get")
    mock_requests.return_value.status_code = 200
    mock_requests.return_value.headers = {'Last-Modified': 10.0}
    mock_requests.return_value.text = ""

    assert update_manager.check_if_update(url, float('-inf')) is False

    # period passed, no etag, last modified changed
    url = 'google.com/photos'

    mock_db.get_TI_file_info.return_value = {'Last-Modified': 10}
    mock_requests = mocker.patch("requests.get")
    mock_requests.return_value.status_code = 200
    mock_requests.return_value.headers = {'Last-Modified': 11}
    mock_requests.return_value.text = ""

    assert update_manager.check_if_update(url, float('-inf')) is True


def test_read_ports_info():
    db = ModuleFactory().create_db_manager_obj(1234)
    update_manager = ModuleFactory().create_update_manager_obj(db)
    filepath = 'slips_files/ports_info/ports_used_by_specific_orgs.csv'
    assert update_manager.read_ports_info(filepath) > 100

    org = update_manager.db.get_organization_of_port('5243/udp')
    assert org

    org = json.loads(org)
    assert 'org_name' in org
    assert 'Viber' in org['org_name']


    org = update_manager.db.get_organization_of_port('65432/tcp')
    assert org

    org = json.loads(org)
    assert 'org_name' in org
    assert 'Apple' in org['org_name']

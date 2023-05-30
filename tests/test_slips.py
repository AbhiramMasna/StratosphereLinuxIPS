"""Unit test for ../slips.py"""
from ..slips import *
from ..redis_manager import RedisManager
from ..process_manager import ProcessManager
import os
import argparse
import subprocess
import time
import pytest

IS_IN_A_DOCKER_CONTAINER = os.environ.get('IS_IN_A_DOCKER_CONTAINER', False)


def do_nothing(*args):
    """Used to override the print function because using the self.print causes broken pipes"""
    pass


# Main Class tests
def create_Main_instance():
    """returns an instance of Main() class in slips.py"""
    main = Main(testing=True)
    main.input_information = 'test.pcap'
    main.input_type = 'pcap'
    main.line_type = False
    return main

def create_redis_manager_instance(main):
    return RedisManager(main)
def create_process_manager_instance():
    return ProcessManager(create_Main_instance())

def test_load_modules():
    proc_manager = create_process_manager_instance()
    failed_to_load_modules = proc_manager.get_modules(
        ['template', 'mldetection-1', 'ensembling']
    )[1]
    assert failed_to_load_modules == 0
#
# @pytest.mark.skipif(IS_IN_A_DOCKER_CONTAINER, reason='This functionality is not supported in docker')
# def test_save():
#     """ tests saving the database"""
#     # this test needs sudo
#     command = f'sudo ./slips.py -l -f dataset/test9-mixed-zeek-dir -s > /dev/null 2>&1'
#     # this function returns when slips is done
#     os.system(command)
#     assert os.path.exists('redis_backups/test9-mixed-zeek-dir.rdb')
#     os.remove('redis_backups/test9-mixed-zeek-dir.rdb')
#
# @pytest.mark.skipif(IS_IN_A_DOCKER_CONTAINER, reason='This functionality is not supported in docker')
# def test_load(database):
#     """ tests loading the database"""
#     # make sure the db exists
#     if not os.path.exists('redis_backups/test9-mixed-zeek-dir.rdb'):
#         # save it if it doesn't exist
#         command = f'sudo ./slips.py -l -f dataset/test9-mixed-zeek-dir -s > /dev/null 2>&1'
#         os.system(command)
#
#     # this test needs sudo
#     command = f'sudo ./slips.py -d redis_backups/test9-mixed-zeek-dir.rdb  > /dev/null 2>&1'
#     # this function returns when slips is done
#     os.system(command)
#     # wait for the command to finish
#     time.sleep(3)
#     # check a random value to make sure the db is loaded
#     x = database.r.hgetall('profile_10.0.2.2_timewindow1_flows')
#     assert 'CDm47v3jrYL8lx0cOh' in str(x)

def test_clear_redis_cache_database():
    main = create_Main_instance()
    redis_manager = create_redis_manager_instance(main)
    assert redis_manager.clear_redis_cache_database() == True



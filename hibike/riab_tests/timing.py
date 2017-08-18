"""
Timing tests for Hibike.
"""
import multiprocessing
import os
import sys
import time
import unittest

import hibike_message
add_runtime_to_path()
# pylint: disable=import-error
import runtime
import runtimeUtil
from runtimeUtil import HIBIKE_COMMANDS
import studentAPI


def add_runtime_to_path():
    """
    Modify paths so that we can import
    stuff from runtime.
    """
    path = os.path.dirname(os.path.abspath(__file__))
    parent_path = path.rstrip("hibike/riab_tests")
    runtime = os.path.join(parent_path, "runtime")
    sys.path.insert(1, runtime)


class FakeRobot(object):
    WAIT_GRANULARITY_SECS = 0.001
    WAIT_TIME_SECS = 1
    def __init__(self, pipe_to_sm, pipe_from_sm):
        """
        Params:
            PIPE_TO_SM -- a pipe to StateManager.
            PIPE_FROM_SM -- a pipe from StateManager.
        """
        self.from_manager = pipe_from_sm
        self.to_manager = pipe_to_sm

    def time_read_roundtrip(self, uid):
        device_id = hibike_message.uid_to_device_id(uid)
        device_params = hibike_message.all_params_for_device_id(device_id)
        self.to_manager.put([HIBIKE_COMMANDS.SUBSCRIBE, [uid, 1, []])
        start_time = time.time()
        self.to_manager.put([HIBIKE_COMMANDS.READ, device_params])


class EndToEndLatencyTests(unittest.TestCase):
    """
    Test latency roundtrip from student code
    to Hibike.
    """
    ROUND_TRIP_GOAL_MS = 1000

    @classmethod
    def setUpClass(cls):
        # pylint: disable=import-error
    def test_end_to_end_latency(self):
        import runtime
        import studentAPI

        bad_things_queue = multiprocessing.Queue()
        state_queue = multiprocessing.Queue()
        spawn_process = runtime.process_factory(bad_things_queue, state_queue)


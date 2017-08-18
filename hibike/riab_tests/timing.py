"""
Timing tests for Hibike.
"""
import multiprocessing
import os
import sys
import time
import unittest

import hibike_message

def add_runtime_to_path():
    """
    Modify paths so that we can import
    stuff from runtime.
    """
    path = os.path.dirname(os.path.abspath(__file__))
    parent_path = path.rstrip("hibike/riab_tests")
    runtime = os.path.join(parent_path, "runtime")
    sys.path.insert(1, runtime)


add_runtime_to_path()
# pylint: disable=import-error
import runtime
import runtimeUtil
from runtimeUtil import HIBIKE_COMMANDS
import studentAPI


class FakeRuntime:
    """
    A fake version of Runtime.
    """
    __slots__ = ["bad_things_queue", "state_queue"]
    def __init__(self):
        self.bad_things_queue = multiprocessing.Queue()
        self.state_queue = multiprocessing.Queue()

    def run(self):
        """
        Start StateManager and Hibike.
        """
        spawn_process = runtime.process_factory(self.bad_things_queue, self.state_queue)
        try:
            spawn_process(runtimeUtil.PROCESS_NAMES.STATE_MANAGER, runtime.start_state_manager)
            spawn_process(runtimeUtil.PROCESS_NAMES.HIBIKE, runtime.start_hibike)
        # pylint: disable=broad-except
        except Exception as ex:
            print("Encountered exception while spawning process {}".format(ex))

    def run_for(self, secs):
        """
        Execute for SECS seconds, and then terminate.
        """
        self.run()
        curr_time = time.time()
        while time.time() - curr_time < secs:
            pass
        self.terminate_all()

    def terminate_all(self):
        """
        Terminate all processes and shut down.
        """
        runtime.terminate_process(runtimeUtil.PROCESS_NAMES.STATE_MANAGER)
        runtime.terminate_process(runtimeUtil.PROCESS_NAMES.HIBIKE)


def profile_end_to_end():
    """
    Execute fake runtime for about 30 seconds and then quit,
    checking how much time was spent.
    """
    import cProfile
    fake_rt = FakeRuntime()
    cProfile.runctx("fake_rt.run_for(60)", locals={"fake_rt": fake_rt}, globals={})


class FakeRobot(object):
    """
    A fake robot.
    """
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
        device_params = hibike_message.all_paams_for_device_id(device_id)
        self.to_manager.put([HIBIKE_COMMANDS.SUBSCRIBE, [uid, 1, []]])
        start_time = time.time()
        self.to_manager.put([HIBIKE_COMMANDS.READ, device_params])


class EndToEndLatencyTests(unittest.TestCase):
    """
    Test latency roundtrip from student code
    to Hibike.
    """
    ROUND_TRIP_GOAL_MS = 1000
    def test_end_to_end_latency(self):
        fake_rt = FakeRuntime()
        fake_rt.run()
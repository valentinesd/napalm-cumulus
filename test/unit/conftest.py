"""Test fixtures."""
from builtins import super

import pytest
import json
from napalm.base.test import conftest as parent_conftest

from napalm.base.test.double import BaseTestDouble

from napalm_cumulus import cumulus


@pytest.fixture(scope="class")
def set_device_parameters(request):
    """Set up the class."""

    def fin():
        request.cls.device.close()

    request.addfinalizer(fin)

    request.cls.driver = cumulus.CumulusDriver
    request.cls.patched_driver = PatchedCumulusDriver
    request.cls.vendor = "cumulus"
    parent_conftest.set_device_parameters(request)


def pytest_generate_tests(metafunc):
    """Generate test cases dynamically."""
    parent_conftest.pytest_generate_tests(metafunc, __file__)


class PatchedCumulusDriver(cumulus.CumulusDriver):
    """Patched Cumulus Driver."""

    def __init__(self, hostname, username, password, timeout=60, optional_args=None):
        """Patched Cumulus Driver constructor."""
        super().__init__(hostname, username, password, timeout, optional_args)

        self.patched_attrs = ["device"]
        self.device = FakeCumulusDevice()

    def disconnect(self):
        pass

    def is_alive(self):
        return {"is_alive": True}  # In testing everything works..

    def open(self):
        pass


class FakeCumulusDevice(BaseTestDouble):
    """Cumulus device test double."""

    # The following three functions are not needed for testing, but are still called
    # so override them so tests pass
    def disconnect(self):
        pass

    def enable(self):
        pass

    def exit_enable_mode(self):
        pass

    def send_command(self, command):
        """Fake send_command."""
        filename = "{}.json".format(self.sanitize_text(command))
        full_path = self.find_file(filename)

        if "json" in command:
            result = json.dumps(self.read_json_file(full_path))
        else:
            result = self.read_txt_file(full_path)
        return result

    def send_command_timing(self, command):
        """Fake send_command."""
        filename = "{}.json".format(self.sanitize_text(command))
        full_path = self.find_file(filename)

        if "json" in command:
            result = json.dumps(self.read_json_file(full_path))
        else:
            result = self.read_txt_file(full_path)
        return result

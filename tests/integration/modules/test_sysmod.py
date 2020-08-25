import pytest
import salt.utils.platform
from tests.support.case import ModuleCase
from tests.support.helpers import slowTest


@pytest.mark.windows_whitelisted
class SysModuleTest(ModuleCase):
    """
    Validate the sys module
    """

    @slowTest
    def test_valid_docs(self):
        """
        Make sure no functions are exposed that don't have valid docstrings
        """
        timeout = 300
        if salt.utils.platform.is_windows():
            timeout = 600
        ret = self.run_function("runtests_helpers.get_invalid_docs", timeout=timeout)
        if ret == {"missing_docstring": [], "missing_cli_example": []}:
            return

        if isinstance(ret, str):
            self.fail(ret)

        self.fail(
            "There are some functions which do not have a docstring or do not "
            "have an example:\nNo docstring:\n{}\nNo example:\n{}\n".format(
                "\n".join(["  - {}".format(f) for f in ret["missing_docstring"]]),
                "\n".join(["  - {}".format(f) for f in ret["missing_cli_example"]]),
            )
        )

from assertion import Assertion
from unittest import TestCase


class MarvinTestCase(TestCase):

    def __init__(self, *args, **kwargs):  # pragma: no cover
        super(MarvinTestCase, self).__init__(*args, **kwargs)

    def runTest(self):  # just to tests
        pass

    def assertThat(self, assertion):
        if isinstance(assertion, Assertion):
            if not assertion.assertion_value:
                raise AssertionError()  # enhance the message by type of inference expected
        else:
            raise RuntimeError("The assertThat method expects an Assertion instance")

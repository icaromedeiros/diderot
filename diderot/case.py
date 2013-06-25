from assertion import Assertion
from unittest import TestCase


class DiderotTestCase(TestCase):

    def __init__(self, *args, **kwargs):  # pragma: no cover
        super(DiderotTestCase, self).__init__(*args, **kwargs)

    def assertThat(self, assertion):
        if isinstance(assertion, Assertion):
            if not assertion.assertion_value:
                raise AssertionError()  # enhance the message by type of inference expected
        else:
            raise RuntimeError("The assertThat method expects an Assertion instance")

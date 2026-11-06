import math
import sys
from unittest import TestCase

from jinja2 import Environment
from parameterized import parameterized_class


@parameterized_class(
    ("command", "expected"),
    [
        ("'Hello World'", "Hello World"),
        ("1+1", "2"),
        ("max(1, 2)", "2"),
        ("exec('import math') or math.pi", str(math.pi)),
        ("exec('import sys') or sys.argv[-1]", sys.argv[-1]),
    ],
)
class TestMain(TestCase):
    # https://jinja.palletsprojects.com/en/3.0.x/templates/
    environment: Environment
    command: str
    expected: str

    def setUp(self):
        self.environment = Environment(  # noqa: S701
            extensions=["jinja2_eval.EvalExtension"]
        )

    def test_statement(self):
        template = self.environment.from_string("{% eval " + f'"{self.command}"' + " %}")
        assert template.render() == self.expected

    def test_expression(self):
        template = self.environment.from_string("{{ " + f'"{self.command}"' + " | eval }}")
        assert template.render() == self.expected

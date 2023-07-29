from __future__ import annotations

from typing import Any, Mapping

from jinja2 import Environment, nodes
from jinja2.ext import Extension
from jinja2.parser import Parser


class EvalExtension(Extension):
    """Jinja2 extension to evaluate expressions and statements."""

    tags = {"eval"}
    """A set of names that trigger the extension."""

    def __init__(self, environment: Environment) -> None:
        super().__init__(environment)
        environment.filters["eval"] = eval  # nosec

    def parse(self, parser: Parser) -> nodes.Output:
        lineno = next(parser.stream).lineno

        __source = parser.parse_expression()

        if parser.stream.skip_if("comma"):
            __globals = parser.parse_expression()
        else:
            __globals = nodes.Const(None)

        if parser.stream.skip_if("comma"):
            __locals = parser.parse_expression()
        else:
            __locals = nodes.Const(None)

        return nodes.Output(
            [self.call_method("_eval", [__source, __globals, __locals])], lineno=lineno
        )

    def _eval(
        self,
        __source: str,
        __globals: dict[str, Any] | None = None,
        __locals: Mapping[str, object] | None = None,
    ) -> str:
        return eval(__source, __globals, __locals)  # nosec

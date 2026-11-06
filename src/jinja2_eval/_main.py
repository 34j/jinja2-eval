from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any

from jinja2 import Environment, nodes
from jinja2.ext import Extension

if TYPE_CHECKING:
    from jinja2.parser import Parser


class EvalExtension(Extension):
    """Jinja2 extension to evaluate expressions and statements."""

    tags: set[str] = {"eval"}  # noqa: RUF012
    """A set of names that trigger the extension."""

    def __init__(self, environment: Environment) -> None:
        super().__init__(environment)
        environment.filters["eval"] = eval  # noqa: S307

    def parse(self, parser: Parser) -> nodes.Output:
        lineno = next(parser.stream).lineno

        source = parser.parse_expression()

        if parser.stream.skip_if("comma"):
            globals_ = parser.parse_expression()
        else:
            globals_ = nodes.Const(None)

        locals_ = parser.parse_expression() if parser.stream.skip_if("comma") else nodes.Const(None)

        return nodes.Output([self.call_method("_eval", [source, globals_, locals_])], lineno=lineno)

    def _eval(  # noqa: PLR6301
        self,
        source: str,
        globals_: dict[str, Any] | None = None,
        locals_: Mapping[str, object] | None = None,
    ) -> str:
        return eval(source, globals_, locals_)  # noqa: S307

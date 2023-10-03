from collections.abc import Callable, Iterator
from typing import Any, BinaryIO, NamedTuple


class Call(NamedTuple):
    name: str
    start_offset: int
    end_offset: int
    args: tuple
    result: Any


class CommandRegister:
    def __init__(self):
        self._inner = []

    def add_section(self, text: str) -> None:
        self._inner.append([text])

    def append(self, call: Call) -> None:
        self._inner[-1].append(call)

    def __iter__(self) -> Iterator[Call]:
        return iter(self._inner)


class CallTracer:
    def __init__(self, proxy_instance: BinaryIO, collector: CommandRegister):
        self._collector = collector
        self._proxy_instance = proxy_instance

    def __getattr__(self, item: str) -> Any:
        function = getattr(self._proxy_instance, item)

        def wrapper(*args: Any, **kwargs: Any) -> Callable[[Any], Any]:
            offset = self._proxy_instance.tell()
            result = function(*args, **kwargs)
            call = Call(
                function.__name__,
                offset,
                self._proxy_instance.tell(),
                args,
                result,
            )
            self._collector.append(call)
            return result

        return wrapper


def wrap_to_tracer(proxy_instance: BinaryIO) -> tuple[BinaryIO, CommandRegister]:
    register = CommandRegister()
    wrapped: BinaryIO = CallTracer(proxy_instance, register)
    return wrapped, register

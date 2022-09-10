from typing import Any, Callable, Iterator, NamedTuple, TypeVar


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


Wrapped = TypeVar("Wrapped")


class CallTracer:
    def __init__(self, proxy_instance: Wrapped, collector: CommandRegister):
        self._collector = collector
        self._proxy_instance = proxy_instance

    def __getattr__(self, item: str) -> Wrapped:
        function = getattr(self._proxy_instance, item)

        def wrapper(*args: Any, **kwargs: Any) -> Callable[[Any], Wrapped]:
            offset = self._proxy_instance.tell()
            result = function(*args, **kwargs)
            call = Call(
                function.__name__, offset, self._proxy_instance.tell(), args, result
            )
            self._collector.append(call)
            return result

        return wrapper

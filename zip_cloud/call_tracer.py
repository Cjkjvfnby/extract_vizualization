from typing import Any, NamedTuple


class Call(NamedTuple):
    name: str
    args: tuple
    result: Any


class CommandRegister:
    def __init__(self):
        self._inner = []

    def add_section(self, text):
        self._inner.append([text])

    def append(self, call: Call):
        self._inner[-1].append(call)

    def __iter__(self):
        return iter(self._inner)


class CallTracer:
    def __init__(self, proxy_instance, collector: CommandRegister):
        self._collector = collector
        self._proxy_instance = proxy_instance

    def __getattr__(self, item):
        callable = getattr(self._proxy_instance, item)

        def wrapper(*args, **kwargs):
            result = callable(*args, **kwargs)

            call = Call(callable.__name__, args, result)
            self._collector.append(call)
            return result

        return wrapper

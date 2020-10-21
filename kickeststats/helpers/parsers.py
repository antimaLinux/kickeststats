from html.parser import HTMLParser
from typing import List, Union

from ..exceptions import ParsingException
from .data import grouper


class HeaderParser(HTMLParser):
    def __init__(self, *, convert_charrefs: bool = True):
        super(HeaderParser, self).__init__(convert_charrefs=convert_charrefs)
        self._header_data: List[str] = []

    def handle_data(self, data: str) -> None:
        self._header_data.append(data)

    def out(self) -> List[str]:
        return self._header_data

    @property
    def data(self) -> List[str]:
        return self._header_data

    def error(self, message: str) -> None:
        raise ParsingException(message)


class RowParser(HTMLParser):
    def __init__(self, *, convert_charrefs: bool = True):
        super(RowParser, self).__init__(convert_charrefs=convert_charrefs)
        self._row_data: List[str] = []

    def handle_data(self, data: str) -> None:
        self._row_data.append(data)

    def out(self, header: List[str]) -> List[dict]:
        return [
            dict(zip(header, [self._str_to_num(v) for v in row]))
            for row in list(grouper(self._row_data, len(header), fillvalue=None))
        ]

    @property
    def data(self) -> List[str]:
        return self._row_data

    def _str_to_num(self, val: str) -> Union[str, float]:
        try:
            return float(val)
        except ValueError:
            return val

    def error(self, message: str) -> None:
        raise ParsingException(message)


class PaginationParser(HTMLParser):
    def __init__(self, *, convert_charrefs: bool = True):
        super(PaginationParser, self).__init__(convert_charrefs=convert_charrefs)
        self._pag_data: List[str] = []

    def handle_data(self, data: str) -> None:
        self._pag_data.append(data)

    def out(self) -> range:
        pages = [int(i) for i in self._pag_data if i.isdigit()]
        return range(pages[0], pages[-1] + 1)

    @property
    def data(self) -> List[str]:
        return self._pag_data

    def error(self, message) -> None:
        raise ParsingException(message)

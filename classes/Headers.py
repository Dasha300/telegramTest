from classes.Table import Table


class Headers(Table):
    table_name: str = 'headers'
    type: dict = {'id': 'INTEGER PRIMARY KEY',
                  'site_id': 'INTEGER',
                  'content': 'TEXT',
                  'header': 'TEXT'
                  }
    foreign_key: dict = {'column': 'site_id', 'references': 'site', 'on_delete': 'SET NULL'}

    def __init__(self, site_id: int = None, header_id=None, content: str = None,
                 header: str = None, link: str = None) -> None:
        super().__init__(header_id, link)
        self._foreign_id = site_id
        self._content = content
        self._header = header

    def set_content(self, content: str) -> None:
        self._content = content

    def return_dict(self) -> dict:
        return {'site_id': self._foreign_id,
                'content': self._content,
                'header': self._header
                }

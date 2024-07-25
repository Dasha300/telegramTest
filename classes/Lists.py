from classes.Table import Table


class Lists(Table):
    table_name: str = 'lists'
    type: dict = {'id': 'INTEGER PRIMARY KEY',
                  'site_id': 'INTEGER',
                  'content': 'TEXT',
                  'list_num': 'INTEGER'
                  }
    foreign_key: dict = {'column': 'site_id',
                         'references': 'site',
                         'on_delete': 'SET NULL'}

    def __init__(self, site_id: int = None, list_id=None, content: str = None,
                 list_num=None, link: str = None) -> None:
        super().__init__(list_id, link)
        self._foreign_id = site_id
        self._content = content
        self._list_num = list_num

    def set_content(self, content: str) -> None:
        self._content = content

    def return_dict(self) -> dict:
        return {'site_id': self._foreign_id,
                'content': self._content,
                'list_num': self._list_num
                }

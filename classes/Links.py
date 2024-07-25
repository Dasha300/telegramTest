from classes.Table import Table


class Links(Table):
    table_name: str = 'links'
    type: dict = {'id': 'INTEGER PRIMARY KEY',
                  'site_id': 'INTEGER',
                  'link': 'TEXT',
                  'title': 'TEXT'
                  }
    foreign_key: dict = {'column': 'site_id',
                         'references': 'site',
                         'on_delete': 'SET NULL'}

    def __init__(self, site_id: int = None, link: str = None, link_id=None, title: str = None) -> None:
        super().__init__(link_id, link)
        self._foreign_id = site_id
        self._title = title

    def set_link(self, link: str) -> None:
        self._link = link

    def set_title(self, title: str) -> None:
        self._title = title

    def return_dict(self) -> dict:
        return {'site_id': self._foreign_id,
                'link': self._link,
                'title': self._title}

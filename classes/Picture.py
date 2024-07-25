from classes.Table import Table


class Picture(Table):
    table_name: str = 'picture'
    type: dict = {'id': 'INTEGER PRIMARY KEY',
                  'site_id': 'INTEGER',
                  'alt': 'TEXT',
                  'src': 'TEXT',
                  }
    foreign_key = {'column': 'site_id', 'references': 'site', 'on_delete': 'SET NULL'}

    def __init__(self, site_id: int = None, link: str = None, link_id=None, alt: str = None, src: str = None) -> None:
        super().__init__(link_id, link)
        self._foreign_id = site_id
        self._alt = alt
        self._src = src

    def set_alt(self, alt: str) -> None:
        self._alt = alt

    def set_src(self, src: str) -> None:
        self._src = src

    def return_dict(self) -> dict:
        return {'site_id': self._foreign_id,
                'alt': self._alt,
                'src': self._src}

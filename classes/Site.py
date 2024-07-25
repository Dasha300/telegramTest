from classes.Table import Table


class Site(Table):
    table_name: str = 'site'
    type: dict = {'id': 'INTEGER PRIMARY KEY',
                  'link': 'TEXT UNIQUE',
                  'title': 'TEXT'}

    def __init__(self, site_id: int = None, link: str = None, title: str = None) -> None:
        super().__init__(site_id, link)
        self._title = title

    @property
    def self_id(self):
        return self._site_id

    def set_id(self, site_id) -> None:
        self._site_id = site_id

    def return_dict(self) -> dict:
        return {'link': self._link,
                'title': self._title}

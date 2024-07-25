class Table:
    table_name: str = None
    type: dict = None
    foreign_key: dict = None

    def __init__(self, site_id: int, link: str):
        self._site_id = site_id
        self._link = link

    def return_dict(self) -> dict:
        return {}

    def set_id(self, site_id) -> None:
        self._site_id = site_id

    def link(self, link) -> None:
        self._link = link

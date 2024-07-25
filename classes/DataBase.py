import sqlite3
from typing import Any
from classes.Site import Site
from classes.Lists import Lists
from classes.Picture import Picture
from classes.Paragraph import Paragraph
from classes.Links import Links
from classes.Headers import Headers
from loguru import logger

LIST_TABLES: set = {Site.table_name,
                    Lists.table_name,
                    Picture.table_name,
                    Paragraph.table_name,
                    Links.table_name,
                    Headers.table_name}
LISTS_SQL: str = """select * from lists 
left join site on lists.site_id = site.id
where INSTR(lists.content, (?)) > 0 OR 
      INSTR(lists.list_num, (?)) > 0 """
PICTURE_SQL: str = """select * from picture 
left join site on picture.site_id = site.id
where INSTR(picture.alt, (?)) > 0 OR 
      INSTR(picture.src, (?))"""
PARAGRAPH_SQL: str = """select * from paragraphs 
left join site on paragraphs.site_id = site.id
where INSTR(paragraphs.content, (?)) > 0"""
LINKS_SQL: str = """select * from links 
left join site on links.site_id = site.id
where INSTR(links.link, (?)) > 0 OR 
      INSTR(links.title, (?))"""
HEADERS_SQL: str = """select * from headers 
left join site on headers.site_id = site.id
where INSTR(headers.content, (?)) > 0"""

SQL: str = """select * from """


class DataBase:
    def __init__(self, db_name: str, ip_address: str = None, port: str = None,
                 user: str = None, password: str = None) -> None:
        self.db_name = db_name
        self.password = password
        self.user = user
        self.port = port
        self.ip_address = ip_address
        self.cursor = None
        self.conn = None

    async def open_connect(self) -> None:
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    async def create_table(self, table: Any) -> None:
        try:
            await self.open_connect()
            column_definitions = ", ".join(f"{name} {data_type}" for name, data_type in table.type.items())

            # Добавляем определение внешних ключей, если они есть
            if table.foreign_key:
                foreign_key_definitions = (
                    f"FOREIGN KEY ({table.foreign_key['column']}) "
                    f"REFERENCES {table.foreign_key['references']} (id) "
                    f"ON DELETE {table.foreign_key['on_delete']}"

                )
                column_definitions += ", " + foreign_key_definitions
            sql = f"CREATE TABLE IF NOT EXISTS {table.table_name} ({column_definitions})"
            self.cursor.execute(sql)
            self.conn.commit()
            await self.close_conn()

        except Exception as ex:
            await self.close_conn()
            logger.exception(ex)

    async def insert_value(self, table: Any) -> bool:
        try:
            await self.open_connect()
            params = tuple('?' * len(table.return_dict().keys()))
            sql = f"""INSERT INTO {table.table_name}
                      ({', '.join([str(key) for key in table.return_dict().keys()])}) 
                      VALUES ({', '.join(params)})"""
            self.cursor.execute(sql, tuple([key for key in table.return_dict().values()]))
            self.conn.commit()
            await self.close_conn()
            return True
        except Exception as ex:
            await self.close_conn()
            logger.exception(ex)
            return False

    async def select_values(self, sql: str, user_request: tuple = None) -> str:
        select_db = ''
        try:
            await self.open_connect()
            if user_request:
                try:
                    self.cursor.execute(sql, [user_request])
                except Exception as ex:
                    self.cursor.execute(sql, user_request)
            else:
                self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            if rows:
                # Получение названий столбцов
                column_names = self.return_column_names()
                # Вывод заголовков столбцов
                select_db += "\n" + "-" * 80 + "\n" + "| " + " | ".join(column_names) + " |" + "\n" + "-" * 80 + "\n"
                # Вывод данных
                for row in rows:
                    select_db += "| " + " | ".join(str(value) for value in row) + " |" + "\n"
                select_db += "-" * 80 + "\n"
                await self.close_conn()
                return select_db
            else:
                return "\n Данные в таблице отсутствуют \n"
        except Exception as ex:
            await self.close_conn()
            logger.exception(ex)

    async def update_row(self, table: Any, key: str, value: str, table_id: int) -> None:
        try:
            await self.open_connect()
            sql = f"UPDATE {table.table_name} SET {key}=(?) WHERE id = (?)"
            self.cursor.execute(sql, (value, table_id))
            self.conn.commit()
            await self.close_conn()
        except Exception as ex:
            logger.exception(ex)
            await self.close_conn()

    async def delete_row(self, table: Any, table_id: int) -> None:
        await self.open_connect()
        try:
            sql = f"DELETE FROM {table.table_name} WHERE id = (?)"
            self.cursor.execute(sql, str(table_id))
            self.conn.commit()
            await self.close_conn()
        except Exception as ex:
            logger.exception(ex)
            await self.close_conn()

    async def create_database(self) -> None:
        try:
            await self.open_connect()
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in self.cursor.fetchall()]
            tables_difference = return_table_difference(set(tables), LIST_TABLES)
            if tables_difference:
                await create_table_difference(self, tables_difference)
            await self.close_conn()
        except Exception as ex:
            await self.close_conn()
            logger.exception(ex)

    async def return_table_id(self, table: Any) -> str:
        try:
            await self.open_connect()
            sql = f"""select id from {table.table_name}
                              order by id DESC 
                              limit 1"""
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            await self.close_conn()
            return rows[0][0]
        except Exception as ex:
            await self.close_conn()
            logger.exception(ex)

    def return_column_names(self):
        return [description[0] for description in self.cursor.description]

    async def return_user_request(self, user_request: str) -> dict:
        await self.open_connect()
        lists_select = await self.select_values(LISTS_SQL, (user_request, user_request))
        picture_select = await self.select_values(PICTURE_SQL, (user_request, user_request))
        paragraphs_select = await self.select_values(PARAGRAPH_SQL, (user_request,))
        links_select = await self.select_values(LINKS_SQL, (user_request, user_request))
        headers_select = await self.select_values(HEADERS_SQL, (user_request,))
        await self.close_conn()
        return {Links.table_name: str(links_select),
                Headers.table_name: str(headers_select),
                Paragraph.table_name: str(paragraphs_select),
                Lists.table_name: str(lists_select),
                Picture.table_name: str(picture_select)}

    async def return_latest(self) -> dict:
        await self.open_connect()
        site_table = await self.select_values(return_sql(Site))
        links_table = await self.select_values(return_sql(Links))
        headers_table = await self.select_values(return_sql(Headers))
        paragraphs_table = await self.select_values(return_sql(Paragraph))
        lists_table = await self.select_values(return_sql(Lists))
        picture_table = await self.select_values(return_sql(Picture))
        await self.close_conn()
        return {Site.table_name: str(site_table),
                Links.table_name: str(links_table),
                Headers.table_name: str(headers_table),
                Paragraph.table_name: str(paragraphs_table),
                Lists.table_name: str(lists_table),
                Picture.table_name: str(picture_table)}

    async def close_conn(self) -> None:
        self.conn.close()


def return_table_difference(set_db_tables: set, set_table: set) -> set:
    return set_table - set_db_tables


async def create_table_difference(db: DataBase, t_diff: set) -> None:
    for table in t_diff:
        if table == Site.table_name:
            await db.create_table(Site)
            logger.debug(f"{Site.table_name} создана")
        if table == Lists.table_name:
            await db.create_table(Lists)
            logger.debug(f"{Lists.table_name} создана")
        if table == Picture.table_name:
            await db.create_table(Picture)
            logger.debug(f"{Picture.table_name} создана")
        if table == Links.table_name:
            await db.create_table(Links)
            logger.debug(f"{Links.table_name} создана")
        if table == Headers.table_name:
            await db.create_table(Headers)
            logger.debug(f"{Headers.table_name} создана")
        if table == Paragraph.table_name:
            await db.create_table(Paragraph)
            logger.debug(f"{Paragraph.table_name} создана")


def return_sql(table: Any) -> str:
    return f"""select * from {table.table_name}
               order by id desc
               limit 1"""

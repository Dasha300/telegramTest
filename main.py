from classes.Paragraph import Paragraph
from classes.Parser import Parser
from classes.Site import Site
from classes.Links import Links
from classes.Picture import Picture
from classes.Headers import Headers
from classes.Lists import Lists
import time
from loguru import logger

H_Tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']


# отправляем запрос с заголовками по нужному адресу

async def fill_site_table(link, parser, dbase):
    title = parser.return_title()
    site = Site(link=link, title=title)
    inserted_value = await dbase.insert_value(site)
    if inserted_value:
        site_id = await dbase.return_table_id(site)
        site.set_id(site_id)
        return site
    else:
        return None


async def fill_link_table(parser, site, dbase):
    tags = parser.return_list_tags('a')
    for tag in tags:
        links = Links(site_id=site.self_id)
        links.set_link(tag['href'])
        links.set_title(tag.text)
        await dbase.insert_value(links)


async def fill_picture_table(parser, site, dbase):
    tags = parser.return_list_tags('img')
    for tag in tags:
        picture = Picture(site_id=site.self_id)
        try:
            picture.set_alt(tag.attrs['alt'])
        except Exception as ex:
            logger.debug(ex)
            continue
        try:
            picture.set_src(tag.attrs['src'])
        except Exception as ex:
            logger.debug(ex)
            continue
        await dbase.insert_value(picture)


async def fill_headers(parser, site, dbase):
    for h_tags in H_Tags:
        tags = parser.return_list_tags(h_tags)
        for tag in tags:
            header = Headers(site_id=site.self_id, header=h_tags)
            header.set_content(tag.text)
            await dbase.insert_value(header)


async def fill_lists(parser, site, dbase):
    tags = parser.return_list_tags('ul')
    list_num = 0
    for tag in tags:
        for li in tag.findChildren('li'):
            lists = Lists(site_id=site.self_id, list_num=list_num)
            lists.set_content(li.text)
            await dbase.insert_value(lists)
        list_num += 1


async def fill_paragraphs(parser, site, dbase):
    tags = parser.return_list_tags('p')
    for tag in tags:
        paragraph = Paragraph(site_id=site.self_id)
        paragraph.set_content(tag.text)
        await dbase.insert_value(paragraph)


async def main(dbase, link):
    start_time = time.time()
    # link = "https://htmlacademy.ru/blog/html-tags/p"
    parser = Parser(link)
    await dbase.create_database()
    site = await fill_site_table(link, parser, dbase)
    if site:
        await fill_link_table(parser, site, dbase)
        await fill_picture_table(parser, site, dbase)
        await fill_headers(parser, site, dbase)
        await fill_lists(parser, site, dbase)
        await fill_paragraphs(parser, site, dbase)
    end_time = time.time()
    execution_time = end_time - start_time
    logger.debug(f"Время выполнения программы: {execution_time} секунд")

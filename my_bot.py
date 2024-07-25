from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from classes.DataBase import DataBase
from main import main
from yaml import load as yaml_load, SafeLoader
from munch import DefaultMunch


def get_conf() -> DefaultMunch:
    with open(f'config.yaml', 'r') as settings:
        configuration = DefaultMunch.fromDict(yaml_load(settings, SafeLoader))
    return configuration


config = get_conf()
BOT_TOKEN = config.token

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
db = DataBase(config.db_name)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await db.create_database()
    await main(db, "https://htmlacademy.ru/blog/html-tags/p")
    await message.answer("Привет! 👋 Я бот, который парсит сайты и может искать информацию, по введенной строке!")


@dp.message_handler(commands=['latest'])
async def latest(message: types.Message):
    latest_articles = await db.return_latest()
    latest_dict = dict(latest_articles)
    text = ''
    for key in latest_dict:
        text += f"В таблице {key} последние значения" + latest_dict[key]
    await message.answer(text)


@dp.message_handler(commands=['search'])
async def search(message: types.Message):
    try:
        search_query = " ".join(message.text.split(' ')[1:])  # Получение поискового запроса
        found_articles = await db.return_user_request(search_query)
        found_articles_dict = dict(found_articles)
        if found_articles_dict:
            text = f"Найдено по запросу {search_query}\n"
            for key in found_articles_dict:
                text += f"- {key} \n {found_articles_dict[key]} \n"
            await message.answer(text)
        else:
            await message.answer(f"По запросу '{search_query}' ничего не найдено.")
    except IndexError:
        await message.reply("Неверный формат команды. Используйте: /search [строка поиска]")


@dp.message_handler(commands=['insert'])
async def insert(message: types.Message):
    try:
        link = message.text.split(' ', 2)[1]  # Получение ссылки на статью
        await main(db, link)
        await message.reply(f"Статья '{link}' добавлена!")
    except IndexError:
        await message.reply("Неверный формат команды. Используйте: /insert [ссылка]")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)

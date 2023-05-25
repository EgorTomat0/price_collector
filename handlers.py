from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from FSM.states import SearchState
from loader import dp, bot
from parsers.children.kns_parser import KNSParser
from parsers.children.pleer_parser import PleerParser
from parsers.children.regard_parser import RegardParser
from utils.sort import dict_bubble_sort


@dp.message_handler(Command('start'))
async def start(message: types.Message):
    await SearchState.query_waiting.set()
    await bot.send_message(text="Здравствуйте, введите полное название товара, который вы хотите найти",
                           chat_id=message.chat.id)


@dp.message_handler(state=SearchState.query_waiting)
async def result(message: types.Message, state: FSMContext):
    await SearchState.in_search.set()
    bot_message = await bot.send_message(text="Поиск🔍...", chat_id=message.chat.id, reply_markup=None)
    query = message.text
    pleer = PleerParser(product_name=query).parse()
    regard = RegardParser(product_name=query).parse()
    kns = KNSParser(product_name=query).parse()
    results = [kns, pleer, regard]
    results_dict = {"prices": [], "links": []}
    for dictionary in results:
        for el in dictionary["price"]:
            results_dict["prices"].append(el)
        for el in dictionary["link"]:
            results_dict["links"].append(el)
    async with state.proxy() as data:
        data["result_message"] = bot_message
        data["pleer"] = pleer
        data["regard"] = regard
        data["kns"] = kns
    if len(results_dict["prices"]) != 0:
        results_dict = dict_bubble_sort(results_dict)
        await SearchState.search_result.set()
        async with state.proxy() as data:
            data["cheapest_price"] = results_dict['prices'][0]
            data["cheapest_url"] = results_dict['links'][0]
        await bot_message.edit_text(
            f"Самый дешёвый вариант: \n{results_dict['prices'][0]} руб.")
        await bot_message.edit_reply_markup(InlineKeyboardMarkup(row_width=1, inline_keyboard=[
            [
                InlineKeyboardButton(text="Результаты pleer.ru", callback_data="pleer"),
            ],
            [
                InlineKeyboardButton(text="Результаты regard.ru", callback_data="regard"),
            ],
            [
                InlineKeyboardButton(text="Результаты kns.ru", callback_data="kns")
            ],
            [
                InlineKeyboardButton(text="Купить🛒", url=results_dict['links'][0])
            ],
            [
                InlineKeyboardButton(text="Сделать новый запрос", callback_data="new_query")
            ]
        ]))
        await SearchState.search_result.set()
    else:
        await SearchState.query_waiting.set()
        await bot_message.edit_text(
            "По вашему запросу ничего не найдено. Пожалуйста введите корректное название модели.")


@dp.callback_query_handler(text="back", state=SearchState.search_result)
async def back(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        await data["result_message"].edit_text(
            f"Самый дешёвый вариант: \n{data['cheapest_price']} руб.")
        await data["result_message"].edit_reply_markup(InlineKeyboardMarkup(row_width=1, inline_keyboard=[
            [
                InlineKeyboardButton(text="Результаты pleer.ru", callback_data="pleer"),
            ],
            [
                InlineKeyboardButton(text="Результаты regard.ru", callback_data="regard"),
            ],
            [
                InlineKeyboardButton(text="Результаты kns.ru", callback_data="kns")
            ],
            [
                InlineKeyboardButton(text="Купить🛒", url=data["cheapest_url"])
            ],
            [
                InlineKeyboardButton(text="Сделать новый запрос", callback_data="new_query")
            ]
        ]))


@dp.callback_query_handler(text="pleer", state=SearchState.search_result)
async def pleer_results(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if len(data["pleer"]["price"]) != 0:
            await data["result_message"].edit_text("Все результаты pleer.ru:\n\n" + '\n\n'.join(
                [f'{data["pleer"]["price"][i]} руб. {data["pleer"]["link"][i]}' for i in
                 range(len(data["pleer"]["link"]))]))
            await data["result_message"].edit_reply_markup(InlineKeyboardMarkup(row_width=1, inline_keyboard=[
                [
                    InlineKeyboardButton(text="Назад⬅️", callback_data="back")
                ]
            ]))
        else:
            await call.answer("Этот сайт не нашёл товаров по вашему запросу", show_alert=True)


@dp.callback_query_handler(text="kns", state=SearchState.search_result)
async def kns_results(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if len(data["kns"]["price"]) != 0:
            await data["result_message"].edit_text("Все результаты kns.ru:\n\n" + '\n\n'.join(
                [f'{data["kns"]["price"][i]} руб. {data["kns"]["link"][i]}' for i in
                 range(len(data["kns"]["link"]))]))
            await data["result_message"].edit_reply_markup(InlineKeyboardMarkup(row_width=1, inline_keyboard=[
                [
                    InlineKeyboardButton(text="Назад⬅️", callback_data="back")
                ]
            ]))
        else:
            await call.answer("Этот сайт не нашёл товаров по вашему запросу", show_alert=True)


@dp.callback_query_handler(text="regard", state=SearchState.search_result)
async def regard_results(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if len(data["regard"]["price"]) != 0:
            await data["result_message"].edit_text("Все результаты regard.ru:\n\n" + '\n\n'.join(
                [f'{data["regard"]["price"][i]} руб. {data["regard"]["link"][i]}' for i in
                 range(len(data["regard"]["link"]))]))
            await data["result_message"].edit_reply_markup(InlineKeyboardMarkup(row_width=1, inline_keyboard=[
                [
                    InlineKeyboardButton(text="Назад⬅️", callback_data="back")
                ]
            ]))
        else:
            await call.answer("Этот сайт не нашёл товаров по вашему запросу", show_alert=True)


@dp.callback_query_handler(text="new_query", state=SearchState.search_result)
async def new_query(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        await data["result_message"].edit_text("Введите новый запрос")
        await SearchState.query_waiting.set()

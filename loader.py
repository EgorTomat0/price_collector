from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token='5995470726:AAEHUyBGwq4A1ZoM5Ao_nRXIm-H02TBTOR4')

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

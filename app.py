if __name__ == '__main__':
    from aiogram.utils import executor
    from handlers import dp

    executor.start_polling(dp)

from aiogram.dispatcher.filters.state import State, StatesGroup


class SearchState(StatesGroup):
    query_waiting = State()
    in_search = State()
    search_result = State()

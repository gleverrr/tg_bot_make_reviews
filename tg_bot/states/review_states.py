from aiogram.fsm.state import State, StatesGroup

class ReviewStates(StatesGroup):
    article = State()
    waiting_for_photos = State()
    waiting_for_photo2 = State()
    waiting_for_video = State()
    waiting_for_text = State()
    waiting_for_time = State()
    confirmation = State()
    
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_keyboard_photo():
    buttons = [
        KeyboardButton(text="Не хочу загружать фото")
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[buttons],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard

def get_keyboard_photo2():
    buttons = [
        KeyboardButton(text="Не хочу загружать второе фото")
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[buttons],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard

def get_keyboard_video():
    buttons = [
        KeyboardButton(text="Не хочу загружать видео")
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[buttons],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard
def get_keyboard_confirm():
    buttons = [
        KeyboardButton(text="Да"),
        KeyboardButton(text="Хочу отменить этот отзыв")
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[buttons],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard

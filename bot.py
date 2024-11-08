import logging
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types, Router
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
import os
from dotenv import load_dotenv
from tg_bot.handlers.messages import *
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, Message
from tg_bot.keyboards.review_kb import get_keyboard_photo, get_keyboard_photo2, get_keyboard_video, get_keyboard_confirm
from tg_bot.states.review_states import ReviewStates
from aiogram.fsm.context import FSMContext
from tg_bot.misc.functions import filling_bd_handler
from tg_bot.models.db_connection import get_db_session
from tg_bot.models.models import get_user_class, get_order_class
load_dotenv()
logging.basicConfig(level=logging.INFO)
BOT_TOKEN = os.getenv('BOT_TOKEN')
if BOT_TOKEN is None:
    print("BOT_TOKEN not found in .env file")
    raise ValueError("BOT_TOKEN not found in .env file")

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

router = Router()
session = get_db_session()
Order = get_order_class()
User = get_user_class() 
@router.message(Command("start"))
async def start_add_review(message: Message, state: FSMContext):
    user_id = str(message.from_user.id)
    account = session.query(User).filter(User.tg == user_id).first() 
    global db_user_id 
    if (account):
        db_user_id = account.id
        articles = session.query(Order).filter((Order.buyer_id == db_user_id) & (Order.marketplace == "WB") & (Order.status == 5)).distinct(Order.article).all()
        global accept_articles
        accept_articles = [] 
        buttons = []
        row = []
        for artic in articles:
            accept_articles.append(artic.article)
            row.append(KeyboardButton(text=artic.article))
            if len(row) == 2: 
                buttons.append(row)  
                row = [] 
        
        if row:
            buttons.append(row)
        global articles_keyboard
        articles_keyboard = ReplyKeyboardMarkup(
            keyboard=buttons,
            resize_keyboard=True,
            one_time_keyboard=True
        )
        await message.answer("Выберите артикул:", reply_markup=articles_keyboard)
        await state.set_state(ReviewStates.article)
    else :
        await message.answer("Кажется, у вас нет товаров, на которые можно оставить отзыв")
    
@router.message(ReviewStates.article)
async def get_article_message(message: Message,state: FSMContext):
    try:
        chosen_article = int( message.text)
        if chosen_article in accept_articles:
            global change_order
            change_order = session.query(Order).filter((Order.article == chosen_article) & (Order.buyer_id == db_user_id) & (Order.marketplace == "WB") & (Order.status == 5)).distinct(Order.article).first()
            await message.answer("Загрузите фотографии (до 2 штук)", reply_markup=get_keyboard_photo())
            await state.update_data(order_id=change_order.id)
            await state.set_state(ReviewStates.waiting_for_photos)
        else:
            await message.answer("Выберите корректный артикул", reply_markup=articles_keyboard)
    except ValueError:
        await message.answer("Выберите корректный артикул", reply_markup=articles_keyboard)

@router.message(ReviewStates.waiting_for_photos)
async def photo_handler(message: types.Message, state:FSMContext):
        if message.photo:
            await state.update_data(mess_ph1 = message, is_ph1 = True)
            await message.answer("Загрузите вторую фотографию", reply_markup=get_keyboard_photo2())
            await state.set_state(ReviewStates.waiting_for_photo2)

       
        elif (message.text == "Не хочу загружать фото"):
            await message.answer("Загрузите видео", reply_markup=get_keyboard_video())

            await state.update_data(is_ph1 = False)
            await state.set_state(ReviewStates.waiting_for_video)
        else:
            await message.answer("Загрузите фотографию или напишите 'Не хочу загружать фото'", reply_markup=get_keyboard_photo())

@router.message(ReviewStates.waiting_for_photo2)
async def photo2_handler(message: types.Message, state:FSMContext):
    if message.photo:
            await state.update_data(mess_ph2 = message, is_ph2 = True)
            await message.answer("Загрузите видео", reply_markup=get_keyboard_video())
            await state.set_state(ReviewStates.waiting_for_video)
    elif (message.text == "Не хочу загружать второе фото"):
            await message.answer("Загрузите видео", reply_markup=get_keyboard_video())
            await state.update_data(is_ph2 = False)
            await state.set_state(ReviewStates.waiting_for_video)
    else:
            await message.answer("Загрузите фотографию или напишите 'Не хочу загружать второе фото'", reply_markup=get_keyboard_photo2())
@router.message(ReviewStates.waiting_for_video)
async def video_handler(message: types.Message, state:FSMContext):
    if message.video:
         await state.update_data(mess_video = message, is_video = True)
         await message.answer("Введите текст вашео отзыва", reply_markup=types.ReplyKeyboardRemove())
         await state.set_state(ReviewStates.waiting_for_text)
    elif (message.text == "Не хочу загружать видео"):
         await state.update_data(is_video = False) 
         await message.answer("Введите текст вашео отзыва", reply_markup=types.ReplyKeyboardRemove())
         await state.set_state(ReviewStates.waiting_for_text)
    else:
         await message.answer("Загрузите видео или напишите 'Не хочу загружать видео'", reply_markup=get_keyboard_video())
@router.message(ReviewStates.waiting_for_text)
async def text_handler(message: types.Message, state:FSMContext):
     if not(message.text):
          await message.answer("Введите текст", reply_markup=types.ReplyKeyboardRemove())
          return
     if len(message.text) > 1023:
          await message.answer("Текст слишком длинный, должен быть до 1023 символов", reply_markup=types.ReplyKeyboardRemove()) 
          return
     await state.update_data(review_text = message.text)
     await message.answer("Введите время (в минутах), через которое опубликовать отзыв", reply_markup=types.ReplyKeyboardRemove())
     await state.set_state(ReviewStates.waiting_for_time)

@router.message(ReviewStates.waiting_for_time)
async def time_handler(message: types.Message, state:FSMContext):
     text = message.text
     try:
          t_int = int(text)
     except:
          await message.answer("Введите только число!", reply_markup=types.ReplyKeyboardRemove())
          return 
     new_t = datetime.now() + timedelta(minutes=t_int)
     await state.update_data(time_public = new_t) 
     await message.answer("Вы уверены, что хотите оставить этот отзыв?", reply_markup=get_keyboard_confirm())
     await state.set_state(ReviewStates.confirmation)
@router.message(ReviewStates.confirmation)
async def confirmation_handler(message: types.Message, state:FSMContext):
     if (message.text == "Да"):
          await message.answer("Хорошо! Ваш отзыв успешно сохранен", reply_markup=types.ReplyKeyboardRemove())
          await filling_bd_handler(state, bot, BOT_TOKEN)
          await state.clear() 
     elif (message.text == "Хочу отменить этот отзыв"):
          await message.answer("Ваш отзыв не будет отправлен", reply_markup=types.ReplyKeyboardRemove()) 
          await state.clear()
     else:
          await message.answer("Напшите 'да' или 'Хочу отменить этот отзыв'", reply_markup=get_keyboard_confirm())

dp.include_router(router)
router_s = Router()
register_message_handlers(router_s)
dp.include_router(router_s)
session.close() 
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
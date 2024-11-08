import os
import os
import requests
from aiogram import Bot, types
from aiogram.fsm.context import FSMContext
from tg_bot.models.db_connection import get_db_session
from tg_bot.models.models import get_order_class
def create_folder(order_id):
    base_path = os.path.join('uploads', str(order_id))
    photos_path = os.path.join(base_path, 'photos')
    videos_path = os.path.join(base_path, 'video')
    os.makedirs(photos_path, exist_ok=True)
    os.makedirs(videos_path, exist_ok=True)
    return {
        'base': base_path,
        'photos': photos_path,
        'video': videos_path
    }

async def put_photo_files(state:FSMContext, message: types.Message, bot: Bot, BOT_TOKEN, number):
    
    data = await state.get_data()
    order_id = data.get('order_id')
    paths = create_folder(order_id)
    photos_path = paths['photos']
    photo_info = message.photo[-1]  
    photo_file = await bot.get_file(photo_info.file_id)
    download_url = f'https://api.telegram.org/file/bot{BOT_TOKEN}/{photo_file.file_path}'
    file_response = requests.get(download_url)
    if file_response.status_code == 200:
        file_name = f'image{number}.jpg'
        save_path = os.path.join(photos_path, file_name)
        with open(save_path, 'wb') as f:
            f.write(file_response.content)
        print(f'Файл {file_name} успешно скачан и сохранен как {save_path}')
    else:
        print('Ошибка при скачивании файла.')


async def save_video_file(state: FSMContext, message: types.Message, bot: Bot, BOT_TOKEN):
    data = await state.get_data()
    order_id = data.get('order_id')
    paths = create_folder(order_id)
    videos_path = paths['video']
    video_info = message.video
    video_file = await bot.get_file(video_info.file_id)
    download_url = f'https://api.telegram.org/file/bot{BOT_TOKEN}/{video_file.file_path}'
    file_response = requests.get(download_url)
    if file_response.status_code == 200:
        file_name = f'video.mp4'
        save_path = os.path.join(videos_path, file_name)
        with open(save_path, 'wb') as f:
            f.write(file_response.content)
        print(f'Видео успешно скачано и сохранено как {save_path}')
    else:
        print('Ошибка при скачивании видео.')


async def filling_bd_handler(state:FSMContext, bot, BOT_TOKEN):
    data = await state.get_data()
    is_photo = data.get('is_ph1')
    if is_photo:
        ph2 = data.get('is_ph2') 
        mess_ph1 = data.get('mess_ph1') 
        await put_photo_files(state, mess_ph1, bot,BOT_TOKEN, 1)
        if ph2:
            mess_ph2 = data.get('mess_ph2') 
            await put_photo_files(state, mess_ph2, bot,BOT_TOKEN, 2)
    else:
         create_folder(data.get('order_id')) 
    is_video = data.get('is_video')
    if is_video:
         mess_video = data.get('mess_video')
         await save_video_file(state, mess_video, bot, BOT_TOKEN)
    
    r_text = data.get('review_text')
    r_time = data.get('time_public')
    session = get_db_session()
    Order = get_order_class()
    order_id = data.get('order_id')
    order = session.query(Order).filter(Order.id == order_id).first()
    if order:
        order.status = 6
        order.review_text = r_text
        if (is_video):
            order.review_video = '1'
        else:
            order.review_video = '0'
        if (is_photo):
            order.review_photo = '1'
        else:
            order.review_photo = '0' 
        order.review_data = r_time
        session.commit()

    session.close()
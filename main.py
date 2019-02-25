from model import ClassPredictor
from telegram_token import token
import torch
from config import reply_texts
import numpy as np
from PIL import Image
from io import BytesIO


model = ClassPredictor()
job_queue = Queue()


def worker(bot, queue):
    while True:
        message = queue.get()
        chat_id = message.chat_id
        print("Got image from {}".format(chat_id))

        
        image_info = message.photo[-1]
        image_file = bot.get_file(image_info)
        image_stream = BytesIO()
        image_file.download(out=image_stream)

        
        class_ = 1#model.predict(image_stream)
        sleep(10)

        message.reply_text(str(class_))
        print("Sent Answer to user, predicted: {}".format(class_))


def photo(bot, update):
    update.message.reply_text("Ваше фото помещено в очередь")
    job_queue.put(update.message)


if __name__ == '__main__':
    from telegram.ext import Updater, MessageHandler, Filters
    import logging

    
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)
    
    updater = Updater(token=token)
    updater.dispatcher.add_handler(MessageHandler(Filters.photo, photo))

   
    worker_args = (updater.bot, job_queue)
    worker_process = Process(target=worker, args=worker_args)
    worker_process.start()

    updater.start_polling()

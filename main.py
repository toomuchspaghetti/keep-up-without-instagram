from dotenv import load_dotenv
from typing import Final
import os
from telegram.ext import ApplicationBuilder, ExtBot
import asyncio
from time import sleep
from datetime import datetime
import subprocess
from PIL import Image, ImageChops
import re

SLEEP_SECONDS: Final = 5 * 60
WORK_DIR: Final = "work"
OLD_IMAGE_FILENAME: Final = "old.png"
NEW_IMAGE_FILENAME: Final = "new.png"

def send_notification(bot: ExtBot, chat_id: int):
    asyncio.run(bot.send_message(chat_id, "you have a notification from instagram!"))
    # TODO send photo

def load_image(filename: str):
    try:
        return Image.open(os.path.join(WORK_DIR, filename))
    except Exception:
        return

def main():
    try:
        if not load_dotenv(override=True):
            raise Exception()

        TELEGRAM_TOKEN: Final[str] = os.environ["TELEGRAM_TOKEN"]
        TELEGRAM_CHAT_ID: Final = int(os.environ["TELEGRAM_CHAT_ID"])
    except Exception:
        print("cannot load env")
        exit(1)

    def send_notification_quick(bot: ExtBot):
        send_notification(bot, TELEGRAM_CHAT_ID)

    os.makedirs(WORK_DIR, exist_ok=True)

    while True:
        try:
            print(f"trying... {datetime.now().astimezone().isoformat()}")

            result = re.search(r"success", subprocess.run(["node", "main.ts"], capture_output=True).stdout.decode())

            if result == None:
                raise Exception("cannot find \"success\", node script failed")

            old_image = load_image(OLD_IMAGE_FILENAME)
            
            if old_image != None:
                new_image = load_image(NEW_IMAGE_FILENAME)

                if new_image == None:
                    raise Exception("cannot find new image, node script is buggy!")
                
                difference_image = ImageChops.difference(old_image, new_image)

                if difference_image.getbbox() != None:
                    send_notification_quick(ApplicationBuilder().token(TELEGRAM_TOKEN).build().bot)

            os.rename(os.path.join(WORK_DIR, NEW_IMAGE_FILENAME), os.path.join(WORK_DIR, OLD_IMAGE_FILENAME))
        except Exception as e:
            print(f"whoops! error: {e}")
            raise

        sleep(SLEEP_SECONDS)

if __name__ == "__main__":
    main()
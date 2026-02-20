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
MODE: Final = "RGB"

def get_file_from_work_dir(filename: str) -> str:
    return os.path.join(WORK_DIR, filename)

async def send_notification_async(bot: ExtBot, chat_id: int):
    try:
        await bot.send_photo(chat_id, open(get_file_from_work_dir(NEW_IMAGE_FILENAME), "rb"), caption="your instagram has updated!")
    except Exception:
        await bot.send_message(chat_id, "oops! cannot send photo... but your instagram has updated")
        raise Exception("cannot send photo")
    

def send_notification(bot: ExtBot, chat_id: int):
    asyncio.run(send_notification_async(bot, chat_id))

def load_image(filename: str):
    try:
        return Image.open(get_file_from_work_dir(filename))
    except Exception:
        raise Exception(f"cannot load image \"{filename}\"")

def main():
    try:
        if not load_dotenv(override=True):
            raise Exception()

        TELEGRAM_TOKEN: Final[str] = os.environ["TELEGRAM_TOKEN"]
        TELEGRAM_CHAT_ID: Final = int(os.environ["TELEGRAM_CHAT_ID"])
    except Exception:
        print("cannot load env")
        return

    def send_notification_quick(bot: ExtBot):
        send_notification(bot, TELEGRAM_CHAT_ID)

    os.makedirs(WORK_DIR, exist_ok=True)

    while True:
        try:
            try:
                print(f"trying... {datetime.now().astimezone().isoformat()}")

                result = re.search(r"success", subprocess.run(["node", "main.ts"], capture_output=True).stdout.decode())

                if result == None:
                    raise Exception("cannot find \"success\", node script failed")

                new_image = load_image(NEW_IMAGE_FILENAME)

                if new_image == None:
                    raise Exception("cannot find new image, node script is buggy!")
                
                new_image = new_image.crop((0, 0, 13, new_image.height)).convert(MODE)
                
                old_image = load_image(OLD_IMAGE_FILENAME).convert(MODE)
                if old_image != None:
                    difference_image = ImageChops.difference(old_image, new_image)

                    if difference_image.getbbox() != None:
                        print("saw difference, sending notification.")
                        send_notification_quick(ApplicationBuilder().token(TELEGRAM_TOKEN).build().bot)

                new_image.save(get_file_from_work_dir(OLD_IMAGE_FILENAME))
            except Exception as e:
                print(f"whoops! error: {e}")

            sleep(SLEEP_SECONDS)
        except KeyboardInterrupt:
            print("\nquitting...")
            return
if __name__ == "__main__":
    main()
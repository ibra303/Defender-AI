__version__ = '0.1'
__author__ = 'Habib Ibrahim'

import data
from datetime import datetime
import winsound
from deepface import DeepFace
from telegram import Bot, TelegramError, InputFile
from moviepy.editor import VideoFileClip


def delayDetecting_function():
    print("Detecting Again")
    data.detecting = True


# Beeb sound when alert is true
def beep_alarm():
    for _ in range(1):
        if not data.alarm_mode:
            break
        print("צבע אדום")
        winsound.Beep(2500, 1000)
    data.alarm = False


# Sending alert to telegram channel
def send_alert(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    bot = Bot(token=data.TOKEN)
    if message == "not familiar":
        alert_message = f"🚨 RED ALERT 🚨[{timestamp}] \n\nMotion detected in your room! \n "
        try:
            convert_avi_to_mp4(data.output_path, 'output_video.mp4')
            with open('output_video.mp4', 'rb') as video:
                bot.send_video(chat_id=data.CHANNEL_ID, video=InputFile(video), caption=alert_message)
            print(f"Message sent: {message}")
        except TelegramError as e:
            print(f"Error sending message: {e}")

    elif message == "familiar":
        alert_message = f"🚨" + data.faceNames + " is home[" + timestamp + "]\n\nHave a good day! \n "
        try:
            bot.send_message(chat_id=data.CHANNEL_ID, text=alert_message)
            print(f"Message sent: {message}")
        except TelegramError as e:
            print(f"Error sending message: {e}")


def convert_avi_to_mp4(input_file, output_file):
    try:
        clip = VideoFileClip(input_file)
        clip.write_videofile(output_file, codec='libx264', audio_codec='aac')
        print(f"Conversion successful: {output_file}")
    except Exception as e:
        print(f"Error during conversion: {e}")


# Main code
def isFamiliar(frame1):
    try:
        for ref_picture in data.ref_pictures:
            if DeepFace.verify(frame1, ref_picture.copy())['verified']:
                print("fam face")
                data.familiar = True
                break
            else:
                print("not fam face")
                data.familiar = False
    except ValueError:
        print("error fam")
        data.familiar = False

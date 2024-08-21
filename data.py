__version__ = '0.1'
__author__ = 'Habib Ibrahim'

import os
import cv2

# Telegram Channel Bot Token and Channel ID
TOKEN = '6986314525:AAEPsbfUdyRuItgnVIv2OtekqouxTqDmurU'
CHANNEL_ID = '@DefenderAI'

# Folder path containing the reference pictures
folder_path = "pics"

# Get all files in the folder
all_files = os.listdir(folder_path)

# Filter only image files (assuming images have extensions like .jpg, .png, etc.)
image_files = [file for file in all_files if file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]

# Load reference pictures
ref_pictures = [cv2.imread(os.path.join(folder_path, file)) for file in image_files]

# ref_picture = cv2.imread("pics/ref_pic.jpg")
alarm_mode = False
alarm_counter = 0

output_path = 'captured_video_no_sound.avi'

# Set the delay time to 60 seconds
delay_seconds = 60
alarm = False
detecting = True
familiar = False
faceNames = "Habib"

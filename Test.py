import os,datetime
import shutil
from datetime import datetime

archive = "C:\\Users\\tony\\PycharmProjects\\SystemTest\\Archive"
log_file_path = "C:\\Users\\tony\\PycharmProjects\\SystemTest\\Log\\SystemTest.log"
screenshots_path = "C:\\Users\\tony\\PycharmProjects\\SystemTest\\Screenshots"


#CD = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")

"""if not (os.path.exists(archive)):
    os.makedirs(archive)
elif os.path.exists(screenshots_path) and os.path.isfile(log_file_path):
    # Move Log into Screenshot folder
    shutil.move(log_file_path, screenshots_path)
    if len(os.listdir(screenshots_path)) > 0:
        # Move Screenshot folder to archive folder
        shutil.move(screenshots_path, os.path.join(archive, CD + "_" + "Log and Screenshots"))
        os.makedirs(screenshots_path)"""


date = datetime.today().date()
print(date)



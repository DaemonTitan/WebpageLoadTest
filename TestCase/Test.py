import os,datetime
import shutil

archive = "C:\\Users\\tony\\PycharmProjects\\SystemTest\\Archive"
log_file_path = "C:\\Users\\tony\\PycharmProjects\\SystemTest\\Log\\SystemTest.log"
screenshots_path = "C:\\Users\\tony\\PycharmProjects\\SystemTest\\Screenshots"

record = []
CD = datetime.datetime.now().strftime("%d_%m_%Y")
CT = datetime.datetime.now().strftime("%H_%M_%S")

if not (os.path.exists(archive)):
    os.makedirs(archive)
elif os.path.exists(screenshots_path) and os.path.isfile(log_file_path):
    shutil.move(log_file_path, screenshots_path)
    if len(os.listdir(screenshots_path)) > 0:
        shutil.move(screenshots_path, os.path.join(archive, CD+"_"+CT+"_"+"Log and Screenshots"))
        os.makedirs(screenshots_path)
        record.append(CD)
        print(record)

compare = record > CD
print(compare)




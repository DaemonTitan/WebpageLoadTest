import os, datetime
import shutil

archive = "C:\\Users\\tony\\PycharmProjects\\SystemTest\\Archive"
log_file_path = "C:\\Users\\tony\\PycharmProjects\\SystemTest\\Log\\SystemTest.log"
screenshots_path = "C:\\Users\\tony\\PycharmProjects\\SystemTest\\Screenshots"

CD_filename = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
today = datetime.datetime.now()

# newdate = datetime.datetime.strptime(CD, '%d_%m_%Y_%H_%M_%S')
# print(newdate.date())

try:
    # Create archive if not exists
    if not (os.path.exists(archive)):
        os.makedirs(archive)
    # Get creation date from first file
    elif len(os.listdir(archive)) > 0:
        folder_name = []
        for f in os.listdir(archive):
            arch_file = os.path.join(archive, f)
            if os.path.isdir(arch_file):
                folder_name.append(arch_file)
        first_folder = min(folder_name, key=os.path.getmtime)
        print(first_folder)
        file_mdate = datetime.datetime.fromtimestamp(os.path.getctime(first_folder))
        print(file_mdate)
        # add 2 days to first file
        new_f_date = file_mdate + datetime.timedelta(days=2)
        # Compare current date with first file
        if new_f_date == today:
            shutil.rmtree(archive)
            os.makedirs(archive)
    else:
        print("Date not match, cannot delete archive folder")
except IOError as error:
    print(error)

try:
    # Move file to archive folder
    if os.path.exists(screenshots_path) and os.path.isfile(log_file_path):
        # Move Log into Screenshot folder
        shutil.move(log_file_path, screenshots_path)
        # Move Screenshot folder to archive folder
        shutil.move(screenshots_path, os.path.join(archive, CD_filename + "_" + "SystemTestLog"))
        os.makedirs(screenshots_path)
except IOError as error:
    print(error)

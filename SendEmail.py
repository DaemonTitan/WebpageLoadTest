import smtplib, re, os, datetime, logging, shutil
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from logging.handlers import RotatingFileHandler

"""Email Logging Setting"""
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
LOG_FORMAT = logging.Formatter('%(levelname)s %(asctime)s - %(message)s')
file_handler = RotatingFileHandler('Email_Log.log', maxBytes=1000, backupCount=1)
file_handler.setFormatter(LOG_FORMAT)
logger.addHandler(file_handler)

"File path"
log_file_path = 'C:\\Users\\PycharmProjects\\SystemTest\\Log\\SystemTest.log'
screenshots_path = 'C:\\Users\\PycharmProjects\\SystemTest\\Screenshots'
archive = 'C:\\Users\\tony\\PycharmProjects\\SystemTest\\Archive'

"""Current Date"""
CD = datetime.datetime.now().strftime('%d/%m/%Y_%H:%M:%S')
CD_filename = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
date_TD = (datetime.datetime.now()).date()

"""Email Setting"""
smtp_server = 'smtp.office365.com'
port = 587
# sender_email = os.environ.get('Admin_Email')
# sender_pass = os.environ.get('Admin_Pass')
# receiver_email = ['xx@xx.com']

sender_email = os.environ.get('Email')
sender_pass = os.environ.get('Email_Pass')
receiver_email = ['xx@xx.com']


def run_test():
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
            first_folder = min(folder_name, key=os.path.getctime)
            file_cdate = (datetime.datetime.fromtimestamp(os.path.getctime(first_folder))).date()
            # add 2 days to first file's creation date
            new_f_date = file_cdate + datetime.timedelta(days=4)
            # Compare current date with first file's creation date
            if new_f_date == date_TD:
                shutil.rmtree(archive)
                os.makedirs(archive)
                logger.info("Archive folder cleared out")
            else:
                logger.info("Date not match, cannot delete archive folder")
        else:
            logger.info("Archive Task fail")
    except IOError as error:
        logger.info(error)
    # Move log to archive folder
    try:
        # Move file to archive folder
        if os.path.exists(screenshots_path) and os.path.isfile(log_file_path):
            # Move Log into Screenshot folder
            shutil.move(log_file_path, screenshots_path)
            # Move Screenshot folder to archive folder
            shutil.move(screenshots_path, os.path.join(archive, CD_filename + "_" + "SystemTestLog"))
            os.makedirs(screenshots_path)
            logger.info("Files moved into archive folder")
    except IOError as error:
        logger.info(error)



def send_email():
    """Search ERROR in log file"""
    if log_file_path != "":
        with open(log_file_path, mode='r') as file:
            for line in file:
                if re.search(r"\B[-] ERROR[:]", line):
                    """Email Content"""
                    logger.info("Find testing error. Drafting Email")
                    msg = MIMEMultipart()
                    msg['From'] = sender_email
                    msg['To'] = ', '.join(receiver_email)
                    msg['Subject'] = "Error Found During Testing"
                    #Email Body
                    msg.attach(MIMEText(
                        "<b>%s</b>" % (
                            "Hi all, "
                            "<br><br>An error occurred  during testing. Please see attached log and image."
                            "<br><br>Tested at: "+CD+
                            "<br><br>Error Message: "+line[34:]), 'html'))

                    #Attach log file
                    try:
                        with open(log_file_path, 'rb') as attach_log:
                            logfile = attach_log.read()
                            attach_text = MIMEText(logfile, 'plain', 'utf-8')
                            attach_text.add_header('Content-Disposition', 'attachment', filename='Log.txt')
                            msg.attach(attach_text)
                            logger.info("Attaching log file")
                    except IOError as error:
                        logger.info(error)

                    #Attach screenshots
                    if len(os.listdir(screenshots_path)) > 0:
                        files = os.listdir(screenshots_path)
                        for image in files:
                            file_path = os.path.join(screenshots_path, image)
                            image_name = os.path.basename(image)
                            open_image = open(file_path, 'rb')
                            image = MIMEImage(open_image.read())
                            open_image.close()
                            image.add_header('Content-Disposition', 'attachment', filename=image_name)
                            msg.attach(image)
                        logger.info("Attaching screenshots")
                    else:
                        logger.info("Can not find any screenshots to attach")
                    try:
                        smtpObj = smtplib.SMTP(smtp_server, port)
                        smtpObj.ehlo()
                        smtpObj.starttls()
                        smtpObj.login(sender_email, sender_pass)
                        smtpObj.sendmail(sender_email, receiver_email, msg.as_string())
                        logger.info("Error found email sent\n")
                        # print("Email sent")
                        smtpObj.quit()
                    except Exception as e:
                        logger.info(e)
            logger.info("No errors. Not send email\n")
        file.close()
    else:
        logger.info("Can not find log file. Email didn't sent")


if __name__ == "__main__":
    run_test()
    from TestCase.TestCases import CCE_test
    CCE_test()
    send_email()

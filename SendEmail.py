import smtplib, re, os, datetime, logging, shutil
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from TestCase import TestCases

"""Email Logging Setting"""
LOG_FORMAT = '%(levelname)s %(asctime)s - %(message)s'
logging.basicConfig(filename='C:\\Users\\tony\\PycharmProjects\\SystemTest\\Email_Log.log',
                    level=logging.INFO, format=LOG_FORMAT, datefmt='%d/%m/%Y %H:%M:%S', filemode='a')
logger = logging.getLogger()

"File path"
log_file_path = 'C:\\Users\\tony\\PycharmProjects\\SystemTest\\Log\\SystemTest.log'
screenshots_path = 'C:\\Users\\tony\\PycharmProjects\\SystemTest\\Screenshots'
archive = 'C:\\Users\\tony\\PycharmProjects\\SystemTest\\Archive'

"""Current Date"""
CD = datetime.datetime.now().strftime('%d/%m/%Y_%H:%M:%S')
CD_filename = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
today = datetime.datetime.now()

"""Email Setting"""
smtp_server = 'smtp.office365.com'
port = 587
sender_email = os.environ.get('Admin_Email')
sender_pass = os.environ.get('Admin_Pass')
receiver_email = ['tony@integrumsystems.com']


# sender_email = os.environ.get('Email')
# sender_pass = os.environ.get('Email_Pass')
#receiver_email = 'tony@integrumsystems.com'

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
                        logger.info("Email sent\n")
                        print("Email sent")
                        smtpObj.quit()
                    except Exception as e:
                        logger.info(e)
        file.close()
    else:
        logger.info("Can not find log file. Email didn't sent")


if __name__ == "__main__":
    # archive_task()
    TestCases.CCE_test()
    send_email()

import smtplib, re, os, datetime,logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
#from TestCase import TestCases

"""Email Logging Setting"""
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename="C:\\Users\\tony\\PycharmProjects\\SystemTest\\Email_Log.log",
                    level=logging.INFO, format=LOG_FORMAT, datefmt='%d/%m/%Y %H:%M:%S', filemode='a')
logger = logging.getLogger()


"File path"
log_file_path = "C:\\Users\\tony\\PycharmProjects\\SystemTest\\Log\\SystemTest.log"
screenshots_path = "C:\\Users\\tony\\PycharmProjects\\SystemTest\\Screenshots"
archive = "C:\\Users\\tony\\PycharmProjects\\SystemTest\\Archive"

"""Current Date"""
CD = datetime.datetime.now().strftime("%d/%m/%Y_%H:%M:%S")

"""Email Setting"""
smtpObj = smtplib.SMTP("smtp.office365.com", 587)
smtpObj.ehlo()
smtpObj.starttls()
smtpObj.login("sysadmin@integrumsystems.com", "Kur03463")
sender_email = "sysadmin@integrumsystems.com"
receiver_email = ["tony@integrumsystems.com", "Monica@integrumsystems.com"]
#smtpObj.login("tony@integrumsystems.com", "2121083Ct")
#sender_email = "tony@integrumsystems.com"
#receiver_email = "tony@integrumsystems.com"

def send_email():
    """Search ERROR in log file"""
    if log_file_path != "":
        with open(log_file_path, mode='r') as file:
            for line in file:
                if re.search(r"\BRROR", line):
                    """Email Content"""
                    logger.info("Find testing error. Drafting Email")
                    msg = MIMEMultipart()
                    msg['From'] = sender_email
                    msg['To'] = ", ".join(receiver_email)
                    #msg['To'] = receiver_email
                    msg['Subject'] = 'Error Found During Testing'
                    #Email Body
                    msg.attach(MIMEText(
                        '<b>%s</b>' % (
                            "Hi all, "
                            "<br><br>An error occurred  during testing. Please see attached log and image."
                            "<br><br>Tested at: "+CD+
                            "<br><br>Error Message: "+line[34:]), 'html'))

                    #Attach log file
                    with open(log_file_path, "rb") as attach_log:
                        logfile = attach_log.read()
                        attach_text = MIMEText(logfile, "plain", "utf-8")
                        attach_text.add_header("Content-Disposition", "attachment", filename="Log.txt")
                        msg.attach(attach_text)
                        logger.info("Attaching log file")

                    #Attach screenshots
                    if len(os.listdir(screenshots_path)) > 0:
                        files = os.listdir(screenshots_path)
                        for image in files:
                            file_path = os.path.join(screenshots_path, image)
                            image_name = os.path.basename(image)
                            image = MIMEImage(open(file_path, 'rb').read())
                            image.add_header("Content-Disposition", "attachment", filename=image_name)
                            msg.attach(image)
                            logger.info("Attaching screenshots")
                    else:
                        logger.info("Can not find any screenshots to attach")
                    try:
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
    #TestCases.CCE_test()
    send_email()

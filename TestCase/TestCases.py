# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#   The testing cases tests CCE Live testing only.           #
#   The test cases perform below testing                     #
#    1. Test CCE Prod Server is On                           #
#    2. Log in Test                                          #
#    3. Test Action Management View                          #
#    4. Test Create Action Management                        #
#    5. Test YF Access and BI Loads                          #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import logging, os

"""Test Account"""
loginUsername = os.environ.get('CCETest')
loginPassword = os.environ.get('CCETest_Pass')

"""Logging Setting"""
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
LOG_FORMAT = logging.Formatter("%(levelname)s %(asctime)s - %(message)s", "%d-%m-%Y %H:%M:%S")
file_handler = logging.FileHandler('C:\\Users\\\PycharmProjects\\SystemTest\\Log\\SystemTest.log')
file_handler.setFormatter(LOG_FORMAT)
logger.addHandler(file_handler)

"""Open in browser"""
browser_name = "Chrome"
if browser_name == "Chrome":
    driver = webdriver.Chrome(ChromeDriverManager().install())
elif browser_name == "Firefox":
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
else:
    # print("Browser Name:" + browser_name)
    raise Exception("Driver not found")
driver.implicitly_wait(10)
driver.minimize_window()


def CCE_test():

    """Starts Testing"""
    """Test Case 1: Test CCE Live Server is On"""
    logger.info("-----------------TESTING STARTED-----------------")
    try:
        driver.get("URL")
    except WebDriverException:
        logger.info("ERROR: Site not reachable")
        driver.save_screenshot("C:\\Users\\PycharmProjects\\SystemTest\\Screenshots\\Site_down.png")
        logger.info("-----------------TESTING COMPLETED-----------------")
        driver.implicitly_wait(10)
        driver.quit()
        return

    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "user-id")))
        # print("Login page loads")
        logger.info("Login page loads")
    except TimeoutException:
        logger.info("ERROR: Login page time out or Server is down")
        driver.save_screenshot("C:\\Users\\PycharmProjects\\SystemTest\\Screenshots\\Login_page_error.png")
        logger.info("-----------------TESTING COMPLETED-----------------")
        driver.implicitly_wait(10)
        driver.quit()
        return
    else:
        # Log in with test account
        logger.info("Start Login with Test2 Test2 account")
        driver.implicitly_wait(1)
        driver.find_element_by_id("user-id").clear()
        driver.find_element_by_id("user-id").send_keys(loginUsername)
        driver.implicitly_wait(1)
        driver.find_element_by_id("pw-id").clear()
        driver.find_element_by_id("pw-id").send_keys(loginPassword)
        driver.find_element_by_class_name("button-link").click()

    """Test Case 2: Log in Test"""
    try:
        driver.implicitly_wait(1)
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//frameset[1]/frame[1]")))
        #print("Login successfully")
        logger.info("Login successfully")
    except TimeoutException:
        logger.info("ERROR:Landing page is not loading")
        driver.save_screenshot("C:\\Users\\PycharmProjects\\SystemTest\\Screenshots\\Landing_Page_error.png")
        logger.info("-----------------TESTING COMPLETED-----------------")
        driver.implicitly_wait(10)
        driver.quit()
        return

    """ Test Cases 3: Test Action Management View"""
    # Switch to Project IMS Group Profile
    driver.implicitly_wait(2)
    try:
        driver.switch_to.frame(driver.find_element_by_xpath("/html[1]/frameset[1]/frame[1]"))  #Switch to frame
        driver.switch_to.frame(driver.find_element_by_name("BLF_P"))  #Switch to left frame
        group_name = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//option[contains(text(),'Project IMS')]")))
        group_name.click()
        #print("Access Project IMS Group Profile")
        logger.info("Access Project IMS Group Profile")
    except (TimeoutException, NoSuchElementException) as error:
        logger.info("ERROR:" + error)
        driver.save_screenshot("C:\\Users\\PycharmProjects\\SystemTest\\Screenshots\\Left_Panel_Not_Loading.png")
        logger.info("-----------------TESTING COMPLETED-----------------")
        driver.implicitly_wait(10)
        driver.quit()
        return
    # Open Action Management View
    driver.implicitly_wait(2)
    try:
        driver.find_element_by_xpath("//a[contains(text(),'Smart Form View - Action Management')]").click()
        driver.switch_to.default_content() # Back to HTML top content level
        driver.switch_to.frame(driver.find_element_by_xpath("/html[1]/frameset[1]/frame[1]"))
        driver.switch_to.frame(driver.find_element_by_name("TRF_P"))  # Switch to right frame
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='NewDoc']")))
        #print("Load SF View")
        logger.info("Load SF View")
    except (TimeoutException, NoSuchElementException) as error:
        logger.info("ERROR:" + error)
        driver.save_screenshot("C:\\Users\\PycharmProjects\\SystemTest\\Screenshots\\View_Not_Loading.png")
        logger.info("-----------------TESTING COMPLETED-----------------")
        driver.implicitly_wait(10)
        driver.quit()
        return
    # Loads SF View Contents
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH,"/html[1]/body[1]/div[3]/table[1]/tbody[1]/tr[2]/td[3]/table[1]/tbody[1]/tr[2]")))
        #print("SF view Contents Loads successfully")
        logger.info("SF view Contents Loads successfully")
    except TimeoutException:
        logger.info("ERROR: Load SF view content time out")
        driver.save_screenshot(
            "C:\\Users\\PycharmProjects\\SystemTest\\Screenshots\\Load_SF_view_content_time_out.png")
        logger.info("-----------------TESTING COMPLETED-----------------")
        driver.implicitly_wait(10)
        driver.quit()
        return

    """Test Case 4: Test Create Action Management SF"""
    home_page = driver.window_handles[0]
    try:
        new_form_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='NewDoc']")))
        new_form_button.click()
        #print("Click on Create New SF Button")
        logger.info("Click on Create New SF Button")
    except TimeoutException:
        logger.info("ERROR: Time out on loading new doc button")
        driver.save_screenshot(
            "C:\\Users\\PycharmProjects\\SystemTest\\Screenshots\\New_Doc_Button_not_Loading.png")
        logger.info("-----------------TESTING COMPLETED-----------------")
        driver.implicitly_wait(10)
        driver.quit()
        return
    try:
        template = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Action Management')]")))
        template.click()
        new_form = driver.window_handles[1]
        driver.switch_to.window(new_form)
        driver.minimize_window()
        #print("New SF Created")
        logger.info("New SF Created"+"["+driver.current_url+"]")
    except TimeoutException:
        logger.info("ERROR: Time out on loading template button")
        driver.save_screenshot("C:\\Users\\PycharmProjects\\SystemTest\\Screenshots\\Create_SF_Error.png")
        logger.info("-----------------TESTING COMPLETED-----------------")
        driver.implicitly_wait(10)
        driver.quit()
        return
    # Test SF contents load
    try:
        ou_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, "//tbody/tr[1]/td[2]/div[1]/span[1]/div[1]")))
        ou_field.click()
        #print("SF Content loads")
        logger.info("SF Content loads")
    except TimeoutException:
        logger.info("ERROR: SF content is not loading")
        driver.save_screenshot(
            "C:\\Users\\PycharmProjects\\SystemTest\\Screenshots\\SF_Content_not_loading.png")
        logger.info("-----------------TESTING COMPLETED-----------------")
        driver.implicitly_wait(10)
        driver.quit()
        return
    else:
        """Close SF window and go back to home page"""
        driver.implicitly_wait(10)
        driver.close()
        driver.switch_to.window(home_page)
        driver.minimize_window()

    """Test Case 5: Test YF Access and BI Report Loads """
    # Load YF
    try:
        driver.switch_to.frame(driver.find_element_by_xpath("/html[1]/frameset[1]/frame[1]"))  #Switch to frame
        driver.switch_to.frame(driver.find_element_by_name("BLF_P"))  #Switch to left frame
        group_name = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Business Reporting')]")))
        group_name.click()
        #print("Open YF")
        logger.info("Open YF")
        driver.implicitly_wait(15)
        driver.switch_to.default_content()  # Back to HTML top content level
        driver.switch_to.frame(driver.find_element_by_xpath("/html[1]/frameset[1]/frame[1]"))
        driver.switch_to.frame(driver.find_element_by_name("TRF_P"))  # Switch to right frame
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
            (By.CLASS_NAME, "mainToolbarItem")))
        #print("YF Loads")
        logger.info("YF Loads")
    except (TimeoutException, NoSuchElementException):
        logger.info("ERROR: YF not loading")
        driver.save_screenshot("C:\\Users\\PycharmProjects\\SystemTest\\Screenshots\\YF_Not_Loading.png")
        logger.info("-----------------TESTING COMPLETED-----------------")
        driver.implicitly_wait(10)
        driver.quit()
        return

    # Load YF Dashboard
    try:
        if WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "dashboardMainPartTable"))):
            #print("Can not find dashboards")
            logger.info("Can not find dashboards")
        elif WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "i4DashColumn"))):
            #print("YF Dashboard loads")
            logger.info("YF Dashboard loads")
    except TimeoutException:
        logger.info("ERROR: Can not load Dashboard and report")
        driver.save_screenshot("C:\\Users\\PycharmProjects\\SystemTest\\Screenshots\\Dashboard_Not_Loading.png")
        logger.info("-----------------TESTING COMPLETED-----------------")
        driver.implicitly_wait(10)
        driver.quit()
        return
    else:
        """CLose browser and Test Completes"""
        driver.implicitly_wait(15)
        driver.quit()
    logger.info("-----------------TESTING COMPLETED-----------------")

if __name__ == "__main__":
    CCE_test()


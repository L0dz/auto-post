import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import autoit
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
driver=''

#to disable GUI
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')

def setup_phone(username, password):
    global driver
    #setting chrome options
    options = Options()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1')
    driver=webdriver.Chrome(ChromeDriverManager().install(), options=options)

    #open the browser
    driver.get('https://instagram.com')
    time.sleep(2)

    #instagram access
    driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div/div/div/div[2]/button').click()
    time.sleep(5)
    print('Writing credentials')
    driver.find_element_by_xpath('//*[@id="loginForm"]/div[1]/div[3]/div/label/input').send_keys(username)
    driver.find_element_by_xpath('//*[@id="loginForm"]/div[1]/div[4]/div/label/input').send_keys(password)
    driver.find_element_by_xpath('//*[@id="loginForm"]/div[1]/div[6]').click()
    time.sleep(3)

    #get rid of annoying pop ups
    try:
        driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/button').click()
    except Exception as e:
        print('passed')
    for x in range(2):
        try:
            driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]').click()
        except Exception as e:
            print('passed')
        time.sleep(2)


def upload(username, password, path, desc):
    #setup
    setup_phone(username, password)

    #upload the image
    print('UPLOAD')
    driver.find_element_by_xpath('//*[@id="react-root"]/section/nav[2]/div/div/div[2]/div/div/div[3]').click()
    time.sleep(2)

    #select image from the pc
    autoit.win_active("Apri") #open can change by your os language if not open change that
    time.sleep(2)
    autoit.control_send("Apri", "Edit1", path)
    time.sleep(1.5)
    autoit.control_send("Apri", "Edit1", "{ENTER}")
    time.sleep(3)
    print('Posting...')

    #adjust image
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.find_element_by_xpath('//*[@id="react-root"]/section/div[2]/div[2]/div/div/div/button[1]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="react-root"]/section/div[1]/header/div/div[2]/button').click()
    time.sleep(0.5)

    #set description
    driver.find_element_by_xpath('//*[@id="react-root"]/section/div[2]/section[1]/div[1]/textarea').send_keys(desc)

    #publish
    driver.find_element_by_xpath('//*[@id="react-root"]/section/div[1]/header/div/div[2]/button').click()
    driver.close()


def setup(username, password):
    global driver
    #setting chrome options
    options = Options()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    driver=webdriver.Chrome(ChromeDriverManager().install(), options=options)

    #open chrome
    driver.get('https://instagram.com')
    time.sleep(2)

    #instagram login
    driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input').send_keys(username)
    driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input').send_keys(password)
    driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]').click()
    time.sleep(3)

    #get rid of annoying pop ups
    try:
        driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/div/button').click()
    except Exception as e:
        print('passed')
    for x in range(2):
        try:
            driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[3]/button[2]').click()
        except Exception as e:
            print('passed')
        time.sleep(2)



def upload_vid(username, password, path, desc):
    #setup
    setup(username, password)

    #go to profile
    driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[5]/span/img').click()
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/div[5]/div[2]/div/div[2]/div[2]/a[1]/div').click()
    time.sleep(3.5)
    driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/a[2]/span/span').click()
    time.sleep(2.5)

    #upload igtv
    driver.find_element_by_css_selector('#react-root > section > main > div > div._2z6nI > div > div.SRori > div > a > button').click()
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/form/div/div[1]/label/div/div/div[2]').click()
    time.sleep(1)

    #select image from the pc
    autoit.win_active("Apri") #open can change by your os language if not open change that
    time.sleep(2)
    autoit.control_send("Apri", "Edit1", path)
    time.sleep(1.5)
    autoit.control_send("Apri", "Edit1", "{ENTER}")

    time.sleep(2)
    #wait for the video to upload
    while(driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/form/div/div[1]/label/div/div/div/div/div[2]').text != '100%'):
        time.sleep(1)

    #set description
    driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/form/div/div[2]/div[5]/div/div/textarea').send_keys(desc)

    #publish
    driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/form/div/div[2]/div[9]/button').click()
    driver.close()

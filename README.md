# meets_checkin
避免上晨會後，還要在開啟google表單點選報到。
# 這是for 會議室:meets 、 報到表單: google
# 有用其他的要在依照不同網頁調整爬的內容，框和流程大概是這樣
# 直接照抄一定不能用 :)
```python
import requests
from bs4 import BeautifulSoup
import time
import json
import schedule
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def job():
    # 設定Chrome瀏覽器啟動選項
    options = webdriver.ChromeOptions()
    # 開啟chrome權限，避免跳出授權視窗
    options.add_experimental_option("prefs", { \
        "profile.default_content_setting_values.media_stream_mic": 1,     # 1:allow, 2:block 
        "profile.default_content_setting_values.media_stream_camera": 1,  # 1:allow, 2:block 
        "profile.default_content_setting_values.geolocation": 1,          # 1:allow, 2:block 
        "profile.default_content_setting_values.notifications": 1         # 1:allow, 2:block 
    })
    # # 不開瀏覽器執行(還是base on google)
    options.add_argument('--headless')
    # 關掉一些LOG
    options.add_argument('--log-level=3')
    # 避免 print 出的資料有[0615/125210.910:ERROR:socket_manager.cc(141)] Failed to resolve address for meet-jit-si-turnrelay.jitsi.net., errorcode: -105
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # 開啟瀏覽器
    driver = webdriver.Chrome(options=options)
    #會議室的url
    # url = '你自己會議室的url'
    driver.get(url)
    driver.set_window_size(1440, 1200)
    time.sleep(2)
    #這邊是selenium開始依照html格式爬資料
    #適時的sleep很重要，selenium跑太快網頁跟不上會報錯
    driver.find_element(By.CSS_SELECTOR, ".css-hh0z88-input").click()
    driver.find_element(By.CSS_SELECTOR, ".css-hh0z88-input").send_keys('點名機器人')
    driver.find_element(By.CSS_SELECTOR, ".css-1hbmoh1-actionButton").click()
    try:
        time.sleep(1)
        driver.find_element(By.NAME, "lockKey").click()
        #會議室密碼，有換其他會議室記得改密碼
        driver.find_element(By.NAME, "lockKey").send_keys("你自己會議室的password，不一定有")
        driver.find_element(By.CSS_SELECTOR, "#modal-dialog-ok-button > span").click()
    except:
        pass
    time.sleep(2)
    #這邊原本會關掉畫廊模式，但發現人數只要超過10人，沒有滾動名單列的話CLASS反而不完整
    # searchButtonElement = driver.find_element(By.ID,'localVideoContainer')
    # time.sleep(2)
    # ActionChains(driver).click(searchButtonElement).perform()
    # time.sleep(2)
    #把已在會議室內的全部名子抓出來
    namelist = driver.find_elements(By.CSS_SELECTOR, ".css-5bay1g-displayName")
    #只取每個名子最後兩個字(為了去找google點名的那個中文字)
    meetsName = []
    for n in namelist:
        strName = n.text
        meetsName.append(strName[-2:])
        print(strName[-2:])
    print(meetsName)

    time.sleep(2)
    #把selenium換去 google報到的頁面
    #這邊如果用其他的或要串其他的下面整個要換掉
    url = 'https://script.google.com/macros/.....'
    driver.get(url)
    #這邊因為前面有設定--headless 所以這行沒用，如果要看selenium實際操作畫面，把--headless那行註解掉。
    driver.set_window_size(1440, 1200)
    driver.implicitly_wait(5) # seconds
    #google有包iframe，直接抓會抓不到，要switch frame
    driver.switch_to.frame("sandboxFrame")
    driver.switch_to.frame("userHtmlFrame")
    a = driver.find_elements(By.CLASS_NAME, "card.ng-scope.checkin")
    b = driver.find_elements(By.CLASS_NAME, "card.ng-scope")

    # 這邊就把上面拿到的名子，去找到按鈕後 點報到
    
    for j in b:
        checkin = 'n'
        for i in a:
            if(j.text == i.text):
                checkin = 'y'
            continue
        if(checkin == 'n'):
            if(j.text in meetsName):
                print(b.index(j))  
                print(j.text)    
                b[b.index(j)].click()
                try:
                    # 報到會跳alert 造成阻塞，這邊是等alert跳出來把他點掉。
                    # 使用WebDriverWait等待alert出現，最多等待4秒
                    alert = WebDriverWait(driver, 4).until(EC.alert_is_present())
                    time.sleep(1)
                    # 接著按下OK按鈕
                    alert.accept()
                except:
                    pass

    time.sleep(2)  
try:
    #就排程，可自己隨意設定
    # 每(n)秒/分/時/天/週執行(job)
    schedule.every().day.at('08:27').do(job)
    while True:
        schedule.run_pending()
        time.sleep(5)

    #測試    
    # job()
except Exception as e: 
    print(e)
```

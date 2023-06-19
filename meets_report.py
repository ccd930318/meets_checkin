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
    url = 'https://meet.jit.si/ecscdpmeet_1qaD3k9Fk3_'
    driver.get(url)
    driver.set_window_size(1440, 1200)
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, ".css-hh0z88-input").click()
    driver.find_element(By.CSS_SELECTOR, ".css-hh0z88-input").send_keys('點名機器人')
    driver.find_element(By.CSS_SELECTOR, ".css-1hbmoh1-actionButton").click()
    try:
        time.sleep(1)
        driver.find_element(By.NAME, "lockKey").click()
        driver.find_element(By.NAME, "lockKey").send_keys("在這打上會議密碼")
        driver.find_element(By.CSS_SELECTOR, "#modal-dialog-ok-button > span").click()
    except:
        pass
    time.sleep(2)
    #這邊原本會關掉畫廊模式，但發現人數只要超過10人，沒有滾動名單列的話CLASS反而不完整
    # searchButtonElement = driver.find_element(By.ID,'localVideoContainer')
    # time.sleep(2)
    # ActionChains(driver).click(searchButtonElement).perform()
    # time.sleep(2)
    
    # print(namelist)
    namelist = driver.find_elements(By.CSS_SELECTOR, ".css-5bay1g-displayName")

    meetsName = []
    for n in namelist:
        strName = n.text
        meetsName.append(strName[-2:])
        print(strName[-2:])
    print(meetsName)

    time.sleep(2)

    url = 'https://script.google.com/macros/s/AKfycbyD1bEgI__cNXt-3cqGcNLy2H72HKpBWpuSAKv-yYVCr4E8dlGtUsvksDn1eJJDuD3u/exec'
    driver.get(url)
    driver.set_window_size(1440, 1200)
    driver.implicitly_wait(5) # seconds
    driver.switch_to.frame("sandboxFrame")
    driver.switch_to.frame("userHtmlFrame")
    a = driver.find_elements(By.CLASS_NAME, "card.ng-scope.checkin")
    b = driver.find_elements(By.CLASS_NAME, "card.ng-scope")

    # for i in a:
    #   print(i.text)
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
                    # 使用WebDriverWait等待alert出現，最多等待4秒
                    alert = WebDriverWait(driver, 4).until(EC.alert_is_present())
                    time.sleep(1)
                    # 接著按下OK按鈕
                    alert.accept()
                except:
                    pass

    time.sleep(2)  
try:
    # 每(n)秒/分/時/天/週執行(job)
    schedule.every().day.at('08:27').do(job)
    schedule.every().day.at('08:28').do(job)
    schedule.every().day.at('08:29').do(job)
    schedule.every().day.at('08:30').do(job)
    schedule.every().day.at('08:31').do(job)
    schedule.every().day.at('08:32').do(job)
    schedule.every().day.at('08:33').do(job)
    schedule.every().day.at('08:34').do(job)
    schedule.every().day.at('08:35').do(job)
    schedule.every().day.at('08:36').do(job)
    schedule.every().day.at('08:37').do(job)
    schedule.every().day.at('08:38').do(job)
    while True:
        schedule.run_pending()
        time.sleep(5)

    #測試    
    # job()
except Exception as e: 
    print(e)


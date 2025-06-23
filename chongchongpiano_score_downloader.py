# -*- coding: utf-8 -*-
# author: haroldchen0414

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import base64
import requests
import time
import os

class ScoreDownloader:
    def __init__(self):
        self.chromeOptions = Options()
        self.chromeOptions.add_argument("--headless")
        self.chromeOptions.add_argument("--no-sandbox")
        self.chromeOptions.add_argument("--window-size=1920,1080")
        self.chromeOptions.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36")
        os.makedirs("output", exist_ok=True)

    def collect_url(self, link):
        try:
            response = requests.get(link)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            iframe = soup.find("iframe", id="ai-score")

            if iframe and "src" in iframe.attrs:
                return iframe["src"]
            
            else:
                return None
        
        except requests.exceptions.RequestException as e:
            print("请求错误: {}".format(e))
            return None

    # model=0获取五线谱, mode=1获取简谱
    def save_score(self, link, mode=0):
        url = "https://www.gangqinpu.com" + self.collect_url(link)
        print("正在获取乐谱: {}".format(url))
        
        # 获取简谱
        if mode == 1:
            url = url.replace("jianpuMode=0", "jianpuMode=1")
        try:
            driver = webdriver.Chrome(service=Service(executable_path=r"D:\new\software\Python\chromedriver.exe"), options=self.chromeOptions)
            driver.get(url)
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "body")))
            # 不运行该script页面会显示空白
            script = """
            (function(){
                'use strict';
                !document.referrer && (location.href += "");
                document.querySelectorAll('.print').forEach(el => {
                    el.style.display = 'none';
                });
            })();
            """
            driver.execute_script(script)
            
            titleElement = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "text[text-anchor='middle']")))
            title = titleElement.text.strip()
            printOptions = {
                "paperWidth": 8.27,
                "paperHeight": 11.69,
                "marginTop": 0,
                "marginBottm": 0,
                "marginLeft": 0,
                "marginRight": 0,
                "printBackground": True,
                "landscape": False
            }

            # 等待5秒, 否则获取的pdf文件会有干扰
            time.sleep(5)
            data = driver.execute_cdp_cmd("Page.printToPDF", printOptions)
            
            if mode == 0:
                with open(os.path.join("output", (title + "_五线谱.pdf")), "wb") as f:
                    f.write(base64.b64decode(data["data"]))

                print("成功保存: {}_五线谱.pdf".format(title))

            if mode == 1:
                with open(os.path.join("output", (title + "_简谱.pdf")), "wb") as f:
                    f.write(base64.b64decode(data["data"]))

                print("成功保存: {}_简谱.pdf".format(title))
            
        except Exception as e:
            print("发生错误: {}".format(e))
        finally:
            driver.quit()

if __name__ == "__main__":
    downloader = ScoreDownloader()

    url = "https://www.gangqinpu.com/cchtml/1064375.htm"
    # 获取五线谱
    downloader.save_score(url)
    # 获取简谱
    downloader.save_score(url, mode=1)
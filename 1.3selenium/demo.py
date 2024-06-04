'''
python selenium  foresightnews
'''
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium.common.exceptions import NoSuchElementException
import json

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(options=options, service=service)

driver.get("https://foresightnews.pro/")

# 等待页面的JavaScript加载完成
WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "waterfall-column"))
)
print(driver.title)
# 等待3秒
sleep(3)

# 获取所有class为waterfall-column的元素
columns = driver.find_elements(By.CLASS_NAME, "topic-content")

# 准备一个列表来存储结果
results = []

# 遍历每个waterfall-column元素
for a_tag in columns:
    # 如果a标签存在，获取链接、标题和时间
    if a_tag:
        link = a_tag.get_attribute('href')  # 获取链接
        title = a_tag.find_element(By.CLASS_NAME, "topic-body-title").text  # 获取标题
        # 假设foot-tag是包含time的元素的class
        try:
            time = a_tag.find_element(By.CLASS_NAME, "topic-time").text  # 获取时间
        except NoSuchElementException:
            print("no topic tag")
            continue
        
        results.append({"link":link,"title":title,"time":time})

# 打印结果列表
# for result in results:
#     print(result)
print(json.dumps(results))

# 关闭浏览器
driver.quit()

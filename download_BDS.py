# -*- coding: utf-8 -*-
# date: 2020/7/19
# author: zhang.xd

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import re
import pandas as pd
from tqdm import tqdm

# 用户自定义需要下载数据的时间
input_ = "2020-001"

# 设置需要下载测站的文件路径
bds_stas_dir = 'MultiGNSS.xlsx'

# 用户名和密码
username = " "
password = " "

# 定义驱动相关参数
options = webdriver.ChromeOptions()
## 禁用下载弹窗， 设置下载路径
prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': 'd:\\'}
options.add_experimental_option('prefs', prefs)
# 无窗口运行
options.headless = True

# 设置浏览器驱动
driver = webdriver.Chrome(chrome_options=options)

def get_source_code(driver, username, password):
    driver.get("https://cddis.nasa.gov/archive/gnss/data/daily/")
    time.sleep(2)

    # 模拟登录
    print("[Info] logging in ...")
    driver.find_element_by_id("username").send_keys(username)
    driver.find_element_by_id("password").send_keys(password)
    driver.find_element_by_name("commit").click()
    print("[Info] Finish logging!")
    time.sleep(5)

    driver.find_element_by_id(input_[:4]).click()
    time.sleep(2)
    driver.find_element_by_id(input_[5:8]).click()
    time.sleep(2)
    driver.find_element_by_id(input_[2:4] + "d").click()
    time.sleep(2)

    source = driver.page_source

    return source


def load_bds_sta(source, bds_stas_dir):
    # 通过正则表达式匹配网页源码中的站点数据压缩包名称
    pattern = re.compile('<a.*?id="(.*?)"\stitle="DataFile"')
    items = re.findall(pattern, source)
    # 读取需要下载数据的站点名称；仅读取第一列,即站名
    df = pd.read_excel(bds_stas_dir, sheet_name='BDS', usecols=[0])
    # df.values为 numpy数组
    df_sta = df.values.tolist()
    bds_sta_names = []
    for sta in df_sta:
        bds_sta_names.append(sta[0])

    # 匹配一下需要下载的站点和网站中提供下载的站点，提取能够下载的站点数据压缩包名称
    download_stas = []
    for item in items:
        if item[:9] in bds_sta_names:
            download_stas.append(item)

    return download_stas

if __name__ == '__main__':
    source = get_source_code(driver, username, password)
    download_stas = load_bds_sta(source, bds_stas_dir)
    # 遍历下载
    print("[Info] Downloading...")
    for id in tqdm(download_stas):
        driver.find_element_by_id(id).click()
        time.sleep(1)

    print("[Info] Finish!")
    driver.close()




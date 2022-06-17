# import linkGetter_version_desktop_requests
# linkGetter_version_desktop_requests.MainLinkGetter()
# https://anilist.co/search/anime/top-100
# div.data-v-9a20c1b0 class.results cover

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome('C:\\Users\\selcukemre\\Desktop\\chromedriver.exe', options=chrome_options)
driver.get('https://www.google.com')

print(driver.page_source)



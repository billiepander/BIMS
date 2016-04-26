#coding:utf-8
# from selenium import webdriver
# from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.common.keys import Keys
# import time
#
# browser = webdriver.Chrome() # Get local session of firefox
# browser.get("http://www.yahoo.com") # Load page
# # assert "Yahoo!" in browser.title
# # elem = browser.find_element_by_name("p") # Find the query box
# # elem.send_keys("seleniumhq" + Keys.RETURN)
# # time.sleep(0.2) # Let the page load, will be added to the API
# # try:
# #     browser.find_element_by_xpath("//a[contains(@href,'http://seleniumhq.org')]")
# # except NoSuchElementException:
# #     assert 0, "can't find seleniumhq"
# browser.close()


from selenium import webdriver

driver = webdriver.Chrome()

driver.get(r'http://map.baidu.com/')
print driver.title
# <input id="sole-input" class="searchbox-content-common" type="text" name="word" autocomplete="off" maxlength="256" placeholder="搜地点、查公交、找路线" value="">
sousuo = driver.find_element_by_id('sole-input')
sousuo.send_keys(u'西直门桥')
# <button id="search-button" data-title="搜索" data-tooltip="1"></button>
clicli = driver.find_element_by_id('search-button')
clicli.click()
print(driver.current_url)
# driver.quit()

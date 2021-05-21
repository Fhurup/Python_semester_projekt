from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from datetime import date
import pandas as pd

today = date.today()
file_name = "../data/links_scr.csv"

data = pd.read_csv(file_name)


def _connect(link):

    """opens page and clicks on the cookie button.
    Returns a webdriver"""

    base_url = link
    profile = webdriver.FirefoxProfile()
    profile.set_preference(
        "general.useragent.override",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0",
    )

    # headless would be needed here if we did not have a GUI version of firefox
    options = Options()
    options.headless = True

    browser = webdriver.Firefox(options=options)

    browser.get(base_url)
    browser.implicitly_wait(3)

    try:
        cookie_button = browser.find_element_by_id("onetrust-accept-btn-handler")
        try:
            cookie_button.click()
            sleep(3)
            return browser
        except Exception as ex:
            print(ex)
    except Exception as e:
        print("BUTTON EXCEPTION", e)





def scrap_one_car(link):
    car={}
    browser=_connect(link)
    price_span= browser.find_element_by_class_name('price-tag')
    try:
        price=price_span.text.replace("kr.","").strip().replace(".","")
        car["price"]=price


    except Exception as e:
        print("something went wrong... ", e)
        return None

init_link='https://www.biltorvet.dk/bil/alfa-romeo/mito/1-3-jtdm-distinctive-85hk-3d/1772499'
scrap_one_car()
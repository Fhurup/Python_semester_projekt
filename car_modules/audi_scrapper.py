import pandas as pd
import re
from time import sleep

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys


def extract_audi():

    all_cars = pd.read_csv("./bil_torvet/bil_torvet_data.csv", sep=";", header=None)
    all_cars = pd.DataFrame(all_cars)
    all_cars = all_cars.sort_values([0])
    all_cars[1500:1550]
    r = re.compile(r"(Audi).*")
    audi = all_cars[all_cars[0].apply(lambda x: bool(r.match(x)))]
    audi.to_csv("./bil_torvet/audi_links.csv", sep=";", header=None, index=False)


def audi_links():
    audi = pd.read_csv("./bil_torvet/audi_links.csv", sep=";", header=None)
    return audi[5]


def connect(link):

    """opens page and clicks on the cookie button.
    Returns a webdriver"""

    profile = webdriver.FirefoxProfile()
    profile.set_preference(
        "general.useragent.override",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:81.0) Gecko/20100101 Firefox/81.0",
    )

    # headless would be needed here if we did not have a GUI version of firefox
    options = Options()
    options.headless = True

    browser = webdriver.Firefox(options=options)

    browser.get(link)
    browser.implicitly_wait(3)

    error_div = browser.find_elements_by_css_selector("div.error__component")
    if len(list(error_div)) > 0:
        raise Exception("Page not found")
    else:

        try:
            cookie_button = browser.find_element_by_class_name("coi-banner__accept")
            try:
                cookie_button.click()
                sleep(3)
                return browser
            except Exception as ex:
                print(ex)
        except Exception as e:
            print("BUTTON EXCEPTION", e)
            raise e


def get_fuel_door(browser):

    try:
        fuel = browser.find_element_by_xpath(
            "//div[contains(text(), 'Brændstof')]/following-sibling::div"
        )

        door = browser.find_element_by_xpath(
            "//div[contains(text(), 'Antal døre')]/following-sibling::div"
        )
       
        return [fuel.text, door.text.strip().split(" ")[0]]
    except Exception as e:
        print("fuel exception", e)
        raise e


def collect_data():
    audi = pd.read_csv("../bil_torvet/audi_links.csv", sep=";", header=None)
    links = audi[5]
    counter=1
    for link in links:
        door = None
        fuel = None
        browser = None
        
        try:

            browser = connect(link)
            fuel, door = get_fuel_door(browser)
            
        except Exception as e:
            print("No data scrapped... ", e)
        car = {"link": link, "fuel": fuel, "door": door}
        df=pd.DataFrame([car])
        df.to_csv(path_or_buf="../bil_torvet/audi_fuel_door.csv", sep=";", mode="a", header=None, index=False)
        print(counter)
        counter+=1
    browser.close()

collect_data()

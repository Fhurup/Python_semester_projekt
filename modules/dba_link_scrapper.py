from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from datetime import date
import pandas as pd


today = date.today()


def _connect():

    """opens page and clicks on the cookie button.
    Returns a webdriver"""

    base_url = "https://www.dba.dk/biler/biler/"
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


def _validate_car_data(car):
    """check if car is possibly in leasing or if author provideed invalide data.
    Returns a link to the page with possibly valid car
    """

    result=""

    link = ""
    tds = list(car.find_elements_by_css_selector("td"))

    try:
        link = tds[1].find_element_by_css_selector("a").get_attribute("href")
    except Exception as e:
        print("Link not found... ", e)

    try:
        km = int(tds[2].text.strip().replace(".", ""))

    except ValueError as e:
        km = 0
    try:
        year = int(tds[3].text.strip())

    except ValueError as e:
        year = 0

    try:
        price = tds[5].text.strip().split(" ")
        price = int(price[0].replace(".", ""))

    except ValueError as e:
        price = 0

    if km < 2 or year < 1000 or price < 2000:
        link = ""

    if year > 2010 and price < 10000:
        link = ""

    return link


def _read_valid_data_on_current_page(browser, link_list):
    """Reads ellements representing cars in the browser
    Validates each element
    Adds valid links to the list of links"""

    file_name = "data/car_links.csv"

    try:
        car_elements = browser.find_elements_by_xpath(
            "//tr[contains(@class, 'dbaListing listing')]"
        )
        car_elements = list(car_elements)

    except Exception as e:
        print("No car elements fund... ", e)

    for car in car_elements:
        link = _validate_car_data(car)
        if link != "":
            link_list.append(link)
            link_df = pd.DataFrame([{"added": today, "link": link, "scrapped": False}])
            link_df.to_csv(
                path_or_buf=file_name, sep=";", mode="a", header=False, index=False
            )


def _read_all_pages(browser):
    links = []

    for i in range(1, 100):

        _read_valid_data_on_current_page(browser=browser, link_list=links)
    try:

        next_page_btn = browser.find_element_by_xpath(
            "//span[@data-ga-lbl='paging-next']"
        )
        next_page_btn.click()
    except Exception as e:
        print("could not click on 'next'... ", e)

    return links


def sort_by_date(browser):
    try:
        sort_tab = browser.find_element_by_class_name("sorting")
        sort_options = sort_tab.find_elements_by_css_selector("th")
        date_btn = sort_options[4]
        date_btn.click()

    except Exception as e:
        print("Could not click on Sotring", e)


def run():
    """
    open brwser
    locate tabs of private and comercial annonces
    create list of links for each tab
    for each tab read valid links on each page

    """
    browser = _connect()
    # sort_by_date(browser)

    # print(browser.current_url)
    links = _read_all_pages(browser)

    print("links: ", len(links))

    # return links


# def _locate_tabs(browser):
#     try:
#         tab_list = browser.find_elements_by_xpath("//ul[@class='left tabs160']/li")
#         return tuple(tab_list)

#     except Exception as e:
#         print("TAB EXCEPTION", e)


# def _read_all_pages(browser,tab):
#     links=[]
#     try:
#         tab.click()
#     except Exception as e:
#         print("Could not click on tab ", e)
#         raise Exception("Could not click on tab ")

#     for i in range(1, 100):

#         _read_valid_data_on_current_page(browser=browser, link_list=links)
#     try:

#         next_page_btn = browser.find_element_by_xpath(
#             "//span[@data-ga-lbl='paging-next']"
#         )
#         next_page_btn.click()
#     except Exception as e:
#         print("could not click on 'next'... ", e)

#     return links

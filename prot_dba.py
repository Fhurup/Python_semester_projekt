
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.options import Options



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

tabs = ()

private_links = []
commercial_links = []


def accept_cookies():
    try:
        cookie_button = browser.find_element_by_id("onetrust-accept-btn-handler")
        try:
            cookie_button.click()
            sleep(3)
        except Exception as ex:
            print(ex)
    except Exception as e:
        print("BUTTON EXCEPTION", e)


def get_car_elements():
    try:
        # car_elements=browser.find_elements_by_class_name("dbaListing listing boldListing hasInsertionFee topListing")

        car_elements = browser.find_elements_by_xpath(
            "//tr[contains(@class, 'dbaListing listing')]"

        )

    except Exception as e:
        print("No car elements fund... ", e)

    for car in car_elements:

        try:
            km = car.find_element_by_xpath('//td[@title="Km"]')
        except Exception as e:
            print("No Km fund... ", e)

        try:
            year = car.find_element_by_xpath('//td[@title="Modelår"]')
        except Exception as e:
            print("No Year fund... ", e)

        try:
            price = car.find_element_by_xpath('//td[@title="Pris"]')
        except Exception as e:
            print("No price fund... ", e)

        print(km.text, "\n", year.text, price.text)


def validate_car_data(car):
        try:
            km = car.find_element_by_xpath('//td[@title="Km"]')
            year = car.find_element_by_xpath('//td[@title="Modelår"]')
            price = car.find_element_by_xpath('//td[@title="Pris"]')
        except Exception as e:
            print("No Km,year or price fund... ", e)

        

        print(km.text, "\n", year.text, price.text)


def read_links_on_page():
    try:
        car_direct_links = browser.find_elements_by_class_name("listingLink")
        try:
            for c in car_direct_links:
                href = c.get_attribute("href")
                # print(type(href))
                private_links.append(href)
        except Exception as e:
            print("Could not get attribute href, ", e)

    except Exception as e:
        print("couldn't find any links", e)


def get_links(tab):
    try:
        tab.click()
    except Exception as e:
        print("Could not click on tab ", e)

    read_links_on_page()

    for i in range(1, 100):
        print(i, "\n")
        try:

            next_page_btn = browser.find_element_by_xpath(
                "//span[@data-ga-lbl='paging-next']"
            )

            read_links_on_page()
            next_page_btn.click()
        except Exception as e:
            print("could not click on 'next'... ", e)


def run():
    accept_cookies()

    try:
        tab_list = browser.find_elements_by_xpath("//ul[@class='left tabs160']/li")
        tabs = tuple(tab_list)
    except Exception as e:
        print("TAB EXCEPTION", e)

    private_tab = tabs[1]

    # get_links(private_tab)
    get_car_elements()


run()
print(len(private_links))

from time import sleep
from warnings import catch_warnings
from numpy.core.numeric import NaN
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys 

from datetime import date
import pandas as pd

today = date.today()

base_url="https://www.biltorvet.dk/"
scrapped=['Abarth',
 'Adria',
 'Alfa Romeo',
 'Alpina',
 'Aston Martin',
 'Audi',
 'Austin',
 'Bentley',
 'BMW',
 'Buick',
 'Cadillac',
 'Chevrolet',
 'Chrysler',
 'Citroën',
 'Cupra',
 'Dacia',
 'Daewoo',
 'DAF',
 'Daihatsu',
 'Daimler',
 'Datsun',
 'Dodge',
 'DS',
 'Ferrari',
 'Fiat',]
all_makes=[
 'Ford',
 'Heinkel',
 'Hillman',
 'Honda',
 'Hummer',
 'Hyundai',
 'Infiniti',
 'Isuzu',
 'Jaguar',
 'Jeep',
 'Kia',
 'KTM',
 'Lada',
 'Lamborghini',
 'Lancia',
 'Land Rover',
 'Lexus',
 'Lotus',
 'MAN',
 'Maserati',
 'Maxus',
 'Mazda',
 'McLaren',
 'Mercedes-Benz',
 'Mercury',
 'Messerschmidt',
 'MG',
 'Mini',
 'Mitsubishi',
 'Morgan',
 'Morris',
 'Nissan',
 'NSU',
 'Opel',
 'Peugeot',
 'Plymouth',
 'Polaris',
 'Polestar',
 'Pontiac',
 'Porsche',
 'Renault',
 'Rolls-Royce',
 'Rover',
 'Royal',
 'Seat',
 'Skoda',
 'Smart',
 'SsangYong',
 'Subaru',
 'Sunbeam',
 'Sunbeam Talbot',
 'Suzuki',
 'Saab',
 'Tesla',
 'Toyota',
 'Trabant',
 'Triumph',
 'Volvo',
 'VW',
 'Watercar']

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


def load_all_results_on_one_page(browser):

    try:
        no_results=browser.find_element_by_xpath("//p[contains(text(), 'Ingen resultater blev fundet')]")
    
        return
    except Exception as e:
    
  
        
        stop=0
        count=0
        while(stop==0):
            try:
                load_more=browser.find_element_by_class_name("search-results__button.button.button--highlight")

                count+=1
                browser.find_element_by_tag_name('body').send_keys(Keys.END)
                
                print(count)
                load_more.click()
            except Exception as e:
                stop=2
                print("Load  more exception: ", e)
                browser.save_screenshot("../data/load_more_exc.png")




def select_price(browser):
    
    price_p = browser.find_element_by_xpath("//p[contains(text(), 'Pris')]")
    price_div = price_p.find_element_by_xpath("../.")
    
    price_div.click()
    print("Price menu clicked")
    sleep(3)

    kontant_span=browser.find_element_by_xpath('//span[contains(text(), "Kontant")]')
    div_span=kontant_span.find_element_by_xpath("../../../.")
    # print(div_span.get_attribute('class'))
    div_span.click()
   
    price_div.click()
    print("Price set")

def find_makes(browser):
    make_p = browser.find_element_by_xpath("//p[contains(text(), 'Mærke')]")
    
    make_div = make_p.find_element_by_xpath("../.")
    
    make_div.click()
    browser.save_screenshot('./data/makecontainer.png')
    make_elements=list(browser.find_elements_by_name("MakeId"))
   
    return make_elements

def search_by_make(browser, make):
    #pase make to the input field
    browser.find_element_by_id("textSearch_input").send_keys(make)
    browser.save_screenshot("../data/1_pastedMake.png")
    print("make set")
    sleep(3)
    


def search(browser):
    
    search=browser.find_element_by_class_name("button.button--highlight.advanced-search__button")
    search.click()
    print("search clisked")

    sleep(3)

    


def scrap_results(browser, file):    
    car_elements=browser.find_elements_by_class_name("card-ad-results__result.card-ad-results__result--default-view")

    print("in scrap_result") 
    for element in list(car_elements):
    
        href=element.find_element_by_css_selector("a").get_attribute("href")
        # print("link: ", href)
        price=element.find_element_by_css_selector("p.card__price.card__text--lg.font-semibold").text.replace("kr.","").strip().replace(".","")
        # print('price ',price)
        model= element.find_element_by_css_selector ("div.card__text.card__text--sm.card__text--bounds.font-semibold").text
        # print("modl: ", model)
        details=list(element.find_elements_by_css_selector ("div.card-details__text.card__text--sm"))
        location=details[0].text
        # print("loc: ",location)
        km=details[1].text
        # print('km ',km)
        year=details[2].text.strip()[-1:-5:-1][-1:-5:-1]
        # print('yaer: ',year)

        car={'model':model,'price':price,'km':km,'location':location, "year":year, 'link':href}
        print (car)
        df=pd.DataFrame([car])
        df.to_csv(path_or_buf=file, sep=";", mode="a", header=None, index=False)


file_name = "../bil_torvet/bil_torvet_data.csv"
for make in all_makes:
    
    browser=connect(base_url)
    select_price(browser)
    search_by_make(browser,make)
   
    search(browser)
    load_all_results_on_one_page(browser)
    scrap_results(browser,file_name)

    print("Make: ", make, " scrapped!")


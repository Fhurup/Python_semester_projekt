import pandas as pd
import re
from . import audi_scrapper
def extract_audi():
    all_cars= pd.read_csv("./bil_torvet/bil_torvet_data.csv",sep=";", header=None)
    all_cars=pd.DataFrame(all_cars)
    all_cars=all_cars.sort_values([0])
    all_cars[1500:1550]
    r=re.compile(r'(Audi).*')
    audi=all_cars[all_cars[0].apply(lambda x: bool(r.match(x)))]
    audi.to_csv("./bil_torvet/audi_links.csv",sep=";", header=None, index=False)

def audi_links():
    audi=pd.read_csv("./bil_torvet/audi_links.csv",sep=";",header=None)


connection = audi_scrapper.connection()
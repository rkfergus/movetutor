import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import numpy as np
import chromedriver_binary
from bs4 import BeautifulSoup
import datetime as datetime


def getLink(lst):
    lst = lst.split(r'"')
    if len(lst) > 1:
        return lst[1]
    else:
        return np.NaN


options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

driver.get(r'https://www.serebii.net/attackdex-sm/')

soup_level1 = BeautifulSoup(driver.page_source, 'lxml')
option_vals = pd.Series(soup_level1.find_all('option'))
split = option_vals.apply(lambda x: str(x).split('>'))

moves_master = pd.DataFrame(columns=['Move', 'Link'])
moves_master['Link'] = split.apply(lambda x: getLink(x[0]))
moves_master['Move'] = split.apply(lambda x: x[1].split('<')[0])

print(moves_master.dropna(inplace=True))


def getPokemon(x):
    print(x)
    driver.get(r'https://www.serebii.net' + x)
    mons = list()
    tables = BeautifulSoup(driver.page_source, 'lxml').find_all('table')
    for tb in tables:
        if 'pkmn' in str(tb):
            lines = str(tb).splitlines()
            for line in lines:
                if 'pokedex' in line:
                    if 'pkmn' not in line:
                        if 'img' not in line:
                            mons.append(line.split('</')[0].split('>')[-1])
    return pd.Series(mons).drop_duplicates().tolist()


moves_master['Pokemon'] = moves_master['Link'].apply(lambda x: getPokemon(x))
driver.close()

moves_master.to_csv('latest.csv'.format(str(datetime.datetime.now())))

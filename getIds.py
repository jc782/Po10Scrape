import requests
from bs4 import BeautifulSoup
import collections as co
import pandas as pd

URL = 'https://www.thepowerof10.info/athletes/athleteslookup.aspx?surname=&firstname=&club=thames+hare'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')
table = soup.find(id='cphBody_dgAthletes')
dfs = pd.read_html(str(table))
df = dfs[0]
df.rename(columns=df.iloc[0], inplace=True)
df.drop(df.index[0], inplace = True)
names = df[['First','Surname']] 
print(names)

links = []
for tr in table.findAll("tr"):
    trs = tr.findAll("td")
    for each in trs:
        try:
            link = each.find('a')['href']
            links.append(link)
        except:
            pass

ids = []
discardString = "runbritain"
for link in links:
    if discardString in link:
        print('run britain link')    
    else:
        split_string = link.split("=", 1)
        ids.append(split_string[1])

names['ID'] = ids 
names.to_csv("./ThamesIds.csv", sep=',',index=False)


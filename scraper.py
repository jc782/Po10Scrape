import requests
from bs4 import BeautifulSoup
import collections as co
import pandas as pd
import csv
import time


# Open up the list of ids to loop through. Can be generated using the getids script
with open('ThamesIds.csv', newline='') as f:
    reader = csv.reader(f)
    thamesIds = list(reader)

# remove the header from the ids
thamesIds.pop(0)

# loop through and grab the pbs for each person. Downselect the table to just the PB column (this could be changed to the year columns for a yearly ranking)
data=pd.DataFrame()
for id in thamesIds:
    try:
        firstname = id[0]
        surname =  id[1]
        URL = 'https://thepowerof10.info/athletes/profile.aspx?athleteid=' + id[2]
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find(id='cphBody_divBestPerformances')
        table  = results.find('table')
        dfs = pd.read_html(str(table))
        df = dfs[0]
        df.rename(columns=df.iloc[0], inplace=True)
        df.drop(df.index[0], inplace = True)
        df = df[['Event', 'PB']]
        df = df.loc[:,~df.columns.duplicated()]
        df['Name'] = id[0] +" " + id[1]
        df['id'] = id[2]
        data = data.append(df,ignore_index=True)
        time.sleep(0.5)
        print('got pbs for ' + id[0] + id[1])
    except:
        print("Likely has no pbs")
    

# reshape the data to the format we want
data = data.drop_duplicates()
newf = pd.pivot_table(data, index =['id','Name'], columns='Event',  aggfunc='first') 

# save csv
newf.to_csv("./ThamesPBs.csv", sep=',',index=True)


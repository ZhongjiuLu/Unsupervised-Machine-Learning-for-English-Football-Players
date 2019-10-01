# importing python libraries and packages to help us manipulate the data. 
# Packages: 
#pandas (data manipulation and analysis)
#beautifulsoup (pulling data from HTML and XML files)
#re (regular expression)
import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
import unicodedata

# Create a list named "attributes" 
attributes=['Crossing','Finishing','Heading accuracy',
 'Short passing','Volleys','Dribbling','Curve',
 'Free kick accuracy','Long passing','Ball control','Acceleration',
 'Sprint speed','Agility','Reactions','Balance',
 'Shot power','Jumping','Stamina','Strength',
 'Long shots','Aggression','Interceptions','Positioning',
 'Vision','Penalties','Composure','Marking',
 'Standing tackle','Sliding tackle','GK diving',
 'GK handling','GK kicking','GK positioning','GK reflexes']

# generate a empty list to store the future pulled links from websites.
links=[]   #get all argentinian players

# pull 500 English players in 5 consecutive pages of 100 entries each
for offset in ['0','80','160','320','400','480']:
    # requests the page with a new list of players
    page=requests.get('http://sofifa.com/players?na=14&offset='+offset) 
    # parse the data with html.parser
    soup=BeautifulSoup(page.content,'html.parser')
    # It goes through all the links of the page (not only players' URLs) and saves them in the links array
    for link in soup.find_all('a'):
        links.append(link.get('href'))

#We had all the links of the page stored in links. We re-create links adding the links that have
#'player/' in the url. This is to get the players' URLs only.
links=['http://sofifa.com'+l for l in links if 'player/'in l] 

print(len(links))

#pattern regular expression. We added '\-' and '\'' so that it accepts names as "Oxlade-Chamberlain" or "I'Anson"
pattern=r"""\s*([\w\s\-\']*?)\s*FIFA"""   #file starts with empty spaces... players name...FIFA...other stuff     
for attr in attributes:
    pattern+=r""".*?(\d*\s*"""+attr+r""")"""  #for each attribute we have other stuff..number..attribute..other stuff

pat=re.compile(pattern, re.DOTALL)    #parsing multiline text

#empty array that will later on store every single player's link, name and attributes
rows=[]

#removes the first 10 links from links
links=links[10:]
for j,link in enumerate(links):
    #prints the index and the player's link
    print (j,link)
    row=[link]
    #requests the player's page
    playerpage=requests.get(link)
    playersoup=BeautifulSoup(playerpage.content,'html.parser')
    #gets all the html text from the player's website
    text=playersoup.get_text()
    #Normalise (normalize) unicode data in Python to remove special characters
    text=unicodedata.normalize('NFKD', text).encode('ascii','ignore')
    a=pat.match(text.decode('utf-8'))
    #print(a)
    #adds the player's name to 'row'
    row.append(a.group(1))
    #To each player, it now starts adding every single value for each attribute (e.g. 77 for crossing)
    for i in range(2,len(attributes)+2):
        row.append(int(a.group(i).split()[0]))
    rows.append(row)
    #It prints the the player's name
    print (row[1])

#adds the the columns for the CSV
df=pd.DataFrame(rows,columns=['link','name']+attributes)

#adds the data to the csv
df.to_csv('EnglishPlayers.csv',index=False)





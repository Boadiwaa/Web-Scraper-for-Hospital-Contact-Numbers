import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import openpyxl
from geopy.geocoders import Nominatim

website = 'http://www.ghanahospitals.org/regions/regionlist.php?sel=ownership&page=government&r=ashanti'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}

result = requests.get(website, headers = headers)
content = result.text
soup = BeautifulSoup(content, 'lxml')

print(soup.prettify())

links = []
names = []
listing_divs = soup.find_all('div', class_='listing')
for listing_div in listing_divs:
    link = listing_div.find('a').get('href')
    text = listing_div.find('a').get_text()
    links.append(link)
    names.append(text)

print(links)
print(names)


root = 'http://www.ghanahospitals.org/regions'
links2 = []
#contentcheck = []
for link in links:
    result = requests.get(f'{root}/{link}', headers =headers)
    content = result.text
    soup = BeautifulSoup(content, 'lxml')
    pages_data = soup.select('.fdtails_home')[0].get_text()
    #contentcheck.append(pages_data)
    pattern = r'Tel:.+' 
    tel_match = re.search(pattern, pages_data)
    if tel_match:
        links2.append(tel_match.group()) 
    else:
        pass
    
df = pd.DataFrame({'Names': names, 'Contacts': links2})
df.to_excel('contacts_py.xlsx', index=False)

# Not related to the section above, different Excel sheet involving a bigger dataset. The following code is for geolocation of the 
#list of hospitals scraped.

hospitalsall = pd.read_excel("C:\\Users\\pauli\\Desktop\\R_work\\contacts.xlsx")

lat =[]
long = []
# Example hospital in Accra
geolocator = Nominatim(user_agent="my-app")
for i in hospitalsall['search']:
    try:
        location = geolocator.geocode(i) 
    except:
        pass
    if location == None:
        lat.append("NA")
        long.append("NA")
    else:
        lat.append(location.latitude)
        long.append(location.longitude)
hospitalsall['latitude'] = lat
hospitalsall['longitude'] = long
hospitalsall.to_excel("C:\\Users\\pauli\\Desktop\\hospitalsall.xlsx", index=False)

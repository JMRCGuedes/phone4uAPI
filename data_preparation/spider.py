import pandas as pd
# importing the csv module
import csv

df = pd.read_csv('./phones_data.csv')

brands = df['brand_name']
models = df['model_name']
phones = []

for i in range(0, brands.size):
  phones.append(brands[i] + ' ' + models[i])
print(phones)

# FETCH DOS URLS DOS TELEMOVEIS ATRAVEZ DO SEU NOME E GUARDAR NUM FICHEIRO CSV

#pip install scrapy

#pip install crochet

""" import requests

base_url = 'https://www.devicespecifications.com/index.php?action=search&language=en&search='
urls_array = []

for phone in phones:
  url = base_url + phone
  x = requests.get(url)
  response = x.json()
  print("Request done, status: ", x.status_code)
  try:
    urls_array.append(response[0]['url'])
  except:
    urls_array.append(None)

print(urls_array)




 
file_obj = []

for url in urls_array:
  file_obj.append({'link': url})

 
# field names
fields = ['link']
 
# name of csv file
filename = "phoneUrls.csv"
 
# writing to csv file
with open(filename, 'w') as csvfile:
    # creating a csv dict writer object
    writer = csv.DictWriter(csvfile, fieldnames=fields)
 
    # writing headers (field names)
    writer.writeheader()
 
    # writing data rows
    writer.writerows(file_obj)

 """

# TRATAMENTO DOS DADOS

df = pd.read_csv('./phoneUrls.csv')

urls_array = df['link']



""" from lxml import etree
from io import StringIO
import requests

# Set explicit HTMLParser
parser = etree.HTMLParser()

page = requests.get(urls_array[0])

# Decode the page content from bytes to string
html = page.content.decode("utf-8")

# Create your etree with a StringIO object which functions similarly
# to a fileHandler
tree = etree.parse(StringIO(html), parser=parser)

response = tree.xpath('//*[@id="model-brief-specifications"]//b/@text')
for resp in response:
  print(resp)

print(response) """







import requests
from bs4 import BeautifulSoup
import pandas as pd

# pip install zenrows
from zenrows import ZenRowsClient

client = ZenRowsClient("98f9737ef5f4748d2ab1f9102642bad9408c7f6f")

final_data = pd.read_csv('./phone_final_data.csv')


def get_phone_data(url):
  if url not in final_data['url'].values:
    dimensions = None
    weight = None
    ram = None
    storage = None
    display = None
    camera = None
    wifi = None
    usb = None
    blue = None
    cpu = None
    gpu = None
    battery = None

    if pd.notna(url):

      response = client.get(url)

      #print(response.content)

      #response = requests.get(url, proxies=proxies)
      soup = BeautifulSoup(response.content, 'html.parser')

      quote = soup.find('div', {'id': 'model-brief-specifications'}).get_text(separator='=>', strip=True)

      specs_array = quote.split('=>')
      specs_array_size = len(specs_array)

      for i in range(0,int(specs_array_size),2):
        if ': ' not in specs_array[i+1]:
          continue

        value = specs_array[i+1].split(': ')[1] if len(specs_array[i+1]) > 0 else None
        spec = specs_array[i]
        if 'Dimensions' in spec:
          dimensions = specs_array[i+1].split(': ')[1]
          continue;
        if 'CPU' in spec:
          cpu = value
          continue;
        if 'GPU' in spec:
          gpu = value
          continue;
        if 'Weight' in spec:
          weight = value
          continue;
        if 'RAM' in spec:
          ram = value
          continue;
        if 'Storage' in spec:
          storage = value
          continue;
        if 'Display' in spec:
          display = value
          continue;
        if 'Camera' in spec:
          camera = value
          continue;
        if 'Wi-Fi' in spec:
          wifi = value
          continue;
        if 'USB' in spec:
          usb = value
          continue;
        if 'Bluetooth' in spec:
          blue = value
          continue;
        if 'Battery' in spec:
          battery = value
          continue;

    file_obj.append({
      'dimensions': dimensions,
      'cpu': cpu,
      'gpu': gpu,
      'weight':weight,
      'ram':ram,
      'storage':storage,
      'display':display,
      'camera':camera,
      'wifi':wifi,
      'usb':usb,
      'blue':blue,
      'battery':battery,
      'url': url
    })

    with open("phone_final_data.csv", 'w', encoding="utf-8") as csvfile:
      # creating a csv dict writer object
      writer = csv.DictWriter(csvfile, fieldnames=fields)
  
      # writing headers (field names)
      writer.writeheader()
  
      # writing data rows
      writer.writerows(file_obj)



file_obj = []
fields = ['dimensions', 'cpu', 'gpu', 'weight', 'ram', 'storage', 'display', 'camera','wifi', 'usb', 'blue', 'battery', 'url']

for url in urls_array:
  get_phone_data(url)
  print("parsed: ", url)


import os
import requests
from urllib.parse import urlparse
import argparse
from dotenv import load_dotenv, find_dotenv, dotenv_values

def create_short_link(bitly_token, long_url):
  url = 'https://api-ssl.bitly.com/v4/bitlinks'
  headers = {"Authorization": f"Bearer {bitly_token}"}
  payload = {
    'long_url':f'{long_url}'
  }

  response = requests.post(url, headers=headers, json=payload)
  response.raise_for_status()
  
  bitlink = response.json()['link']
  if 'error' in bitlink:
    raise requests.exceptions.HTTPError(bitlink['error'])
  return bitlink




def count_clicks(bitly_token, bitlink):
  bitlink = urlparse(bitlink)
  
  clicks_url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink.netloc + bitlink.path}/clicks/summary'

  headers = {"Authorization": f"Bearer {bitly_token}"}

  response = requests.get(clicks_url, headers=headers)
  
  clicks_count = response.json()['total_clicks']
  
    
  response.raise_for_status()

  return clicks_count

def is_bitlink(bitly_token, url):
  bitlink = urlparse(url)
  
  headers = {"Authorization": f"Bearer {bitly_token}"}
  
  check_link = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink.netloc + bitlink.path}'
  response = requests.get(check_link, headers=headers)
  
  response.raise_for_status()
  return response.ok

  

if __name__ == '__main__':
  load_dotenv()
  bitly_token = os.getenv("BITLY_TOKEN")
  parser = argparse.ArgumentParser(
    description='Вставте ссылку или Битлинк'
  )
  parser.add_argument('-l','--link', help='Ссылка / Битлинк')
  args_namespace = parser.parse_args()
  
  
  

  try:
    if is_bitlink(bitly_token, args_namespace.link):
      clicks_count = count_clicks(bitly_token, args_namespace.link)
      print('На данную ссылку кликнули:', clicks_count, 'раз')
  except requests.exceptions.HTTPError:    
    try:
      bitlink = urlparse(create_short_link(bitly_token, args_namespace.link))
      print('Битлинк создан:', create_short_link(bitly_token, args_namespace.link))
    except KeyError as error:
      print("Cant create bitlink: {0}".format(error))
  
  

 
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
  bitlink = response.json()['link']
  
  response.raise_for_status()
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
  bitlink_token= dotenv_values(find_dotenv(filename='.env'))
  bitly_token = bitlink_token["BITLY_TOKEN"]

  parser = argparse.ArgumentParser(
    description='Описание как работать с программой'
  )
  parser.add_argument('-l','--link', help='Ссылка / Битлинк')
  args_namespace = parser.parse_args()
  args_link = args_namespace.link
  
  

  try:
    if is_bitlink(bitly_token, args_link):
      clicks_count = count_clicks(bitly_token, args_link)
      print('На данную ссылку кликнули:', clicks_count, 'раз')
  except requests.exceptions.HTTPError:    
    try:
      bitlink = urlparse(create_short_link(bitly_token, args_link))
      print('Битлинк создан:', create_short_link(bitly_token, args_link))
    except KeyError as error:
      print("Cant create bitlink: {0}".format(error))
  
  

 
import sys

import clipboard
import appex

import requests
from bs4 import BeautifulSoup
import base64


url = appex.get_url()
if not url and len(sys.argv) > 1:
	url = sys.argv[1]
if not url:
	url = clipboard.get()

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
for title in soup.find_all('title'):
	label = title.get_text()
	
icon_link = soup.find("link", rel="shortcut icon")
if icon_link:
	icon_url = icon_link.get('href')
	# TODO: Get the smallest size
	# TODO: Get the file format

	icon_response = requests.get(icon_url)
	icon_data = icon_response.content
	icon_base_64 = base64.b64encode(icon_data)
	icon_string = icon_base_64.decode('utf-8')
else:
	icon_url = ''

if icon_url:
	clipboard.set(f'<img src="data:image/ico;base64,{icon_string}" width="12"> [{label}]({url})')
else:
	clipboard.set(f'[{label}]({url})')

appex.finish()



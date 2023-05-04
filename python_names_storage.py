from bs4 import BeautifulSoup
from google.cloud import storage
from google.oauth2 import service_account
import requests
import csv

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

credentials_dict = {
  "type": "service_account",
  "project_id": "concise-result-382223",
  "private_key_id": "98d803365a81707fb252d7a4cbc2eb0d35d01f6c",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCoXNJ95d++aGIr\nAXeXCLA3O4bnnN2nEHi/cIH1oDlKOWP0FXKRwdfGvlALpPQzQ88eXG235Tcpbutr\nsPzyvHqpIRO/vgC3gJyQruG//EVAkpeYSM1XUSjE9vyUJ6w3OwumEGOcVLPWOb68\nUdhZUugqmIYdgdo6VJ8M1v7duYSU5OBuGYBFJydJ381wyq8jXNQi5twQHZlvwCjo\nTRdkQIQXRdO+cuaPbVBhdWZFIooBG9XpzBODq9iDfkENpjnbJfNL2f+iUzIC3p6w\np9kGtGd80KqLN7xbTddRw6ObQp36Y6FmQeOM065RaXQ+nCE0eAlPZLaUHdmZMaFL\n/93mAR7XAgMBAAECggEACE+EqGhHchuu9NZ+s7rfD+rlTtuEaXG7tB92msxM56gL\nkgnY/O7nmszcIKcE0t7/A02msNQks+vgvREge07ocx7J3cYgPO6hS9cGF7b5KCXU\nS9UUJcJA0/ApKZsHujY07f6THC1mLyXsj1ku58Ha6fdbb2twfT6eF0EplYJJ1Buf\nn/f4pacGRtecsb0JSF4QmW41AT6LvHnkMXSDZEHurYTE+tUSZGPDeAFtVp/lUwYM\nEvtg868+lThAl2gnbLoyjqvygE/4LztEqh05o5ElYNE32H+0KVHKdS0sXbtDO/EU\nUHhN3h1nJQiD4DAxb4+5LKnlKTJVRwfr6H5xgKU5UQKBgQDZWOeZD6yY3y+CzFvw\nxHJKAbcexVuLDqJ/z7eFVzdIPAYsTKRb0vp8zwK7R8pONK5Clm9UkFNRB1z5Io/9\no6xpHPXMDWkc0M2aQWGUkVH8YjsS6i2BIp6x7VhosS2CgpZW4t+PGzjJaVnsRsBB\nUWYqN9Z+OYN2diF2hEPzxtTrHwKBgQDGTc7bcpi2T6IpxhYIQBr49TP6bWAW2FJj\n57PP34ITx1m6oGm09Ri0GEXFft6HYNraOlHo4wdQ7KwZBL8fGsditJa3FSdzqo1s\nyGN80ZfWpoapnW94oL/wsPiZuZo21ROfEILT0S2WxCkZSFVL7MpvFgvmSMI7x0Bd\nZLWBQvaNSQKBgQC+a9/tAAiNnux3QihDFzmykTIoqWx8toO0Sv5UuobaqIwX/8X4\nFS4UbyHLhyg9wHX0LOy5QAFe+n6AX8GbzOxe41qOPimbb2zS+vlNOsyDvGRZPAZG\nH1i+Nl3Ay4o9z797vCV1sbnc7Io2Mf56u6Aw2N75k9YT0Yeb2GHYkJk2rQKBgQCl\n94UDQVvyaZ+tGq5h5VUtu/ruww/CzvXVy5xAhC3X4+aDPbJ60w8D27S5YD9aSoOg\nVWMsaKY84nf+0Gws2jq5r67cOAY21i1bODObyccszV6zIqKi8Nbz2QmXjzE0Zwzu\n+eCk6tMe9bn4AQPycZHTez4mVArMAS0rfRgzwRmckQKBgHRmZqtg+eusHoyThZgb\nmLuhL2lj9V217fQx+dDkuW7AyhmGK08eYwZxQRJNXccgnVi70JCbdt0lf6Kg2kuK\n8x6/qa4F34MaTdbrdCr0yzB3fT7IqQkPUxuMcfJxEpklFaZSeVVKsauQAMfoETga\njhGvbDzM3MFTrtwwXgvc/1rM\n-----END PRIVATE KEY-----\n",
  "client_email": "314972401186-compute@developer.gserviceaccount.com",
  "client_id": "108910992508325083929",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/314972401186-compute%40developer.gserviceaccount.com"
}

try:

  """Uploads a file to the bucket."""
  credentials = service_account.Credentials.from_service_account_info(credentials_dict)
  storage_client = storage.Client(credentials=credentials)
  bucket = storage_client.get_bucket('artists_names_ju') ### Nome do seu bucket
  blob = bucket.blob('artist-names.csv')

  pages = []
  names = "Name \n"

  for i in range(1, 5):
    url = 'https://web.archive.org/web/20121007172955/https://www.nga.gov/collection/anZ' + str(i) + '.htm'
    pages.append(url)

  for item in pages:
    page = requests.get(item)
    soup = BeautifulSoup(page.text, 'html.parser')

    last_links = soup.find(class_='AlphaNav')
    last_links.decompose()

    artist_name_list = soup.find(class_='BodyText')
    artist_name_list_items = artist_name_list.find_all('a')

    for artist_name in artist_name_list_items:
      names = names + artist_name.contents[0] + "\n"

    blob.upload_from_string(names, content_type="text/csv")

except Exception as ex:
  print(ex) 

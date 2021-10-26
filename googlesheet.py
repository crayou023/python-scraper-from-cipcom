from bs4 import BeautifulSoup
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

scopes = ["https://spreadsheets.google.com/feeds"]

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json", scopes)

client = gspread.authorize(credentials)

sheet = client.open_by_key(
    "1ZPbdj50OIDXv9CUx0Y9DrSGHjWRGOSJfePkcoQMI7aI").sheet1

c = input("請輸入網址")

response = requests.get(c)

soup = BeautifulSoup(response.text, "html.parser")
# print(soup.prettify())  # 輸出排版後的HTML內容

result = soup.find_all("script", language="JavaScript", limit=1)
# print(result)
out = str(result)
df = pd.DataFrame(columns=['日期', '價格'])

for i in range(500):
    int = i
    int2 = i + 1
    str1 = "arrValue[" + str(int) + "]=\""
    str2 = "\";arrValue[" + str(int2) + "]"
    r = out.find(str1)
    l = out.find(str2)
    s = out[r:l]
    lst = len(str1)
    sp = s[lst:]
    if len(sp) != 0:
        line = sp.split('/價格:')
        date = line[0]
        price = line[1]
        new = pd.DataFrame({
            '日期': date,
            '價格': price
        },
            index=[1])   # 自定義索引為：1 ，這裏也可以不設置index
        df = df.append(new, ignore_index=True)
        # print(line)

sheet.update([df.columns.values.tolist()] + df.values.tolist())

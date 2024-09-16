import http.client

conn = http.client.HTTPSConnection("seeking-alpha.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "2ea2e9c90emsh023fc8de0ef582ep168d1fjsne981a8300d92",
    'x-rapidapi-host': "seeking-alpha.p.rapidapi.com"
}

conn.request("GET", "/news/v2/list?size=20&category=market-news%3A%3Aall&number=1", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))


# Get News By Symbol
import http.client

conn = http.client.HTTPSConnection("seeking-alpha.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "2ea2e9c90emsh023fc8de0ef582ep168d1fjsne981a8300d92",
    'x-rapidapi-host': "seeking-alpha.p.rapidapi.com"
}
stock ="aapl"
conn.request("GET", f"/news/v2/list-by-symbol?size=20&number=1&id={stock}", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
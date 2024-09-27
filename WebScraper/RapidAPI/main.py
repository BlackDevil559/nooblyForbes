import http.client

conn = http.client.HTTPSConnection("seeking-alpha.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "2ea2e9c90emsh023fc8de0ef582ep168d1fjsne981a8300d92",
    'x-rapidapi-host': "seeking-alpha.p.rapidapi.com"
}

conn.request("GET", "/news/v2/list-by-symbol?size=20&number=1&id=tsla", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
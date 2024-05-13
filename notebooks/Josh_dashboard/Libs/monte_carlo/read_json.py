def read_json(url):
    request = Request(url)
    response = urlopen(request)
    #print(response)
    data = response.read()
    #print(data)
    url2 = json.loads(data)
    return url2
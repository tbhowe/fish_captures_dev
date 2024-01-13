
#%%

########### Python 3.2 #############
import http.client, urllib.request, urllib.parse, urllib.error, base64

with open('tide_api_key') as f:
    api_key = f.read()

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': api_key,
}

params = urllib.parse.urlencode({
})

try:
    conn = http.client.HTTPSConnection('admiraltyapi.azure-api.net')
    conn.request("GET", "/uktidalapi/api/V2/Stations/" % params, "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

####################################
# %%

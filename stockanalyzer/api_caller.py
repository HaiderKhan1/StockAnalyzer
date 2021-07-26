import requests
import json

def get_first_option(input):
    url = "https://yfapi.net/v6/finance/autocomplete"
    querystring = {"query":input,"lang":"en","region":"US"}

    headers = {
        'x-api-key': "0lLQYJeZw77eiDnmaeNk28pLAdKzK4Aw174peJKr"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response.text)

#validates the ticker symbol
def validate_ticker(input):
    url = "https://yfapi.net/v11/finance/quoteSummary/"+input
    querystring = {"modules":"defaultKeyStatistics,assetProfile","region":"US","lang":"en"}
    headers = {'x-api-key': "0lLQYJeZw77eiDnmaeNk28pLAdKzK4Aw174peJKr"}
    response = requests.request("GET", url, headers=headers, params=querystring)

    if response.status_code == 200:
        data = json.loads(response.text)
        if data["quoteSummary"]["result"] == None:
            return False
    else:
        return True

#validates stock name, and returns it corresponding symbol
#returns the symbol if it valided, else returns the number -1
def validate_name(input):
    return_string = ""
    url = "https://yfapi.net/v6/finance/autocomplete"
    querystring = {"query":input,"lang":"en","region":"US"}

    headers = {
        'x-api-key': "0lLQYJeZw77eiDnmaeNk28pLAdKzK4Aw174peJKr"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    data = json.loads(response.text)
    if response.status_code == 200:
        return data["ResultSet"]["Result"][0]["symbol"]
    else:
        return -1




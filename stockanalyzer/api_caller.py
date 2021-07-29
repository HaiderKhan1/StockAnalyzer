import requests
import json

fapi_key = {
    'X-API-KEY': '0lLQYJeZw77eiDnmaeNk28pLAdKzK4Aw174peJKr'
}

headers = {
    'x-rapidapi-key': "57224769e1msh3f02ba88a989b5ep1cb616jsnaa1cacdc593a",
    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
}


#validates the ticker symbol
def validate_ticker(input):
    url = "https://yfapi.net/v11/finance/quoteSummary/"+input
    querystring = {"modules":"defaultKeyStatistics,assetProfile","region":"US","lang":"en"}
    response = requests.request("GET", url, headers=fapi_key, params=querystring)

    if response.status_code == 200:
        data = json.loads(response.text)
        if data["quoteSummary"]["result"] == None:
            return False
        else:
            return True
    else:
        return False

#validates stock name, and returns it corresponding symbol
#returns the symbol if it valided, else returns the number -1
def validate_name(input):
    url = "https://yfapi.net/v6/finance/autocomplete"
    querystring = {"query":input,"lang":"en","region":"US"}
    response = requests.request("GET", url, headers=fapi_key, params=querystring)
    data = json.loads(response.text)
    if response.status_code == 200:
        return data["ResultSet"]["Result"][0]["symbol"]
    else:
        return -1




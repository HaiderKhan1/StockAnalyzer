import requests
import json

fapi_key = {
    'X-API-KEY': '0lLQYJeZw77eiDnmaeNk28pLAdKzK4Aw174peJKr'
}

headers = {
    'x-rapidapi-key': "57224769e1msh3f02ba88a989b5ep1cb616jsnaa1cacdc593a",
    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
}

class stock():
    # class variable
    benchmark_avarage = {}
    
    #constructor method
    def __init__(self, input):
        #instance variables
        self.ticker = input
        self.stock_info = {}
        self.stock_info["ticker"] = self.ticker
        self.industry_averages = {}

    #get the core financial info of the inputted stock
    #set the values of inputted stock
    def get_stock_info(self):
        url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-summary"
        querystring = {"symbol":self.ticker,"region":"US"}
        response = requests.request("GET", url, headers=headers, params=querystring)
        data = json.loads(response.text)
        
        #get the full name
        if len(data["price"]) > 0 and data["price"]["longName"]:
            self.stock_info["full_name"] = data["price"]["longName"]
        else:
            self.stock_info["full_name"] = self.ticker
        
        #get business description
        if len(data["summaryProfile"]) > 0 and data["summaryProfile"]["longBusinessSummary"]:
            self.stock_info["business_summary"] = data["summaryProfile"]["longBusinessSummary"]
        else:
            self.stock_info["business_summary"] = None

        #get key financials
        
    #get the average of the stocks in the same industry
    #set the value of the industry averages 
    def get_stocks_similars(self):
        # get similars
        url = 'https://yfapi.net/v6/finance/recommendationsbysymbol/'+self.ticker
        response = requests.get(url = url, headers=fapi_key)
        data_symbols = json.loads(response.text)
        recomendations = []
        if data_symbols["finance"]["result"][0]["recommendedSymbols"]:
            for i in data_symbols["finance"]["result"][0]["recommendedSymbols"]:
                recomendations.append(i["symbol"])
        
        self.industry_averages["similar_companies"] = recomendations
        
        #loop through each of the companies, and tally up the financials and divide by the number of companies
        params = (('lang', 'en'),('region', 'US'),('modules', 'defaultKeyStatistics,assetProfile'))
        avg_eps = avg_pe = avg_peg = avg_ptb = avg_ebita = 0
        pe_tracker = eps_tracker = peg_tracker = ebita_tracker = ptb_tracker = 0

        for symbol in recomendations:     
            summary_url = 'https://yfapi.net/v11/finance/quoteSummary/'+symbol
            response = requests.get(url = summary_url, headers=fapi_key, params=params)
            data = json.loads(response.text)
            #get forward P/E
            if data["quoteSummary"]["result"][0]["defaultKeyStatistics"]["forwardPE"]["fmt"]:
                avg_pe += float(data["quoteSummary"]["result"][0]["defaultKeyStatistics"]["forwardPE"]["fmt"])
                pe_tracker+=1
            
            #get eps
            if data["quoteSummary"]["result"][0]["defaultKeyStatistics"]["forwardEps"]["fmt"]:
                avg_eps+= float(data["quoteSummary"]["result"][0]["defaultKeyStatistics"]["forwardEps"]["fmt"])
                eps_tracker+=1
            
            #get peg
            if data["quoteSummary"]["result"][0]["defaultKeyStatistics"]["pegRatio"]["fmt"]:
                avg_peg += float(data["quoteSummary"]["result"][0]["defaultKeyStatistics"]["pegRatio"]["fmt"])
                peg_tracker += 1
            
            #get price to book
            if data["quoteSummary"]["result"][0]["defaultKeyStatistics"]["priceToBook"]["fmt"]:
                avg_ptb += float(data["quoteSummary"]["result"][0]["defaultKeyStatistics"]["priceToBook"]["fmt"])
                ptb_tracker += 1
            
            #get ebita
            if data["quoteSummary"]["result"][0]["defaultKeyStatistics"]["enterpriseToEbitda"]["fmt"]:
                avg_ebita += float(data["quoteSummary"]["result"][0]["defaultKeyStatistics"]["enterpriseToEbitda"]["fmt"])
                ebita_tracker += 1

        #calculate industry averages
        if eps_tracker > 0:
            self.industry_averages["avg_eps"] = avg_eps/eps_tracker
        else:
            self.industry_averages["avg_eps"] = "N/A"

        if pe_tracker > 0:
            self.industry_averages["avg_pe"] = avg_pe/pe_tracker
        else:
            self.industry_averages["avg_pe"] = "N/A"
        
        if ptb_tracker > 0:
            self.industry_averages["avg_ptb"] = avg_ptb/ptb_tracker
        else:
            self.industry_averages["avg_ptb"] = "N/A"
        
        if ebita_tracker > 0:
            self.industry_averages["avg_ebita"] = avg_ebita/ebita_tracker
        else:
            self.industry_averages["avg_ebita"] = "N/A"
        
        if peg_tracker > 0:
            self.industry_averages["avg_peg"] = avg_peg/peg_tracker
        else:
            self.industry_averages["avg_peg"] = 'N/A'
            
    #check if the inputted stock is above or below average
    #return over valued or under valued
    def fundemental_analysis(self):
        print("whatever")

stock = stock("aapl")
stock.get_stocks_similars()
print(stock.industry_averages)

#specific to the stock in question: working capital, free cash flow, enterpirse value


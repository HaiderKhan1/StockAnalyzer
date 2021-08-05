import requests
import json
import time

fapi_key = {
    'X-API-KEY': '0lLQYJeZw77eiDnmaeNk28pLAdKzK4Aw174peJKr'
}

headers = {
    'x-rapidapi-key': "57224769e1msh3f02ba88a989b5ep1cb616jsnaa1cacdc593a",
    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
}

class Stock():    
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
        
        #get info
        if "longName" in data["price"]:
            self.stock_info["full_name"] = data["price"]["longName"]
        else:
            self.stock_info["full_name"] = self.ticker
        
        if "longBusinessSummary" in data["summaryProfile"]:
            self.stock_info["business_summary"] = data["summaryProfile"]["longBusinessSummary"]
        else:
            self.stock_info["business_summary"] = "null"

        if "recommendationKey" in data["financialData"]:
            self.stock_info["finance_recommendation"] = data["financialData"]["recommendationKey"]
        else:
            self.stock_info["finance_recommendation"] = "null"
        
        if "fmt" in data["financialData"]["totalDebt"]:
            self.stock_info["total_debt"] = data["financialData"]["totalDebt"]["fmt"]
        else:
            self.stock_info["total_debt"] = "null"
        
        if "fmt" in data["financialData"]["returnOnEquity"]:
            self.stock_info["roe"] = data["financialData"]["returnOnEquity"]["fmt"]
        else:
            self.stock_info["roe"] = "null"

        if "fmt" in data["defaultKeyStatistics"]["enterpriseValue"]:
            self.stock_info["ev"] = data["defaultKeyStatistics"]["enterpriseValue"]["fmt"]
        else:
            self.stock_info["ev"] = "null"

        #get comparison financials
        params = (('lang', 'en'),('region', 'US'),('modules', 'defaultKeyStatistics,assetProfile'))
        summary_url = 'https://yfapi.net/v11/finance/quoteSummary/'+self.ticker
        response = requests.get(url = summary_url, headers=fapi_key, params=params)
        fdata = json.loads(response.text)
        
        #get forward P/E
        if "fmt" in fdata["quoteSummary"]["result"][0]["defaultKeyStatistics"]["forwardPE"]:
            self.stock_info["pe"] = float(fdata["quoteSummary"]["result"][0]["defaultKeyStatistics"]["forwardPE"]["fmt"])
        else:
            self.stock_info["pe"] = "null"
            
        #get eps
        if "fmt" in fdata["quoteSummary"]["result"][0]["defaultKeyStatistics"]["forwardEps"]:
            self.stock_info["eps"] = float(fdata["quoteSummary"]["result"][0]["defaultKeyStatistics"]["forwardEps"]["fmt"])
        else:
            self.stock_info["eps"] = "null"
                    
        #get peg
        if "fmt" in fdata["quoteSummary"]["result"][0]["defaultKeyStatistics"]["pegRatio"]:
            self.stock_info["peg"] = float(fdata["quoteSummary"]["result"][0]["defaultKeyStatistics"]["pegRatio"]["fmt"])
        else:
            self.stock_info["peg"] = "null"
                
        #get price to book
        if "fmt" in fdata["quoteSummary"]["result"][0]["defaultKeyStatistics"]["priceToBook"]:
            self.stock_info["ptb"] = float(fdata["quoteSummary"]["result"][0]["defaultKeyStatistics"]["priceToBook"]["fmt"])
        else:
            self.stock_info["ptb"] = "null"
            

    def get_stocks_similars(self):
        # get similars
        url = 'https://yfapi.net/v6/finance/recommendationsbysymbol/'+self.ticker
        response = requests.get(url = url, headers=fapi_key)
        data_symbols = json.loads(response.text)
        recomendations = []
        if "recommendedSymbols" in data_symbols["finance"]["result"][0]:
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
            if "fmt" in data["quoteSummary"]["result"][0]["defaultKeyStatistics"]["forwardPE"]:
                avg_pe += float(data["quoteSummary"]["result"][0]["defaultKeyStatistics"]["forwardPE"]["fmt"])
                pe_tracker+=1
            
            #get eps
            if "fmt" in data["quoteSummary"]["result"][0]["defaultKeyStatistics"]["forwardEps"]:
                avg_eps+= float(data["quoteSummary"]["result"][0]["defaultKeyStatistics"]["forwardEps"]["fmt"])
                eps_tracker+=1
            
            #get peg
            if "fmt" in data["quoteSummary"]["result"][0]["defaultKeyStatistics"]["pegRatio"]:
                avg_peg += float(data["quoteSummary"]["result"][0]["defaultKeyStatistics"]["pegRatio"]["fmt"])
                peg_tracker += 1
            
            #get price to book
            if "fmt" in data["quoteSummary"]["result"][0]["defaultKeyStatistics"]["priceToBook"]:
                avg_ptb += float(data["quoteSummary"]["result"][0]["defaultKeyStatistics"]["priceToBook"]["fmt"])
                ptb_tracker += 1

        #calculate industry averages
        if eps_tracker > 0:
            self.industry_averages["avg_eps"] = avg_eps/eps_tracker
        else:
            self.industry_averages["avg_eps"] = "null"

        if pe_tracker > 0:
            self.industry_averages["avg_pe"] = avg_pe/pe_tracker
        else:
            self.industry_averages["avg_pe"] = "null"
        
        if ptb_tracker > 0:
            self.industry_averages["avg_ptb"] = avg_ptb/ptb_tracker
        else:
            self.industry_averages["avg_ptb"] = "null"

        if peg_tracker > 0:
            self.industry_averages["avg_peg"] = avg_peg/peg_tracker
        else:
            self.industry_averages["avg_peg"] = "null"
            
    #check if the inputted stock is above or below average
    #return over valued or under valued
    def fundemental_analysis(self):
        points = 0
        # lets check for the peg
        if self.stock_info["peg"] != "null" and self.industry_averages["avg_peg"] != "null":
            if self.stock_info["peg"] > 2:
                return "High PEG Ratio Indicates: Over Valued"
            else: 
                if self.stock_info["peg"] < self.industry_averages["avg_peg"]:
                    points+=1
                else:
                    points+=0.5
        if self.stock_info["eps"] != "null" and self.industry_averages["avg_eps"] != "null":
            if self.stock_info["eps"] > self.industry_averages["avg_eps"]:
                points +=1
            else:
                points += 0.5
        
        if points == 2:
            return "Under Valued"
        elif points == 1:
            return "Fair Valued"
        else:
            "Could Not Compute"
        



start_time = time.time()
stock = Stock("intc")
stock.get_stocks_similars()
stock.get_stock_info()
ret = stock.fundemental_analysis()
print("#################### %s ####################"%(ret))
print(stock.stock_info)
print("---------------------")
print(stock.industry_averages)
print("---------------------")
print("%s"%(time.time() - start_time))






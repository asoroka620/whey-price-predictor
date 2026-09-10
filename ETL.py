# Goal: Predict Average Retail Whey Protein Price of 5lb tubs within Canada

# Things we need:
# Scraped data of whey protein brands off amazon
# To get historical data: - maybe only grab the top 5 products?
# 	Amazon - use camelcamelcamel

# 	Brand name
# 	Year of this price
# 	The week this price was in (week 1 week 2 etc.)
# 	Price of 5lb tub
# 	Made in Canada
# 	Whey or Isolate

# Dataset on cheese production in north America
# For the US: You can pull free, beautifully structured historical monthly cheese production reports directly from the USDA National Agricultural Statistics Service.For Canada: You can pull clean historical data directly from Statistics Canada (StatCan).
# 	We'll have to apply the same date thing we're doing where we map it to weeks

# The Keepa Extension Chart Hack (Easiest & Free)While Keepa charges for its API, their Keepa Browser Extension is 100% free and displays interactive timeline charts directly on Amazon.ca product pages.How to get the data: When you hover your mouse over the Keepa chart on Amazon, it tracks every single historical date and price.The Manual Export: Because you are only tracking 3 to 5 products for this project, you don't even need to write a scraper. You can open the Keepa panel on those few products, click on the "Data" or "Settings" tab within the extension widget, and look for an option to "Export product data". It allows you to download a completely free, highly detailed historical .csv file directly to your computer.

import pandas as pd


def extract():
    us_dry_whey_prod = pd.read_csv("data/USDA Dry Whey Prod..csv")
    canada_quarterly_stock = pd.read_csv("data/Stocks of specified dairy products, quarterly 1 2.csv")
    canada_prod_concen_milk = pd.read_csv("data/Production of concentrated milk products.csv")
    return us_dry_whey_prod, canada_quarterly_stock, canada_prod_concen_milk

def transform_us_data(df):
    #DELETE ROWS THAT CONTAIN YEAR, THIS PROVIDES THE YEARLY TOTAL
    df = df[['YEAR','PERIOD','VALUE','COMMODITY']]
    df = df[df['PERIOD'] != 'YEAR']
    df = df.rename(columns = {"VALUE" : "POUNDS"})

def transform_can_data_quarter(quarter):
   # Maps the quarter totals to dictionairy
   # Create empty df
   # For each week, append the year,week, the quarter total / 13
    whey = quarter[quarter["Commodity"] == "Whey powder"].iloc[0]
    week_ranges = {
        "Q1": range(1, 14),
        "Q2": range(14, 27),
        "Q3": range(27, 40),
        "Q4": range(40, 53)
    }

    df_list = []

    for col in whey.index:
        if col == "Commodity":
            continue

        qtr, year = col.split(" ")
        year = int(year)

        tonnes = int(str(whey[col]).replace(",", ""))
        tonnes_per_week = tonnes / 13

        for week in week_ranges[qtr]:
            df_list.append({
                "Year": year,
                "Week": week,
                "Tonnes": tonnes   })

def transform_can_data_total(total):
    # Create weeks column and assign a week number based on the date
    # Get rid of any row that is not whey powder
    # Pivot the table longer
    #Create a year and month column and split the year and month on " "
    #Create empty df, that contains year, week number, tonnes prod.
    

def main():
    us_dry_whey_prod, canada_quarterly_stock, canada_prod_concen_milk = extract()
    transform_us_data(us_dry_whey_prod)


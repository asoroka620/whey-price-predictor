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


def extract_csv():
    us_dry_whey_prod = pd.read_csv("data/USDA Dry Whey Prod..csv")
    canada_quarterly_stock = pd.read_csv("data/Stocks of specified dairy products, quarterly 1 2.csv")
    canada_prod_concen_milk = pd.read_csv("data/Production of concentrated milk products.csv")
    return us_dry_whey_prod, canada_quarterly_stock, canada_prod_concen_milk

def transform_us_data(df):
    #DELETE ROWS THAT CONTAIN YEAR, THIS PROVIDES THE YEARLY TOTAL
    df = df[['YEAR','PERIOD','VALUE','COMMODITY']]
    df = df[df['PERIOD'] != 'YEAR']
    df = df.rename(columns = {"VALUE" : "POUNDS"})
    return df

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
    return pd.DataFrame(df_list)

def transform_can_data_total(total):
    # Create weeks column and assign a week number based on the date
    # Get rid of any row that is not whey powder
    # Pivot the table longer
    #Create a year and month column and split the year and month on " "
    #Create empty df, that contains year, week number, tonnes prod.
    whey = total[total["Commodity"] == "Whey powder"]

    df_long = whey.melt(
        id_vars = "Commodity",
        var_name = "Date",
        value_name = "Tonnes"
    )
    df_long["Tonnes"] = pd.to_numeric(df_long["Tonnes"])
    df_long["Date"] = pd.to_datetime(df_long["Date"])
    df_long["Year"] = df_long["Date"].dt.year
    df_long["Month"] = df_long["Date"].dt.month_name()

    month_week = {
        "January" : range(1,6),
        "February" : range(6,10),
        "March" : range(10,14),
        "April" : range(14,19),
        "May" : range(19, 23),
        "June" : range(23,27),
        "July" : range(27,32),
        "August" : range(32, 36),
        "September" : range(36, 40),
        "October" : range(40, 45),
        "November" : range(45, 49),
        "December" : range(49, 53)
    }

    df_weeks = []

    for row in df_long.itertuples(index=False):

        weeks = list(month_week[row.Month])
        weekly_tonnes = row.Tonnes / len(weeks)

        for week in weeks:
            df_weeks.append({
                "Year": row.Year,
                "Week": week,
                "Tonnes": weekly_tonnes
            })

    df_weeks = pd.DataFrame(df_weeks)
    return df_weeks

def merge_can_data(can_quarter, can_total):
    combined = pd.concat([can_quarter,can_total], ignore_index = True)
    combined = combined.sort_values(by=["Year", "Week"])
    return combined

def load(usa, can):
    usa.to_csv('USA Whey Production.csv', index = False)
    can.to_csv('Canada Whey Production.csv', index = False)

def main():
    us_dry_whey_prod, canada_quarterly_stock, canada_prod_concen_milk = extract_csv()
    us_dry_whey_prod = transform_us_data(us_dry_whey_prod)
    canada_quarterly_stock = transform_can_data_quarter(canada_quarterly_stock)
    canada_prod_concen_milk = transform_can_data_total(canada_prod_concen_milk)
    canada_total_prod = merge_can_data(canada_quarterly_stock, canada_prod_concen_milk)

    load(us_dry_whey_prod, canada_total_prod)



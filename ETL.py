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



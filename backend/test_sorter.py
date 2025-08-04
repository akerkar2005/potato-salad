from stockSorter import StockSorter

if __name__ == "__main__":
    sorter = StockSorter("AGGREGATED_STOCK_DATA.csv")
    sorted_stocks = sorter.sortWithPreferences()
    # Print as a table
    if sorted_stocks:
        headers = sorted_stocks[0].keys()
        print('\t'.join(headers))
        for stock in sorted_stocks[:10]:
            print('\t'.join(str(stock[h]) for h in headers))
    else:
        print("No stocks found.")

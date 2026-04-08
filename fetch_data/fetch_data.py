# %%
# Import important library
import requests
import pandas as pd
import os
import gspreadÍ›
from oauth2client.service_account import ServiceAccountCredentials

# %%
# CONFIGURATION
# Include required fields
security_fields = ['cusip', 'securityType', 'securityTerm', 'originalSecurityTerm', 'series', 'corpusCusip', 'interestRate', 'tips', 'floatingRate', 'callable', 'callDate']

auction_fields = ['cusip', 'auctionDate', 'auctionDateYear', 'announcementDate', 'issueDate', 'maturityDate', 'datedDate', 'maturingDate', 'auctionFormat','closingTimeCompetitive',
            'closingTimeNoncompetitive', 'offeringAmount', 'allocationPercentage', 'totalTendered', 'totalAccepted', 'bidToCoverRatio', 'interestRate', 'highYield', 'lowYield',
            'averageMedianYield', 'highDiscountRate', 'lowDiscountRate', 'highInvestmentRate', 'lowInvestmentRate', 'highPrice', 'lowPrice', 'pricePer100', 'updatedTimestamp'
]

bidder_fields = ['cusip', 'totalAccepted', 'primaryDealerAccepted', 'directBidderAccepted', 'indirectBidderAccepted', 'fimaNoncompetitiveAccepted', 'somaAccepted', 
                'competitiveAccepted', 'noncompetitiveAccepted','treasuryRetailAccepted']


# Excel file to keep updating
base_path = os.path.dirname(os.path.abspath(__file__)) # get the original place of the script
CSV_FILE = os.path.join(base_path, "US_Auction_Data.csv") # point to the csv file 
# Treasury Direct API
API_URL = "https://www.treasurydirect.gov/TA_WS/securities/jqsearch"

# %%
# Fetch the data
def get_data():
    # FETCH API DATA
    response = requests.get(API_URL)
    new_records = response.json()

    # Only keep the required fields
    df = pd.DataFrame(new_records['securityList'])

    # check if required field existed in the API response
    #security_required_fields = [field for field in security_fields if field in df.columns]
    #auction_required_fields = [field for field in auction_fields if field in df.columns]
    #bidder_required_fields = [field for field in bidder_fields if field in df.columns]
    security_new_df = df[security_fields].copy()
    auction_new_df = df[auction_fields].copy()
    bidder_new_df = df[bidder_fields].copy()

    # full worksheet copy
    master_df = df.copy()
    #master_df['issueDate'] = master_df['issueDate'].dt.strftime('%Y-%m-%d')
    master_df = master_df.fillna('')

    # Put the data into the speadsheet
    # Step 1: Setup the connection
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/henrytran/Documents/GitHub/Fiscal-Trade-Policy-Intelligence/Robot Key/Fiscal Index Intelligence.json', scope) # take the credential
    client = gspread.authorize(creds)
    file = client.open('Fiscal_Trade_Index')

    # Step 2: Open the sheets
    worksheets = {
        "Security": security_new_df,
        "Auction": auction_new_df,
        "Bidder": bidder_new_df,
        "Master": master_df  # The merged version
    }

    # Step 3: Loading the data into the correct table
    for worksheet, df in worksheets.items():
        try:
            sheet = file.worksheet(worksheet)
        except:
            sheet = file.add_worksheet(title=worksheet, rows="100", cols="20")
        
        # data to upload
        upload_data = [df.columns.values.tolist()] + df.fillna('').values.tolist()

        sheet.clear()
        sheet.update('A1', upload_data)
        print(f"Successfully updated {worksheet}")
    
    # Keep one CSV copy
    master_df.to_csv(CSV_FILE, index=False)
    print(f"Backup saved to {CSV_FILE}")

if __name__ == "__main__":
    get_data()

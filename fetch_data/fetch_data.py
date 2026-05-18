# %%
# Import important library
import requests
import pandas as pd
import os
from dotenv import load_dotenv
import gspread
from google.oauth2.service_account import Credentials
import json

# %%
# CONFIGURATION
# Include required fields
security_fields = ['cusip', 'securityType', 'securityTerm', 'originalSecurityTerm', 'series', 'corpusCusip', 'interestRate', 'tips', 'floatingRate', 'callable', 'callDate']

auction_fields = ['cusip', 'auctionDate', 'auctionDateYear', 'announcementDate', 'issueDate', 'maturityDate', 'datedDate', 'maturingDate', 'auctionFormat','closingTimeCompetitive',
            'closingTimeNoncompetitive', 'offeringAmount', 'allocationPercentage', 'totalTendered', 'totalAccepted', 'bidToCoverRatio', 'interestRate', 'highYield', 'lowYield',
            'averageMedianYield', 'highDiscountRate', 'lowDiscountRate', 'highInvestmentRate', 'lowInvestmentRate', 'highPrice', 'lowPrice', 'pricePer100', 'updatedTimestamp'
]

bidder_fields = ['cusip', 
                'totalAccepted', 'totalTendered',
                'primaryDealerAccepted', 'primaryDealerTendered',
                'directBidderAccepted', 'directBidderTendered',
                'indirectBidderAccepted', 'indirectBidderTendered',
                'fimaNoncompetitiveAccepted', 'fimaNoncompetitiveTendered',
                'somaAccepted', 'somaTendered',
                'competitiveAccepted', 'competitiveTendered',
                'noncompetitiveAccepted',
                'treasuryRetailAccepted']

# Excel file to keep updating
base_path = os.path.dirname(os.path.abspath(__file__)) # get the original place of the script
CSV_FILE = os.path.join(base_path, "US_Auction_Data.csv") # point to the csv file 
# Treasury Direct API
API_URL = "https://www.treasurydirect.gov/TA_WS/securities/jqsearch"

# Load the .env file
load_dotenv()

# %%
# Fetch the data
def get_data():
    # FETCH API DATA
    params ={
        'startDate': '1998-01-01',
        'format': 'json'
    }

    response = requests.get(API_URL, params=params)

    # if API call is unsuccessful, print the error code and exit
    if response.status_code != 200:
        print(f"Error fetching data: {response.status_code}")
        return

    new_records=response.json()

    # Only keep the required fields
    df = pd.DataFrame(new_records['securityList'])
    df = df.drop_duplicates(subset=['cusip', 'auctionDate'], keep='last')
    df = df.fillna('')

    # Filter the data to only include records with auctionDate after 1998-01-01
    df['auctionDate'] = pd.to_datetime(df['auctionDate'])
    df = df[df['auctionDate'] >= '1998-01-01']

    # Convert dates back to date string for Google Sheets compatibility
    df['auctionDate'] = df['auctionDate'].dt.strftime('%Y-%m-%d')

    # check if required field existed in the API response
    #security_required_fields = [field for field in security_fields if field in df.columns]
    #auction_required_fields = [field for field in auction_fields if field in df.columns]
    #bidder_required_fields = [field for field in bidder_fields if field in df.columns]
    security_new_df = df[security_fields].copy()
    auction_new_df = df[auction_fields].copy()
    bidder_new_df = df[bidder_fields].copy()

    # full worksheet copy
    master_df = df.copy()

    # Put the data into the speadsheet
    # Step 1: Setup the connection
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    # JSON string from the Github secret variable
    json_secret = os.getenv('GCP_SERVICE_ACCOUNT_KEY')  
    if json_secret:
        # Use GitHub Secret
        service_account_info = json.loads(json_secret)
        creds = Credentials.from_service_account_info(service_account_info, scopes=scope)
    else:
        # Use local JSON file path from .env
        local_key_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if not local_key_path:
            raise ValueError("Credentials not found! Check your .env file or GitHub Secrets and variables")
        creds = Credentials.from_service_account_file(local_key_path, scopes=scope)
    #creds = Credentials.from_service_account_file(service_account_json, scope) # take the credential
    client = gspread.authorize(creds)
    try:
        file = client.open('Fiscal_Trade_Index')
    except:
        print('Error: Google Sheet not found! Ensure it is shared with your Service Account email.')

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

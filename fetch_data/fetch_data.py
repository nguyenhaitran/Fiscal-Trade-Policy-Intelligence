# %%
# Import important library
import requests
import pandas as pd
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# %%
# CONFIGURATION
# Include required fields
FIELDS = [
    'cusip', 'issueDate', 'securityType', 'securityTerm', 'auctionDateYear', 'maturityDate', 'datedDate', 'maturingDate',
    'auctionFormat', 'closingTimeCompetitive', 'offeringAmount', 'allocationPercentage', 'totalTendered', 'totalAccepted', 'bidToCoverRatio',
    'interestRate', 'highYield', 'lowYield', 'averageMedianYield', 'highDiscountRate', 'lowDiscountRate', 'highInvestmentRate', 'lowInvestmentRate',
    'highPrice', 'lowPrice', 'pricePer100', 'updatedTimestamp'
]

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

    # SELECTED REQUIRED FIELDS ONLY
    df = pd.DataFrame(new_records['securityList'])
    # check if required field existed in the API response
    required_fields = [field for field in FIELDS if field in df.columns]
    new_df = df[required_fields].copy()

    # Put the data into the speadsheet
    # Step 1: Setup the connection
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/henrytran/Documents/GitHub/Fiscal-Trade-Policy-Intelligence/Robot Key/Fiscal Index Intelligence.json', scope) # take the credential
    client = gspread.authorize(creds)

    # Step 2: Open the Sheet
    sheet = client.open("Fiscal_Trade_Index").worksheet("US_Auction")

    # HANDLE NEW RECORDS AND ADD TO EXISTING EXCEL FILE (ONLY IF AVAILABLE)
    if os.path.exists(CSV_FILE):
        existing_df = pd.read_csv(CSV_FILE)
        # using CUSIP as unique ID, ensuring no same auction added
        new_df['unique_id'] = new_df['cusip'].astype('str')
        existing_df['unique_id'] = existing_df['cusip'].astype('str')
        # filter the data, only keep new/non-existing records
        records_to_add = new_df[~new_df['unique_id'].isin(existing_df['unique_id'])].copy()
        # remove the helper column
        records_to_add = records_to_add.drop(columns=['unique_id'])
        
        # add new data to the current csv file
        if not records_to_add.empty:
            final_df = pd.concat([records_to_add, existing_df], ignore_index=True) # old one first, new one after
            
            # Step 3: Prepare the data
            # Use .fillna('') to ensure no 'NaN' values in case of empty values
            data_to_upload = [final_df.columns.values.tolist()] + final_df.fillna('').values.tolist()

            final_df.to_csv(CSV_FILE, index=False)

            # Step 4: Upload to Google Cloud
            sheet.clear() # Clears old data so you don't have duplicates
            sheet.update('A1', data_to_upload)

            print("Data successfully synced to Google Sheets!")

            print('There are {} new records!'.format(len(records_to_add)))
        else:
            print('No new records found!')
    else:
        # create new csv file if not existed
        new_df.to_csv(CSV_FILE, index=False)
        print('New CSV file created!')

if __name__ == "__main__":
    get_data()


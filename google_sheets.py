import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe
import pandas as pd

# This scope is required for gspread-dataframe
scope = [
    "https://spreadsheets.google.com/feeds",
    'https://www.googleapis.com/auth/spreadsheets',
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

# Function to get the main spreadsheet object
def get_spreadsheet(name='Trading-system'):
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    return client.open(name)

# Function to get a specific tab (worksheet), creating it if it doesn't exist
def get_or_create_worksheet(spreadsheet, worksheet_name):
    try:
        worksheet = spreadsheet.worksheet(worksheet_name)
    except gspread.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(title=worksheet_name, rows="1000", cols="20")
    return worksheet

# Function to update a worksheet with a DataFrame
def update_worksheet_with_df(spreadsheet_name, worksheet_name, df):
    print(f"Writing data to Google Sheet '{spreadsheet_name}' in tab '{worksheet_name}'...")
    try:
        spreadsheet = get_spreadsheet(spreadsheet_name)
        worksheet = get_or_create_worksheet(spreadsheet, worksheet_name)
        worksheet.clear()  # Clears the sheet before writing new data
        set_with_dataframe(worksheet, df)
        print("Written successful.")
        return True
    except Exception as e:
        print(f"Error writing to Google Sheets: {e}")
        return False
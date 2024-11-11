import csv
import os
from pathlib import Path
from time import sleep

import gspread
from google.oauth2.service_account import Credentials


def update_sheets():
    # Define the scopes
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",  # Access to Sheets
        "https://www.googleapis.com/auth/drive"  # Access to Drive (needed for searching files)
    ]
    # Load the service account credentials with the defined scopes
    creds = Credentials.from_service_account_file('e-lexicon-348911-b4c3d1168cca.json', scopes=scopes)
    # Use the credentials as before
    client = gspread.authorize(creds)
    # Open the spreadsheet and the first sheet
    spreadsheet = client.open("Github / UniTech - CS50x Iraq AUIB (Participants Badge) (Responses)")
    # sheets = spreadsheet.worksheets()  # Or use spreadsheet.get_worksheet(0)
    csv_directory = 'csvs/'
    csv_files = [f for f in os.listdir(csv_directory) if f.endswith('.csv')]

    # Loop through each CSV file
    for csv_file in csv_files:

        # Determine sheet name by removing '.csv' from the filename
        sheet_name = Path(csv_file).stem
        try:
            # Try to open the sheet, create it if it does not exist
            try:
                sheet = spreadsheet.worksheet(sheet_name)
            except gspread.WorksheetNotFound:
                # If not found, create the sheet
                sheet = spreadsheet.add_worksheet(title=sheet_name, rows=100, cols=20)
                print(f"Created new sheet: {sheet_name}")

            # Path to the CSV file
            csv_file_path = os.path.join(csv_directory, csv_file)

            # Read the CSV file
            with open(csv_file_path, newline='', encoding='utf-8') as cs:
                csv_reader = csv.reader(cs)
                data_list = list(csv_reader)

            # Clear existing content in the sheet and upload new data
            sleep(2)
            sheet.clear()
            sheet.update(range_name='A1', values=data_list)
            print(f"Updated sheet {sheet_name} with data from {csv_file}")

        except Exception as e:
            print(f"An error occurred while updating {sheet_name}: {e}")




def remove_prefix_from_filenames(folder, pref):
    # Convert directory to a Path object for easy manipulation
    dir_path = Path(folder)

    # Ensure the directory exists
    if not dir_path.is_dir():
        print(f"The directory {folder} does not exist.")
        return

    # Loop through all files in the directory
    for filename in os.listdir(folder):
        # Check if the filename starts with the specified prefix
        if filename.startswith(pref):
            # Create the full path for the current file
            old_file = dir_path / filename

            # Remove the prefix
            new_filename = filename[len(pref):]

            # Create the full path for the new file
            new_file = dir_path / new_filename

            # Rename the file
            os.rename(old_file, new_file)
            print(f"Renamed {old_file} to {new_file}")
        else:
            print(f"No prefix to remove in {filename}")


# Usage
# directory = 'csvs'
# prefix = 'cs50_problems_2024_x_'
# remove_prefix_from_filenames(directory, prefix)
update_sheets()
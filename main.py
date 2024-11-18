import gspread
from google.oauth2.service_account import Credentials
from fetch_data import fetch_data
import re
from datetime import datetime

def main():
    # Initialize Google Sheets credentials
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
    client = gspread.authorize(creds)

    # Google Sheets ID and worksheet name
    sheet_id = "1AyGzrFKcQUBscxkjbKLTd9kQy8M_EpxdLtkfoRIO_Js"
    worksheet_name = "SheetData"

    try:
        # Open the workbook and worksheet
        workbook = client.open_by_key(sheet_id)
        sheet = workbook.worksheet(worksheet_name)

        # Check if headers already exist
        headers = ["transactionDate", "change", "nav", "aum"]
        existing_headers = sheet.row_values(1)  # Get the first row

        if existing_headers != headers:
            print("Headers not found or incorrect. Adding headers...")
            sheet.insert_row(headers, index=1)  # Insert headers in the first row
            sheet.format("A1:D1", {"textFormat": {"bold": True}})
            print("Headers successfully added.")

        # Check the latest transaction date in the worksheet
        transaction_dates = sheet.col_values(1)[1:]  # First column without header
        if transaction_dates:
            latest_date = transaction_dates[0]  # Get the most recent date (top row)
            start_date_obj = datetime.strptime(latest_date, "%Y-%m-%d")
        else:
            start_date_obj = datetime.strptime("2023-01-01", "%Y-%m-%d")  # Default if no data exists

        # Format the start and end dates to "dd-mm-yyyy"
        start_date = start_date_obj.strftime("%d-%m-%Y")
        end_date = datetime.now().strftime("%d-%m-%Y")

        # Fetch data from the API
        print(f"Fetching data from {start_date} to {end_date}...")
        data = fetch_data(start_date=start_date, end_date=end_date)
        print("Data successfully fetched.")

        # Process new data
        new_rows = []
        for entry in data["data"]:
            transaction_date = entry.get("transactionDate", "")
            nav = entry.get("nav", "")
            aum = entry.get("aum", "")

            # Extract the number from the "change" field
            change = entry.get("change", "")
            match = re.search(r'[-+]?\d*\.\d+|\d+', change)
            change_value = match.group() if match else ""

            # Check if the transaction date is already in the worksheet, if so, skip
            if transaction_date not in transaction_dates:
                new_rows.append([transaction_date, change_value, nav, aum])

        if new_rows:
            # Insert new data above (after the header)
            sheet.insert_rows(new_rows, row=2)
            print(f"{len(new_rows)} new rows successfully added to the worksheet '{worksheet_name}'.")

        else:
            print("No new data to add.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

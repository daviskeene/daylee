from datetime import date, datetime, timedelta
import os
from typing import List

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from dotenv import load_dotenv

load_dotenv()

# # # # # # # # # #
#                 #
#   Abstractions  #
#                 #
# # # # # # # # # #


def get_gsheet_client(path_to_client_secret: str) -> gspread.Client:
    # Get Google Sheet client using scope + service account credentials
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        path_to_client_secret, scope
    )
    return gspread.authorize(creds)


def get_google_sheet(client: gspread.Client):
    # Returns the discord membership spreadsheet.
    return client.open("Semester Data Table").sheet1


def write_to_cell(sheet, row: int, col: int, value: str) -> None:
    # Updates a particular cell in the sheet.
    sheet.update_cell(row, col, value)


def write_to_row(sheet, value: list, index: int) -> None:
    # Inserts a row into a particular index in our sheet.
    sheet.insert_row(value, index)


def write_to_next_row(sheet, value: list) -> None:
    write_to_row(
        sheet, value, 2
    )  # Row count doesn't include headers, insert at index 2


def append_row(sheet, value: list) -> None:
    # Appends a row to the sheet
    sheet.append_row(value)


def get_all_formatted_records(sheet):
    records = sheet.get_all_records()
    # Convert date if not in correct format
    for i, record in enumerate(records):
        try:
            date = datetime.strptime(x["Due Date"], "%m/%d/%y")
        except:
            # On exception, change date
            records[i]["Due Date"] = (
                "/".join(record["Due Date"].split("/")[:-1])
                + f"/{str(datetime.today().year)[2:]}"
            )
    # print(records)
    return records


def get_records(sheet, type: str, days: int = 7):
    # Get record of type 'type' due within a certain amount of days (default = 7).
    return [
        x
        for x in get_all_formatted_records(sheet)
        if x["Type"] == type
        and datetime.strptime(x["Due Date"], "%m/%d/%y")
        < datetime.now() + timedelta(days=days)
    ]


def main():
    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    client = get_gsheet_client(os.getenv("PATH_TO_CLIENT_SECRET"))
    sheet = get_google_sheet(client)

    # Extract and print all of the values
    print(get_records(sheet, "Assignment"))


if __name__ == "__main__":
    # Running this file as a script will validate our connection
    # and print the number of users registered with Discord.
    main()

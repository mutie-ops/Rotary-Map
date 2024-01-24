from googleapiclient.discovery import build
from ApiCredentials import credentials
from googleApi import get_location

# Load the credentials into the service
service = build('sheets', 'v4', credentials=credentials)
sheet = service.spreadsheets()

SPREADSHEET_ID = '17ozqiGHk8nJTv6P_NE50sZsLK9y7qBIHHAOI3n7HX50'
RANGE_NAME = "'Rotary Clubs - Africa V2'!A253:H512"

# Function to get values from specified columns
def get_column_values(values, column_index):
    return [row[column_index] if len(row) > column_index else None for row in values]

# Function to create a new sheet
def create_new_sheet(service, spreadsheet_id, sheet_name):
    new_sheet_body = {
        'requests': [
            {
                'addSheet': {
                    'properties': {
                        'title': sheet_name
                    }
                }
            }
        ]
    }
    service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body=new_sheet_body).execute()

# Function to add titles to a new sheet
def add_titles_to_sheet(service, spreadsheet_id, sheet_name, titles):
    value_range = f'{sheet_name}!A1:{chr(65 + len(titles) - 1)}1'
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=value_range,
        body={'values': [titles]},
        valueInputOption='RAW'
    ).execute()

# Function to add values to a specified column in a sheet
def add_values_to_sheet_column(service, spreadsheet_id, sheet_name, column_values, column_letter):
    range_start = 2
    range_end = range_start + len(column_values) - 1
    value_range_body = f'{sheet_name}!{column_letter}{range_start}:{column_letter}{range_end}'
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=value_range_body,
        body={'values': [[value] for value in column_values]},
        valueInputOption='RAW'
    ).execute()

# Main logic

# Get values from existing sheet
result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
values = result.get('values', [])

if not values:
    print(f'No data found in range {RANGE_NAME}.')
else:
    print(f'Data in range {RANGE_NAME}:')

    # Extract values from columns A and H
    column_a_value = get_column_values(values, 0)
    column_h_value = get_column_values(values, 7)

    # Print extracted values
    print(f'Column A: {column_a_value}')
    print(f'Column H: {column_h_value}')

    # Create a new sheet
    new_sheet_name = 'Benjamin'
    create_new_sheet(service, SPREADSHEET_ID, new_sheet_name)

    # Add titles to the new sheet
    new_titles = ['Name', 'Location', 'Longitudes', 'Latitudes']
    add_titles_to_sheet(service, SPREADSHEET_ID, new_sheet_name, new_titles)

    # Add values to columns in the new sheet
    add_values_to_sheet_column(service, SPREADSHEET_ID, new_sheet_name, column_a_value, 'A')
    add_values_to_sheet_column(service, SPREADSHEET_ID, new_sheet_name, column_h_value, 'B')

    # Get longitudes and latitudes using the get_location function
    longitudes = []
    latitudes = []

    for location in column_h_value:
        location_result = get_location(location)
        if location_result is not None:
            longitude, latitude = location_result
            longitudes.append(longitude)
            latitudes.append(latitude)

    # Print longitudes and latitudes
    print(f'Longitudes: {longitudes}')
    print(f'Latitudes: {latitudes}')

    # Add longitudes and latitudes to the new sheet
    add_values_to_sheet_column(service, SPREADSHEET_ID, new_sheet_name, longitudes, 'C')
    add_values_to_sheet_column(service, SPREADSHEET_ID, new_sheet_name, latitudes, 'D')

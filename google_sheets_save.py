import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import os
from datetime import datetime
import json

def save_to_google_sheets(user_input, response):
    if user_input:
        try:
            # Load the service account credentials JSON file
            with open("credentials.json", "r") as creds_file:
                creds_dict = json.load(creds_file)

            # Replace the "private_key" value with the environment variable
            creds_dict["private_key"] = os.environ["GSP_PRIVATE_KEY"].replace('\\n', '\n')
            creds_dict["client_email"] = os.environ["GSP_CLIENT_EMAIL"]

            # Authorize using the updated credentials
            credentials = Credentials.from_service_account_info(creds_dict, scopes=[
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ])
            client = gspread.authorize(credentials)

            # Open the Google Sheets document
            spreadsheet = client.open("BaeGPT_inputs")
            worksheet = spreadsheet.get_worksheet(0)  # Assuming the first worksheet

            # Get the current date and time in a sensible string format
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Append the user input to the Google Sheets document
            worksheet.append_row([current_datetime, user_input, response])
            #st.success("Data saved successfully.")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a valid input.")
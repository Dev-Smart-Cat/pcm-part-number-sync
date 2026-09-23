import streamlit as st
import pandas as pd
import re
from utils import open_gsheet, extract_update_cell


try:
    # Call the function to get a worksheet.
    worksheet = open_gsheet()

    def create_df(worksheet):
        """Returns a pandas dataframe.

        From the gspread.worksheet.Worksheet data type obtained with the function open_gsheet().
        Then, pandas DataFrame method converts gspread.worksheet.Worksheet to readable data.

        Argument:
            worksheet (gspread.worksheet.Worksheet): When using the Google Cloud credentials to access a spresheet,
            the function open_gsheet() returns the first sheet as gspread.worksheet.Worksheet data type.

        Return:
            pandas.core.frame.DataFrame: Returns a dataframe with the format from pandas library from
            the gspread.worksheet.Worksheet data type obtained with the function open_gsheet().
        """
        return pd.DataFrame(worksheet.get_all_records())

    # Call the function to convert to dataframe
    df = create_df(worksheet)

    def part_number_input():
        """Returns a text area to input the part number to be extracted.
        The inputted part number is assigned to the variable part_number."""
        part_number = st.text_input("Part Number: ")
        return part_number

    # Call the function to insert the input text area
    part_number = part_number_input()

    def button_to_input_part_number(part_number):
        """Returns a button below the text area. After pressing the button the part number is assigned
        to the variable part_number and then applies the regex pattern.

        As soon as the button is pressed, the part number inputted on the text area
        is assigned to the variable part_number. The part_number inputted becomes a regex pattern,
        so that the part number inputted along with its variations can be extracted from
        column 'OLD PART NUMBER(S)'.

        Arguments:
            part_number (str): The string inputted on the text area on the browser.

        Return:
            regex: Pattern after adding the part number inputted + regex.
            The regex are used to extract the part inputted along with its variations.
            For example:
            inputted part number: 1234
            extracted part numbers: 1234AA, 1234AB, 1234AC
        """
        # Initialize pattern as None
        pattern = None

        if st.button("Part Number Input"):
            if len(part_number) < 8:
                st.write("Please, enter the correct part number.")
            else:
                pattern = fr'((?:\n)?{re.escape(part_number)}[^\s]*)'

        return pattern

    # Call the function insert the button
    pattern = button_to_input_part_number(part_number)

    # Condition to confirm when the button is pressed
    if pattern:
        # Extract the part number and update the hdw column
        extract_update_cell(df, pattern, worksheet)

    # Call the function to get a worksheet after updating hdw column
    worksheet_updated = open_gsheet()

    # Call the function to convert the worksheet to dataframe after updating hdw column
    df_updated = create_df(worksheet_updated)

except Exception as e:
    print(f'Error: {e}')

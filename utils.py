import gspread
import streamlit as st
import re


def open_gsheet():

    """Returns a gspread.worksheet.Worksheet data type.

    It can be used to convert from this data type to a dataframe.

    Arguments:
        json_path: The dir path where .json file with the Google Cloud credentials are stored. 

        gsheet_name: A string with the name of the gsheet.

    Return:
        Returns a gspread.worksheet.Worksheet data type where.
        It can be used to convert from this data type to a dataframe.

    """

    gsheet_name = "df_year_bc_es_extracted"

    gc = gspread.service_account()

    sh = gc.open(gsheet_name)

    worksheet = sh.sheet1

    return worksheet


def extract_update_cell(df, pattern, worksheet):
    """Returns the cell updated on the gsheet with the part numbers extracted from another cell.
    On the browser shows the cell where the part number were extracted along with all matches.

    After remove the part number extracted from the cell where the part number was extracted.

    Argument: 
        df (pandas.core.frame.DataFrame): After opening the gsheet applying the function 'open_gsheet()',
        followed by the conversion of the gspread.worksheet.Worksheet data type to DataFrame using 
        the method .get_all_records().
        pattern (regex): Regex converted from a single string to a pattern, so that the 
        part number along with its variations will be extracted.
        worksheet (gspread.worksheet.Worksheet): The google sheet data type obtained when 
        applying the function open_gsheet().

    Return:
        Returns the cell updated on the gsheet with the part numbers extracted from the column OLD PART NUMBER(S),
        remove the part number extracted from the cell where the part number was extracted.
    """

    for idx, string in df['OLD PART NUMBER(S)'].items():
            # Values from col 'OLD PART NUMBER(S)'
            old_pn_cell = f'E{idx+2}'
            cell_value_to_str = str(string)
            matches = re.findall(pattern, cell_value_to_str)

            # Values from col 'HW'
            hdw_cell = f'D{idx+2}'
            hdw_cell_value = df['HW'][idx]

            # Condition only hdw column has no part number extracted yet
            # and 'None' is on the cell.
            if matches and hdw_cell_value == "None":
                match_out_of_list = ' '.join(matches)
                df['HW'][idx] = str(match_out_of_list)
                worksheet.update(hdw_cell, values=match_out_of_list)
                df['OLD PART NUMBER(S)'][idx] = re.sub(pattern, '', cell_value_to_str)
                cell_removed_pn = df['OLD PART NUMBER(S)'][idx]
                worksheet.update(old_pn_cell, values=cell_removed_pn)
                st.write(f'{old_pn_cell}: {', '.join(matches)}')   

            # Condition when the cell on hdw column is no longer empty.
            elif matches and hdw_cell_value != "None":
                update_hdw_string = f'{df['HW'][idx]} ' + ' '.join(matches)
                df['HW'][idx] = str(update_hdw_string)
                worksheet.update(hdw_cell, values=str(update_hdw_string))
                df['OLD PART NUMBER(S)'][idx] = re.sub(pattern, '', cell_value_to_str)
                cell_removed_pn = df['OLD PART NUMBER(S)'][idx]
                worksheet.update(old_pn_cell, values=cell_removed_pn)
                st.write(f'{old_pn_cell}: {', '.join(matches)}')

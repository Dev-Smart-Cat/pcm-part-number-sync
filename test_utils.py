import pandas as pd
from utils import open_gsheet


def test_open_gsheet():
    worksheet = open_gsheet()
    # Convert the gspread.worksheet.Worksheet data type to pd.DataFrame object
    df = pd.DataFrame(worksheet.get_all_records())
    # Assert the object df is from class pd.Dataframe
    assert isinstance(df, pd.DataFrame)

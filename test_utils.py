import pytest
import gspread
from utils import open_gsheet

def test_open_gsheet():
    gc = gspread.service_account()          # Attempt connection with Google Cloud API
    assert gc is gspread.client.Client      # Assert object of gspread.client.Client 
    


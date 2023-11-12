import pandas as pd
from datetime import datetime
from fda_api import get_pdf_url

def test_get_pdf_url():
    # Test case 1: KNUMBER does not start with "K"
    row = pd.Series({"KNUMBER": "12345", "date": datetime(2022, 1, 1)})
    assert get_pdf_url(row) == None
    
    # Test case 2: Year is greater than 2001
    row = pd.Series({"KNUMBER": "K12345", "date": datetime(2022, 1, 1)})
    assert get_pdf_url(row) == "https://www.accessdata.fda.gov/cdrh_docs/pdf22/k12345.pdf"
    
    # Test case 3: Year is less than or equal to 2001
    row = pd.Series({"KNUMBER": "K12345", "date": datetime(2001, 1, 1)})
    assert get_pdf_url(row) == "https://www.accessdata.fda.gov/cdrh_docs/pdf/k12345.pdf"

    # Test case 4: Year is less than 2001
    row = pd.Series({"KNUMBER": "K12345", "date": datetime(1998, 1, 1)})
    assert get_pdf_url(row) == "https://www.accessdata.fda.gov/cdrh_docs/pdf/k12345.pdf"

    # Test case: Year is 2005
    row = pd.Series({"KNUMBER": "K12345", "date": datetime(2005, 1, 1)})
    assert get_pdf_url(row) == "https://www.accessdata.fda.gov/cdrh_docs/pdf5/k12345.pdf"
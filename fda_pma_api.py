"""
Created at 11/12/2023
Author: Shahryar Doosti

This module is used to fetch and download PMA data from FDA website.
"""

import requests
import os
import pandas as pd
from time import sleep
from tqdm import tqdm

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"Data")

def read_data(file_name = "pma.csv"):
    """
    This function reads the data from the csv file that includes PMA devices from ? to present (2023).
    """
    df = pd.read_csv(os.path.join(DATA_PATH,file_name))
    df['date'] = pd.to_datetime(df['DATERECEIVED'], format='%m/%d/%Y')
    # returing the rows that do not have supplement number for original documents only not the supplements
    return df[df.SUPPLEMENTNUMBER.isnull()]

def get_pdf_url(row):
    """
    This function gets the URL of the PDF file from the dataframe.
    """
    pnumber = row["PMANUMBER"]
    year = row["date"].year
    if pnumber[0] != "P":
        return None
    else:
        if year > 2001:
            year_short = int(year - 2000)
            return f"https://www.accessdata.fda.gov/cdrh_docs/pdf{year_short}/{pnumber.lower()}.pdf"
        else:
            return f"https://www.accessdata.fda.gov/cdrh_docs/pdf/{pnumber.lower()}.pdf"

def pdf_url_list(df):
    """
    This function returns the list of PDF URLs.
    """
    return df.apply(get_pdf_url, axis=1).tolist()

def download_pdf(url, folder_path="pma_pdfs"):
    # if file exists, skip
    if os.path.exists(os.path.join(DATA_PATH, folder_path, url.split("/")[-1])):
        return "File Exists"
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check response code
    if response.status_code != 200:
        if response.status_code == 404:
            return "Not Found"
        else:
            raise Exception(f"Status code: {response.status_code} | {url} is not valid.")
    
    # Extract the filename from the URL
    filename = url.split("/")[-1]
    
    # Save the PDF file in the folder
    with open(os.path.join(DATA_PATH, folder_path, filename), "wb") as f:
        f.write(response.content)
    
    #print(f"PDF file saved in {folder_path}/{filename}")

def download_all_pdfs(df):
    """
    This function downloads all the PDF files from the FDA website.
    """
    # list of URLs that do not exist
    not_exist = []
    urls = pdf_url_list(df)
    for i, url in enumerate(tqdm(urls)):
        if url is not None:
            result = download_pdf(url)
            if result == "Not Found":
                not_exist.append(url)
            sleep(0.5)
        if i % 100 == 0:
            with open(os.path.join(DATA_PATH, "pma_not_exist.txt"), "w") as f:
                f.write("\n".join(not_exist))


if __name__ == "__main__":
    df = read_data()
    download_all_pdfs(df)            

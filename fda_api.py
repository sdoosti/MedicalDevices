"""
Created at 11/10/2023
Author: Shahryar Doosti

This module is used to fetch and download the data from FDA website.
"""

import requests
import os
import pandas as pd
from time import sleep
from tqdm import tqdm

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"Data")

def read_data(file_name = "pmn96cur.csv"):
    """
    This function reads the data from the csv file that includes 510(K) devices from 1996 to present (2023).
    """
    df = pd.read_csv(os.path.join(DATA_PATH,file_name))
    df['date'] = pd.to_datetime(df['DATERECEIVED'], format='%m/%d/%Y')
    return df

def get_pdf_url(row):
    """
    This function gets the URL of the PDF file from the dataframe.
    """
    knumber = row["KNUMBER"]
    year = row["date"].year
    if knumber[0] != "K":
        return None
    else:
        if year > 2001:
            return f"https://www.accessdata.fda.gov/cdrh_docs/pdf{year}/{knumber.lower()}.pdf"
        else:
            return f"https://www.accessdata.fda.gov/cdrh_docs/pdf/{knumber.lower()}.pdf"

def pdf_url_list(df):
    """
    This function returns the list of PDF URLs.
    """
    return df.apply(get_pdf_url, axis=1).tolist()

def download_pdf(url, folder_path="510k_pdfs"):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check response code
    if response.status_code != 200:
        raise Exception(f"Status code: {response.status_code}")
    
    # Extract the filename from the URL
    filename = url.split("/")[-1]
    
    # Save the PDF file in the folder
    with open(os.path.join(DATA_PATH, folder_path, filename), "wb") as f:
        f.write(response.content)
    
    print(f"PDF file saved in {folder_path}/{filename}")

def download_all_pdfs(df):
    """
    This function downloads all the PDF files from the FDA website.
    """
    urls = pdf_url_list(df)
    for url in tqdm(urls):
        if url is not None:
            download_pdf(url)   
            sleep(0.5)

if __name__ == "__main__":
    df = read_data()
    download_all_pdfs(df)            
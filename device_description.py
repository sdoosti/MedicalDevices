import re
import PyPDF2
from fuzzywuzzy import fuzz

def find_device_description(file_path):
    # Open the PDF file in read-binary mode
    with open(file_path, 'rb') as pdf_file:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)

        # Get the number of pages in the PDF document
        num_pages = pdf_reader.getNumPages()

        # Initialize a list to store the section numbers and headers
        sections = []

        # Loop through each page and extract the text
        for page_num in range(num_pages):
            # Get the page object
            page = pdf_reader.getPage(page_num)

            # Extract the text from the page
            text = page.extractText()

            # Use regular expressions to match device description sections
            matches = re.findall(r'^\s*(\d+\.\d+\.\d+)\s+(.*)\s*$', text, re.MULTILINE)

            # If a match is found, check if it's a device description section using fuzzy matching
            for match in matches:
                section_number = match[0]
                section_name = match[1]
                ratio = fuzz.ratio(section_name.lower(), 'device description')
                if ratio >= 80:
                    sections.append((section_number, section_name))

        # If no match is found, return None
        return sections
   
if __name__ == '__main__':
    file_path = 'E:/FDA/510k PDFs (samples)/K092695.pdf'
    sections = find_device_description(file_path)
    for section in sections:
        print(section)

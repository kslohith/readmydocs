import PyPDF2

# Open the PDF file in read-binary mode
with open('evadocs.pdf', 'rb') as pdf_file:
    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # Initialize an empty string to store the extracted text
    extracted_text = ""

    # Iterate through each page in the PDF
    for page_num in range((len(pdf_reader.pages))):
        # Get a specific page
        page = pdf_reader.pages[page_num]

        # Extract text from the page
        page_text = page.extract_text()

        # Append the page text to the overall extracted text
        extracted_text += page_text

# Print or use the extracted text
output_file_path = 'extracted_text.txt'

# Save the extracted text to a text file
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    output_file.write(extracted_text)

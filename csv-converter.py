import PyPDF2
import csv
import os

def csv_to_articles(input_file, output_directory):
    os.makedirs(output_directory, exist_ok=True)

    with open(input_file, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader)  # get the column headers

        for row in reader:
            # Use the 1st column's value (e.g., name) as filename and replace spaces with underscores
            filename = row[2].replace(" ", "_") + ".txt"
            output_file = os.path.join(output_directory, filename)

            with open(output_file, 'w') as out_f:
                for header, value in zip(headers, row):
                    # Write the header and its corresponding value to the output file
                    if len(value) <= 80:
                        out_f.write(f"{header}: {value}\n")
                    else:
                        # Append newline after each period
                        formatted_value = value.replace(". ", ".\n")
                        out_f.write(f"{header}:\n{value}\n\n")

def parse_pdf(pdf_path):
    # Open the PDF file
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        # Iterate through each page and extract text
        for page in reader.pages:
            text += page.extract_text() + "\n"  # Adding a newline for separation between pages
    return text

# Function to process the extracted text and convert it into CSV format
def text_to_csv(text, csv_path):
    # Process the text to extract structured data
    # This step highly depends on the structure of your PDF text
    # For demonstration, let's assume each line in the text is a new row for the CSV and
    # columns are separated by commas in the text

    rows = text.strip().split('\n')  # Split text into rows by new lines
    with open(csv_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        for row in rows:
            columns = row.split(',')  # Assuming columns are separated by commas
            writer.writerow(columns)

if __name__ == "__main__":
    csv_to_articles('input/mirko-feedback-2024.csv', 'output/mirko-feedback-2024/')  # Output directory is current
    # directory, you can adjust this

    # Specify the path to your PDF document and output CSV file
    # pdf_path = 'input/Lin Family.pdf'
    # csv_path = 'output/lin_family.csv'

    # Parse the PDF document
    # text = parse_pdf(pdf_path)

    # Convert the extracted text to CSV
    # text_to_csv(text, csv_path)
    # print(f"Data from '{pdf_path}' has been successfully written to '{csv_path}'")

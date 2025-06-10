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
                        out_f.write(f"{header}:\n{formatted_value}\n\n")


if __name__ == "__main__":
    csv_to_articles('input/mirko-feedback-2024.csv', 'output/mirko-feedback-2024/')

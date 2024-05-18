import csv

csv_path = "data_5.csv"
    # Define the header line to be added
header_line = "moves,c0,c1,c2,c3,c4,c5,c6\n"

    # Read the existing content of the CSV file
with open(csv_path, 'r') as file:
        existing_content = file.read()

    # Write the modified content back to the CSV file
with open(csv_path, 'w') as file:
        # Add the header line at the beginning
    file.write(header_line)
        # Add the existing content after the header line
    file.write(existing_content)

# Example usage:
csv_path = "parsed_data_5.csv"  # Replace with the path to your CSV file

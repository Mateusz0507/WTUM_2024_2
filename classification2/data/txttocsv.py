import csv

# Input and Output file names
input_file = 'data_5_1.txt'
output_file = 'data_5.csv'

# Read data from data.txt and write to data.csv
with open(input_file, 'r') as in_file, open(output_file, 'w', newline='') as out_file:
    # Create a CSV writer object
    csv_writer = csv.writer(out_file)
    
    # Read each line from the input file
    for line in in_file:
        # Remove any leading/trailing whitespaces and split by comma
        row = line.strip().split(',')
        
        # Write the row to the CSV file
        csv_writer.writerow(row)

print(f"Conversion complete. CSV file '{output_file}' has been created.")
# Open the file in read mode
with open("data_5.txt", "r") as file:
    # Read the first 5000 characters
    chunk = file.read(1000000)

    # Count the occurrences of newline characters
    newline_count = chunk.count("\n")

print("Number of newline characters in the first 5000 characters:", newline_count)
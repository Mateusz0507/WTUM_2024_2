chunk_size = 100000

with open("data_5.txt", "r") as input_file:
    with open("data_5_1.txt", "w") as output_file:
        # Initialize count for comma occurrences
        count = 0

        while True:
            # Read a chunk of text
            chunk = input_file.read(chunk_size)
            # If chunk is empty, we've reached the end of the file
            if not chunk:
                break

            # Replace semicolons with commas
            chunk = chunk.replace(";", ",")

            # Replace every eighth comma with a newline character
            result = ""
            for char in chunk:
                if char == ",":
                    count += 1
                    if count % 8 == 0:
                        result += "\n"
                        continue
                result += char
            
            

            # Write the modified chunk to the output file
            output_file.write(result)
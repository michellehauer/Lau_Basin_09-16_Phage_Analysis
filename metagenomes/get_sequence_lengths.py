import os

#ls *.fna > list.list

def get_sequence_lengths(directory):
    output_file = "sequence_lengths.txt"
    with open(output_file, "w") as outfile:
        for filename in os.listdir(directory):
            if filename.endswith(".fna"):
                filepath = os.path.join(directory, filename)
                with open(filepath, "r") as f:
                    lines = f.readlines()
                    sequence = "".join([line.strip() for line in lines if not line.startswith(">")])
                    sequence_length = len(sequence)
                    outfile.write(f"{filename}\t{sequence_length}\n")

# Replace "path/to/directory" with the path to your directory containing fna files
directory_path = "./"
get_sequence_lengths(directory_path)

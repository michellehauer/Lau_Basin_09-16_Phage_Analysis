import os
from Bio import SeqIO

def check_fasta_file(file_path, output_file):
    print(f"Checking file: {file_path}")
    try:
        with open(file_path, "r") as file, open(output_file, "a") as output:
            for record in SeqIO.parse(file, "fasta"):
                header = record.id
                sequence = str(record.seq)
                seq_len = len(sequence)

                # Check header format
                if not header.startswith(">"):
                    output.write(f"Error: Invalid header format in {file_path}: {header}\n")

                # Check sequence length
                if seq_len == 0:
                    output.write(f"Warning: Empty sequence found in {file_path}: {header}\n")
                elif seq_len < 50 or seq_len > 10000:  # Adjust the range as needed
                    output.write(f"Warning: Unexpected sequence length in {file_path}: {header}\n")

    except Exception as e:
        output.write(f"Error reading {file_path}: {str(e)}\n")

# Specify the directory containing your fasta files
input_directory = "./clean"
output_file = "validation_results.txt"

# Iterate through each fasta file in the directory
for filename in os.listdir(input_directory):
    if filename.endswith(".fasta"):
        file_path = os.path.join(input_directory, filename)
        check_fasta_file(file_path, output_file)

print(f"Validation complete. Results saved to {output_file}")

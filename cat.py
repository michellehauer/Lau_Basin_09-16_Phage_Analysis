import os
from Bio import SeqIO

input_directory = "./clean"  # Specify the directory containing your FASTA files
output_file = "./clean/concatenated.fasta"  # Specify the output file

# Open the output file in write mode ("w")
with open(output_file, "w") as output_handle:
    # Iterate through each FASTA file in the directory
    for filename in os.listdir(input_directory):
        if filename.endswith(".fasta"):
            file_path = os.path.join(input_directory, filename)

            # Read the FASTA sequences
            sequences = SeqIO.parse(file_path, "fasta")

            # Write the sequences to the output file with correct formatting
            for seq_record in sequences:
                output_handle.write(f">{seq_record.id}\n{seq_record.seq}\n")

print("Concatenation complete.")

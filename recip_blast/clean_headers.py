import os
from Bio import SeqIO

def modify_headers(input_directory, output_directory):
    for filename in os.listdir(input_directory):
        if filename.endswith(".fasta"):
            input_file = os.path.join(input_directory, filename)
            output_file = os.path.join(output_directory, filename.replace(".fasta", "_modified.fasta"))

            with open(output_file, "w") as output_handle:
                for seq_record in SeqIO.parse(input_file, "fasta"):
                    # Extract sequence identifier
                    sequence_id = seq_record.id.split('|')[0]
                    
                    # Rewrite header without additional characters
                    new_header = f">{sequence_id}"
                    
                    # Write modified sequence to the output file
                    output_handle.write(f"{new_header}\n{seq_record.seq}\n")

# Example usage:
input_directory = "./"
output_directory = "./clean"
modify_headers(input_directory, output_directory)

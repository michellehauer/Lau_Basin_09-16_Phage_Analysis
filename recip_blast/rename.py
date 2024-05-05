import os

def add_filename_to_headers(directory_path):
    # List all files in the directory
    files = [f for f in os.listdir(directory_path) if f.endswith(".fasta") or f.endswith(".fa")]

    # Iterate through each file
    for filename in files:
        file_path = os.path.join(directory_path, filename)

        # Read the content of the file
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Add file name to sequence headers
        new_lines = [f">{filename}_{line[1:]}" if line.startswith('>') else line for line in lines]

        # Write the modified content back to the file
        with open(file_path, 'w') as file:
            file.writelines(new_lines)

if __name__ == "__main__":
    # Replace 'your_directory_path' with the actual path of your directory
    directory_path = '/gpfs/data/rbeinart/mhauer/phage_LauBasin/recipBlast_and_align_phage_with_CRISPR/best_genomes_only/copy'
    add_filename_to_headers(directory_path)

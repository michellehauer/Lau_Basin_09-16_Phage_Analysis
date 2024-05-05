import os

def count_sequences_per_file(directory):
    sequences_per_file = {}

    for filename in os.listdir(directory):
        if filename.endswith(".fa"):
            file_path = os.path.join(directory, filename)
            count = count_sequences_in_file(file_path)
            sequences_per_file[filename] = count

    return sequences_per_file

def count_sequences_in_file(file_path):
    count = 0
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('>'):
                count += 1
    return count

def save_sequence_counts_to_file(sequence_counts, output_file):
    with open(output_file, 'w') as file:
        file.write("Filename\tSequence Count\n")
        for filename, count in sequence_counts.items():
            file.write(f"{filename}\t{count}\n")

if __name__ == "__main__":
    directory = "./"
    output_file = "sequence_counts_per_file.txt"

    sequence_counts = count_sequences_per_file(directory)
    save_sequence_counts_to_file(sequence_counts, output_file)
    print(f"Sequence counts per file saved to {output_file}")

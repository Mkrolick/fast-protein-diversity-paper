from read_database import open_blast_db, get_sequences_from_blast_db
from tokenizer import BPE


# Generates below string!
def find_amino_acids(blast_db, num_sequences=100):
    sequences = get_sequences_from_blast_db(num_sequences)
    sets = [set(s) for s in sequences]
    # Join all sets to get unique amino acids across all sequences
    unique_amino_acids = set().union(*sets)
    # Convert set of amino acids to a sorted string
    amino_acid_string = ''.join(sorted(unique_amino_acids))
    print(amino_acid_string)

# All amino acids!
master_string = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

# Happy four liner!
itos = {idx: char for idx, char in enumerate(master_string)}
stoi = {char: idx for idx, char in enumerate(master_string)}
encode = lambda seq : [stoi[acid] for acid in seq]
decode = lambda ints : ''.join([itos[n] for n in ints])

def convert_amino_acids_to_list(sequences : str) -> list:
    # Append 25 as a start and end token
    ints = [[25] + encode(s) + [25] for s in sequences]
    return ints



if __name__ == "__main__":
    blast_db = open_blast_db()
    next_token = 26
    
    # Get sequences from the database (optionally specify number of sequences)
    sequences = get_sequences_from_blast_db(num_sequences=10) 
    ints = convert_amino_acids_to_list(sequences)

    tokenizer = BPE()
    
    # Run a tokenizer :)

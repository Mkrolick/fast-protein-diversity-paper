from Bio.Blast import NCBIXML
from Bio import SeqIO
from Bio.Blast.Applications import NcbiblastpCommandline
import os
import subprocess
from io import StringIO
import warnings
from Bio import BiopythonWarning

# Silence Biopython deprecation warnings
warnings.filterwarnings('ignore', category=BiopythonWarning)

# Define the path to the SwissProt database
db_path = "/Users/malcolmkrolick/Documents/GitHub/fast-protein-diversity-paper/downloading/downloads/swissprot/swissprot"

def verify_blast_db():
    """Verify that the BLAST database exists and is accessible"""
    required_extensions = ['.phr', '.pin', '.psq']
    for ext in required_extensions:
        if not os.path.exists(db_path + ext):
            raise FileNotFoundError(f"Missing required BLAST database file: {db_path}{ext}")
    return True

def get_sequences_from_blast_db(start=1, num_sequences=None):
    """Get sequences from BLAST database using blastdbcmd"""
    try:
        # Build blastdbcmd command
        cmd = ['blastdbcmd', '-db', db_path, '-entry', 'all']
        if num_sequences:
            # Add range parameter while keeping -entry all
            cmd.extend(['-range', f'{start}-{num_sequences}'])
        
        # Run command and capture output
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise Exception(f"blastdbcmd failed: {result.stderr}")
        
        # Parse the FASTA output
        sequences = list(SeqIO.parse(StringIO(result.stdout), "fasta"))
        return sequences
    
    except Exception as e:
        print(f"Error getting sequences: {str(e)}")
        return None

def open_blast_db():
    """Initialize connection to the BLAST database"""
    try:
        verify_blast_db()
        print("Successfully connected to SwissProt BLAST database")
        print(f"Database location: {db_path}")
        
        # Create a BLAST command line object
        blastp_cline = NcbiblastpCommandline(db=db_path)
        print("BLAST command line interface initialized")
        
        return blastp_cline
    
    except Exception as e:
        print(f"Error opening database: {str(e)}")
        return None

if __name__ == "__main__":
    blast_db = open_blast_db()
    
    # Get sequences from the database (optionally specify number of sequences)
    sequences = get_sequences_from_blast_db(num_sequences=10)  # Get first 10 sequences
    if sequences:
        print(f"Retrieved {len(sequences)} sequences")
        print("First sequence:", sequences[0].id)
        print("First sequence amino acids:", sequences[0].seq)
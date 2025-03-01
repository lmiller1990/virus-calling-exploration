import os
import pandas as pd

def parse_genes(fna_path: str):
    """Extracts gene sequences and computes metrics from a FASTA file."""
    genes = []
    current_gene = []
    
    with open(fna_path) as f:
        for line in f:
            if line.startswith(">"):  # New gene
                if current_gene:  # Save previous gene
                    genes.append("".join(current_gene))
                    current_gene = []
            else:
                current_gene.append(line.strip())
    
    # Add last gene
    if current_gene:
        genes.append("".join(current_gene))

    return genes

def compute_metrics(fna_path: str):
    """Computes various metrics from a FASTA file."""
    genes = parse_genes(fna_path)
    if not genes:
        return {
            "Gene Count": 0,
            "Avg. Gene Length": 0,
            "Min Gene Length": 0,
            "Max Gene Length": 0,
            "Total Nucleotides": 0,
            "GC Content (%)": 0.0,
        }
    
    gene_lengths = [len(gene) for gene in genes]
    total_nucleotides = sum(gene_lengths)
    gc_content = sum(g.count("G") + g.count("C") for g in genes) / total_nucleotides * 100 if total_nucleotides > 0 else 0
    
    return {
        "Gene Count": len(genes),
        "Avg. Gene Length": sum(gene_lengths) / len(genes),
        "Min Gene Length": min(gene_lengths),
        "Max Gene Length": max(gene_lengths),
        "Total Nucleotides": total_nucleotides,
        "GC Content (%)": gc_content,
    }

# Define tools and their directories
tools = {
    "Glimmer": "glimmer_output",
    "Prodigal": "prodigal_output",
    # Add more tools easily
}

# Base file path
relative_fna_path = "hadv_f/genes.fna"

# Collect metrics
data = {}

for tool, dir_name in tools.items():
    file_path = os.path.join(dir_name, relative_fna_path)
    metrics = compute_metrics(file_path)
    
    for metric, value in metrics.items():
        if metric not in data:
            data[metric] = {}
        data[metric][tool] = value

# Create DataFrame
df = pd.DataFrame.from_dict(data, orient="index")

# Print DataFrame
print(df.round(1))


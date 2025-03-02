import os
from typing import Tuple, TypedDict
import re
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
print(df.round(1).to_markdown())

class ParsedGene(TypedDict):
    start: int
    end: int
    sequence: str


def parse_glimmer(fna_path) -> list[ParsedGene]:
    """Parses Glimmer output and extracts genomic coordinates and sequences."""
    genes = []
    with open(fna_path) as f:
        lines = f.readlines()
    
    seq = ""
    for i, line in enumerate(lines):
        if line.startswith(">"):
            if seq:
                genes[-1]["sequence"] = seq  # Store the previous sequence
            seq = ""  # Reset sequence
            
            parts = line.strip().split()
            if len(parts) >= 3:
                start, end = int(parts[1]), int(parts[2])
                genes.append({"start": min(start, end), "end": max(start, end), "sequence": ""})
        else:
            seq += line.strip()
    
    if seq:
        genes[-1]["sequence"] = seq  # Store the last sequence
    
    return genes


def parse_prodigal(fna_path) -> list[ParsedGene]:
    """Parses Prodigal output and extracts genomic coordinates and sequences."""
    genes = []
    with open(fna_path) as f:
        lines = f.readlines()
    
    seq = ""
    for i, line in enumerate(lines):
        if line.startswith(">"):
            if seq:
                genes[-1]["sequence"] = seq  # Store the previous sequence
            seq = ""  # Reset sequence
            
            match = re.search(r"# (\d+) # (\d+) #", line)
            if match:
                start, end = int(match.group(1)), int(match.group(2))
                genes.append({"start": min(start, end), "end": max(start, end), "sequence": ""})
        else:
            seq += line.strip()
    
    if seq:
        genes[-1]["sequence"] = seq  # Store the last sequence
    
    return genes


def write_bed_file(genes: list[ParsedGene], output_path: str, tool_name: str):
    with open(output_path, "w") as bed_file:
        for idx, gene in enumerate(genes):
            start = gene['start']
            end = gene['end']
            # BED format is 0-based, so subtract 1 from start
            bed_file.write(f"contig{idx}\t{start - 1}\t{end}\t{tool_name}_gene{idx}\n")

glimmer_path = "glimmer_output/hadv_f/genes.fna"
prodigal_path = "prodigal_output/hadv_f/genes.fna"

glimmer_genes = parse_glimmer(glimmer_path)
prodigal_genes = parse_prodigal(prodigal_path)

import json

genes = {
    "glimmer": glimmer_genes,
    "prodigal": prodigal_genes,
}

with open("genes.json", "w") as f:
    f.write(json.dumps(genes, indent=4))

def compare_overlapping_genomic_regions():

    write_bed_file(glimmer_genes, "glimmer.bed", "glimmer")
    write_bed_file(prodigal_genes, "prodigal.bed", "prodigal")

compare_overlapping_genomic_regions()


import pandas as pd
import numpy as np

# Define BED files data
# Convert to DataFrame
df_a = pd.DataFrame(glimmer_genes, columns=["start", "end"])
df_b = pd.DataFrame(prodigal_genes, columns=["start", "end"])

# Function to compute intersection length
def compute_intersection(df_a, df_b):
    total_intersection = 0
    total_bases_b = sum(df_b["end"] - df_b["start"])

    for _, (a_start, a_end) in df_a.iterrows():
        for _, (b_start, b_end) in df_b.iterrows():
            overlap_start = max(a_start, b_start)
            overlap_end = min(a_end, b_end)
            if overlap_start < overlap_end:
                total_intersection += (overlap_end - overlap_start)

    return total_intersection, total_bases_b

# Compute
total_intersection, total_bases_b = compute_intersection(df_a, df_b)
percentage_contained = (total_intersection / total_bases_b) * 100

# Output results
print(total_intersection, total_bases_b, percentage_contained)


# import pybedtools
# 
# def calculate_base_pair_overlap():
#     glimmer_bed = pybedtools.BedTool("glimmer.bed")
#     prodigal_bed = pybedtools.BedTool("prodigal.bed")
# 
#     # Compute total base pairs covered by each tool
#     total_glimmer_bp = sum([int(feature.end) - int(feature.start) for feature in glimmer_bed])
#     total_prodigal_bp = sum([int(feature.end) - int(feature.start) for feature in prodigal_bed])
# 
#     # Compute overlapping base pairs
#     overlap = glimmer_bed.intersect(prodigal_bed, wo=True)  # Report base overlap
#     overlapping_bp = sum([int(feature[-1]) for feature in overlap])  # Last column gives overlap length
# 
#     # Compute percentages
#     percent_glimmer_bp_overlap = (overlapping_bp / total_glimmer_bp) * 100 if total_glimmer_bp > 0 else 0
#     percent_prodigal_bp_overlap = (overlapping_bp / total_prodigal_bp) * 100 if total_prodigal_bp > 0 else 0
# 
#     print(f"Total Glimmer base pairs: {total_glimmer_bp}")
#     print(f"Total Prodigal base pairs: {total_prodigal_bp}")
#     print(f"Overlapping base pairs: {overlapping_bp}")
#     print(f"Percentage of Glimmer base pairs overlapping: {percent_glimmer_bp_overlap:.2f}%")
#     print(f"Percentage of Prodigal base pairs overlapping: {percent_prodigal_bp_overlap:.2f}%")
# 
# calculate_base_pair_overlap()
#     

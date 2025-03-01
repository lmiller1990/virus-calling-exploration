import re
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches

def parse_glimmer(fna_path):
    """Parses Glimmer output and extracts genomic coordinates."""
    genes = []
    with open(fna_path) as f:
        for line in f:
            if line.startswith(">"):
                parts = line.strip().split()
                if len(parts) >= 3:
                    start, end = int(parts[1]), int(parts[2])
                    genes.append((start, end))
    return genes

def parse_prodigal(fna_path):
    """Parses Prodigal output and extracts genomic coordinates."""
    genes = []
    with open(fna_path) as f:
        for line in f:
            if line.startswith(">"):
                match = re.search(r"# (\d+) # (\d+) #", line)
                if match:
                    start, end = int(match.group(1)), int(match.group(2))
                    genes.append((start, end))
    return genes


def visualize_genes_with_size_circles(genome_length, glimmer_genes, prodigal_genes):
    """Visualizes gene predictions with circles sized by gene length."""
    fig, ax = plt.subplots(figsize=(12, 4))

    # Increase spacing between Glimmer (y=2) and Prodigal (y=-2)
    for start, end in glimmer_genes:
        radius = abs(start - end)
        center = (start + end) / 2
        circle = patches.Circle((center, 2), radius, color='blue', fill=False, lw=2)
        ax.add_patch(circle)  
        ax.plot([start, end], [2, 2], color='blue', lw=3, label="Glimmer" if 'Glimmer' not in ax.get_legend_handles_labels()[1] else "")

    for start, end in prodigal_genes:
        radius = abs(start - end)
        center = (start + end) / 2
        circle = patches.Circle((center, -2), radius, color='red', fill=False, lw=2)
        ax.add_patch(circle)  
        ax.plot([start, end], [-2, -2], color='red', lw=3, label="Prodigal" if 'Prodigal' not in ax.get_legend_handles_labels()[1] else "")

    ax.set_yticks([-2, 2])
    ax.set_yticklabels(["Prodigal", "Glimmer"])
    ax.set_xlim(0, genome_length)
    ax.set_xlabel("Genome Position (bp)")
    ax.set_title("Gene Predictions on Genome with Size Circles")
    ax.legend()
    plt.show()


# Example usage
genome_length = 34500  # Replace with actual genome length
glimmer_path = "glimmer_output/hadv_f/genes.fna"
prodigal_path = "prodigal_output/hadv_f/genes.fna"

glimmer_genes = parse_glimmer(glimmer_path)
prodigal_genes = parse_prodigal(prodigal_path)

visualize_genes_with_size_circles(genome_length, glimmer_genes, prodigal_genes)


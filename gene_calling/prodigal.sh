rm -rf prodigal_output
mkdir prodigal_output
mkdir prodigal_output/hadv_f

# Adv F
out=prodigal_output/hadv_f
prodigal -i ../hadv_f/GCA_033353495.1_ASM3335349v1_genomic.fna \
        -o "$out/genes.gff" \
        -a "$out/aa.faa" \
        -d "$out/genes.fna"

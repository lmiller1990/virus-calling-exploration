genome="../hadv_f/GCA_033353495.1_ASM3335349v1_genomic.fna"

rm -rf glimmer_output
mkdir -p glimmer_output/hadv_f

echo "Finding long ORFs..."
long-orfs -n "$genome" glimmer_output/hadv_f/long_orfs

# Remove headers and save a cleaned genome file

echo "Building ICM..."
build-icm glimmer_output/hadv_f/icm < "$genome"

echo "Predicting genes"
glimmer3 \
    --linear \
    -o50 -g110 -t30 \
    "$genome" \
    glimmer_output/hadv_f/icm \
    glimmer_output/hadv_f/predicted

# fix - for whatever reason
#
grep -v "^>" glimmer_output/hadv_f/predicted.predict > glimmer_output/hadv_f/predicted_clean.predict

echo "Extract predicted genes"
extract "$genome" glimmer_output/hadv_f/predicted_clean.predict > glimmer_output/hadv_f/genes.fna



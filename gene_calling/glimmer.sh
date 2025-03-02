#!/bin/bash
set -e  # Stop on errors

genome="../hadv_f/GCA_033353495.1_ASM3335349v1_genomic.fna"
output_dir="glimmer_output/hadv_f"

rm -rf "$output_dir"
mkdir -p "$output_dir"

echo "Finding long ORFs..."
long-orfs -n "$genome" "$output_dir/long_orfs"

echo "Merging all available adenovirus genomes for training..."
cat ../hadv_f/*.fna > "$output_dir/training_set.fna"

echo "Building ICM using merged training set..."
build-icm "$output_dir/icm" < "$output_dir/training_set.fna"

echo "Predicting genes..."
glimmer3 \
    --linear \
    -o50 -g110 -t30 \
    "$genome" \
    "$output_dir/icm" \
    "$output_dir/predicted"

# Fix format issue (remove headers)
grep -v "^>" "$output_dir/predicted.predict" > "$output_dir/predicted_clean.predict"

echo "Extracting predicted genes..."
extract "$genome" "$output_dir/predicted_clean.predict" > "$output_dir/genes.fna"

echo "Done!"


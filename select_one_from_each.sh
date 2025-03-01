for dir in $(ls | grep hadv); do
        echo "dir is => $dir"
        cand=$(find $dir -type f -name "*.fna" | shuf | head -n 1) 
        echo "Copying $cand"
        cp $cand "genomes/$dir.fasta"
done

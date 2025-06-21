#!/bin/bash

# Set thread count
THREADS=32
INDEX_SIZE=64GB

# Build minimap2 index
echo "Building minimap2 index..."
minimap2 -I $INDEX_SIZE -t $THREADS -d assembly.mmi assembly.fasta

# Make sure output folder exists
mkdir -p bams

# Loop over reads
for READ in reads/*.fq; do
    BASENAME=$(basename "$READ" .fq)
    echo "Processing $READ..."

    # Align to coassembly
    minimap2 -I $INDEX_SIZE -t $THREADS -ax map-iclr assembly.mmi "$READ" > "$BASENAME.sam"

    # Sort to BAM
    samtools sort -@ $THREADS "$BASENAME.sam" -o "bams/$BASENAME.bam"

    # Index BAM (optional but good for future tools)
    samtools index "bams/$BASENAME.bam"

    # Cleanup SAM to save space
    rm "$BASENAME.sam"
done

# Run jgi_summarize_bam_contig_depths on all BAMs
echo "Generating depth file..."
jgi_summarize_bam_contig_depths --outputDepth assembly_depth.txt bams/*.bam

echo "Done!"
#!/bin/bash

set -euo pipefail

ASSEMBLY="assembly.fasta"
READ_DIR="reads"
BAM_DIR="bams"
THREADS=32

# Create output dir
mkdir -p "$BAM_DIR"

# Build Bowtie2 index if it doesn't exist
if [ ! -f "${ASSEMBLY}.1.bt2" ]; then
    echo "[INFO] Building Bowtie2 index..."
    bowtie2-build "$ASSEMBLY" assembly
fi

# Loop over R1 reads
for R1 in "$READ_DIR"/*_R1*.fq* "$READ_DIR"/*_R1*.fastq*; do
    [ -e "$R1" ] || continue  # Skip if no matches
    SAMPLE=$(basename "$R1" | sed 's/_R1.*//')
    R2="${R1/_R1/_R2}"

    echo "[INFO] Processing sample: $SAMPLE"

    # Align
    bowtie2 -x assembly -1 "$R1" -2 "$R2" -S "$BAM_DIR/$SAMPLE.sam" -p $THREADS

    # Convert, sort, and index
    samtools view -@ $THREADS -bS "$BAM_DIR/$SAMPLE.sam" | \
        samtools sort -@ $THREADS -o "$BAM_DIR/$SAMPLE.sorted.bam"
    samtools index "$BAM_DIR/$SAMPLE.sorted.bam"

    # Cleanup
    rm "$BAM_DIR/$SAMPLE.sam"
done

# Summarize depth for MetaBAT2
echo "[INFO] Generating depth file for MetaBAT2..."
jgi_summarize_bam_contig_depths --outputDepth assembly_depth.txt "$BAM_DIR"/*.sorted.bam

echo "[INFO] Running MetaBAT2..."
metabat2 -i $ASSEMBLY -a assembly_depth.txt -o bins/bin

echo "[✓] All done."

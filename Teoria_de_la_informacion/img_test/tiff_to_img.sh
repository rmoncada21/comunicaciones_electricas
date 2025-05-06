#!/bin/bash
archivos=(*) # obtener todos los archivos en una lista
# echo "${archivos[@]}"

tiff_file=( $(ls | grep tiff) ) # obtener solo los arvhivos .tiff en una lista

echo "${tiff_file[@]}"

for file in "${tiff_file[@]}"; do
    echo "$file ${file}.png"
done
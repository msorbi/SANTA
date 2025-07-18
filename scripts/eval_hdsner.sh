#!/bin/bash

(
# set attributes
dataset_prefix="dataset/hdsner_"

datasets="`echo ${dataset_prefix}*`"

# move to directory and activate evaluation environment
cd hdsner-utils/
conda activate hdsner

# execute on all datasets
for split in dev test
do
    for dataset in ${datasets}
    do
        if [ -d "../${dataset}" ]
        then
            dataset_name="`basename "${dataset}"`"
            pred_file="../save/${dataset_name}/${split}_predictions.txt"
            output_file="../${dataset}/pred_${split}.json"
            python3 src/eval.py \
                --true "../${dataset}/${split}.txt" \
                --pred "${pred_file}" \
                --output "$output_file" \
                --n 1 \
            > /dev/null
            echo "$output_file" # this is going to python below
        fi
    done | python3 src/eval_summary.py --output "../dataset/hdsner_report_${split}.json"
done

# deactivate environment and return to project directory
conda deactivate
cd ..

)

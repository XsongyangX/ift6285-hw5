#!/bin/bash

# Distributes hyperparameter study over a network of DIRO computers

sizes=(60 100 200 300)
windows=(4 5 7 9)
negatives=(4 5 6)

for i in "${sizes[@]}"; do 
    for j in "${windows[@]}"; do
        for k in "${negatives[@]}"; do
            
            pkscreen echo "$i $j $k" > "$i$j$k".txt
        done
    done
done

# execute the training script on a good machine
word2vec() {
    ssh arcade
    ssh ens
    local size=$1
    local window=$2
    local negative=$3
    local log_file="size"$size"_window"$window"_negative$negative"
    {
        time python word2vec.py /u/felipe/HTML/IFT6285-Automne2020/blogs/train \
        --size $size --window $window --negative $negative \
        2> "$log_file".log
    } 2> time_"$log_file".log
    return 0
}
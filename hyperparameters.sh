#!/bin/bash

# Distributes hyperparameter study over a network of DIRO computers

sizes=(60 100 200 300)
windows=(4 5 7 9)
negatives=(4 5 6)

for i in "${sizes[@]}"; do 
    for j in "${windows[@]}"; do
        for k in "${negatives[@]}"; do
            
            pkscreen ssh ens -J arcade bash $PWD/word2vec.sh $i $j $k &
        done
    done
done


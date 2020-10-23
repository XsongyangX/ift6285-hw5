#!/bin/bash

cd ~/ift6285/hw5
size=$1
window=$2
negative=$3
log_file="size"$size"_window"$window"_negative$negative"
{
    time python word2vec.py /u/felipe/HTML/IFT6285-Automne2020/blogs/train \
        --size $size --window $window --negative $negative \
        2>"$log_file".log
} 2>time_"$log_file".log

#!/bin/bash

dir=''

while read p; do
    dir=$(dirname "$p")
    dir=`echo $dir | sed s:^/Volumes/Public/Media/Games/::`
    outputDir="/Volumes/Public/Media/Games/ROM_dupes/$dir"
    mkdir -vp "$outputDir"
    mv -v "$p" "$outputDir"
done < dupes.txt

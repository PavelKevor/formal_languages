#!/bin/sh

GRAMMARS=DataForFLCourse/FullGraph/grammars/'g1'
GRAPHS=([0]=DataForFLCourse/FullGraph/graphs/fullgraph_10 [1]=DataForFLCourse/FullGraph/graphs/fullgraph_50 [3]=DataForFLCourse/FullGraph/graphs/fullgraph_100 [4]=DataForFLCourse/FullGraph/graphs/fullgraph_200 [5]=DataForFLCourse/FullGraph/graphs/fullgraph_500)

for (( i=0; i < 6; i++ ))
do
    for j in $GRAMMARS
    do
        python3 src/benchmark_crfq.py ${GRAPHS[i]} $j
    done
done

GRAMMARS=DataForFLCourse/MemoryAliases/grammars/'g1'
GRAPHS=([0]=DataForFLCourse/MemoryAliases/graphs/bzip2.txt [1]=DataForFLCourse/MemoryAliases/graphs/gzip.txt [2]=DataForFLCourse/MemoryAliases/graphs/ls.txt [3]=DataForFLCourse/MemoryAliases/graphs/pr.txt [4]=DataForFLCourse/MemoryAliases/graphs/wc.txt)
        
for (( i=0; i < 5; i++ ))
do
    for j in $GRAMMARS
    do
        python3 src/benchmark_crfq.py ${GRAPHS[i]} $j
    done
done


GRAMMARS=DataForFLCourse/SparseGraph/grammars/'g1'
GRAPHS=DataForFLCourse/SparseGraph/graphs/'G*'
for i in $GRAPHS
do
    for j in $GRAMMARS
    do
        python3 src/benchmark_crfq.py $i $j
    done
done

GRAMMARS=DataForFLCourse/WorstCase/grammars/'g1'
GRAPHS=DataForFLCourse/WorstCase/graphs/'worstcase_*'
for i in $GRAPHS
do
    for j in $GRAMMARS
    do
        python3 src/benchmark_crfq.py $i $j
    done
done

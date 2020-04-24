#!/bin/bash
#PBS -N REBAGG-SMOTER_61
#PBS -m abe
#PBS -M japheth.hpc.@gmail.com
#PBS -l nodes=1:ppn=1
#PBS -o hpc/REBAGG-SMOTER_61.out
#PBS -e hpc/REBAGG-SMOTER_61.err

cd /home/japheth/tomer_design_hpc

python hpc/REBAGG-SMOTER_61.py
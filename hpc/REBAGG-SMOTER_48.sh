#!/bin/bash
#PBS -N REBAGG-SMOTER_48
#PBS -m abe
#PBS -M japheth.hpc.@gmail.com
#PBS -l nodes=1:ppn=1
#PBS -o hpc/REBAGG-SMOTER_48.out
#PBS -e hpc/REBAGG-SMOTER_48.err

cd /home/japheth/tomer_design_hpc

python hpc/REBAGG-SMOTER_48.py
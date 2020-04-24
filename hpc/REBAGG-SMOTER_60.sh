#!/bin/bash
#PBS -N REBAGG-SMOTER_60
#PBS -m abe
#PBS -M japheth.hpc.@gmail.com
#PBS -l nodes=1:ppn=1
#PBS -o hpc/REBAGG-SMOTER_60.out
#PBS -e hpc/REBAGG-SMOTER_60.err

cd /home/japheth/tomer_design_hpc

python hpc/REBAGG-SMOTER_60.py
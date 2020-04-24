#!/bin/bash
#PBS -N SMOTER_12
#PBS -m abe
#PBS -M japheth.hpc.@gmail.com
#PBS -l nodes=1:ppn=1
#PBS -o hpc/SMOTER_12.out
#PBS -e hpc/SMOTER_12.err

cd /home/japheth/tomer_design_hpc

python hpc/SMOTER_12.py
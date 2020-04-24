#!/bin/bash
#PBS -N SMOTER_11
#PBS -m abe
#PBS -M japheth.hpc.@gmail.com
#PBS -l nodes=1:ppn=1
#PBS -o hpc/SMOTER_11.out
#PBS -e hpc/SMOTER_11.err

cd /home/japheth/tomer_design_hpc

python hpc/SMOTER_11.py
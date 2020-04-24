#!/bin/bash
#PBS -N SMOTER_7
#PBS -m abe
#PBS -M japheth.hpc.@gmail.com
#PBS -l nodes=1:ppn=1
#PBS -o hpc/SMOTER_7.out
#PBS -e hpc/SMOTER_7.err

cd /home/japheth/tomer_design_hpc

python hpc/SMOTER_7.py
#!/bin/bash
#PBS -N SMOTER_25
#PBS -m abe
#PBS -M japheth.hpc.@gmail.com
#PBS -l nodes=1:ppn=1
#PBS -o hpc/SMOTER_25.out
#PBS -e hpc/SMOTER_25.err

cd /home/japheth/tomer_design_hpc

python hpc/SMOTER_25.py
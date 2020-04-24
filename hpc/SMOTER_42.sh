#!/bin/bash
#PBS -N SMOTER_42
#PBS -m abe
#PBS -M japheth.hpc.@gmail.com
#PBS -l nodes=1:ppn=1
#PBS -o hpc/SMOTER_42.out
#PBS -e hpc/SMOTER_42.err

cd /home/japheth/tomer_design_hpc

python hpc/SMOTER_42.py
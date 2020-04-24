#!/bin/bash
#PBS -N SMOTER_15
#PBS -m abe
#PBS -M japheth.hpc.@gmail.com
#PBS -l nodes=1:ppn=1
#PBS -o hpc/SMOTER_15.out
#PBS -e hpc/SMOTER_15.err

cd /home/japheth/tomer_design_hpc

python hpc/SMOTER_15.py
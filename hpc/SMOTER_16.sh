#!/bin/bash
#PBS -N SMOTER_16
#PBS -m abe
#PBS -M japheth.hpc.@gmail.com
#PBS -l nodes=1:ppn=1
#PBS -o hpc/SMOTER_16.out
#PBS -e hpc/SMOTER_16.err

cd /home/japheth/tomer_design_hpc

python hpc/SMOTER_16.py
#!/bin/bash
#PBS -N SMOTER_31
#PBS -m abe
#PBS -M japheth.hpc.@gmail.com
#PBS -l nodes=1:ppn=1
#PBS -o hpc/SMOTER_31.out
#PBS -e hpc/SMOTER_31.err

cd /home/japheth/tomer_design_hpc

python hpc/SMOTER_31.py
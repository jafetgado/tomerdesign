#!/bin/bash
#PBS -N SMOTER_43
#PBS -m abe
#PBS -M japheth.hpc.@gmail.com
#PBS -l nodes=1:ppn=1
#PBS -o hpc/SMOTER_43.out
#PBS -e hpc/SMOTER_43.err

cd /home/japheth/tomer_design_hpc

python hpc/SMOTER_43.py
#!/bin/bash
#PBS -N SMOTER_20
#PBS -m abe
#PBS -M japheth.hpc.@gmail.com
#PBS -l nodes=1:ppn=1
#PBS -o hpc/SMOTER_20.out
#PBS -e hpc/SMOTER_20.err

cd /home/japheth/tomer_design_hpc

python hpc/SMOTER_20.py
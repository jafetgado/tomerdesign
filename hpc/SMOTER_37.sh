#!/bin/bash
#PBS -N SMOTER_37
#PBS -m abe
#PBS -M japheth.hpc.@gmail.com
#PBS -l nodes=1:ppn=1
#PBS -o hpc/SMOTER_37.out
#PBS -e hpc/SMOTER_37.err

cd /home/japheth/tomer_design_hpc

python hpc/SMOTER_37.py
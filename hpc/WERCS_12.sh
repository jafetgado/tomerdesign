#!/bin/bash
#PBS -N WERCS_12
#PBS -m abe
#PBS -M japheth.hpc.@gmail.com
#PBS -l nodes=1:ppn=1
#PBS -o hpc/WERCS_12.out
#PBS -e hpc/WERCS_12.err

cd /home/japheth/tomer_design_hpc

python hpc/WERCS_12.py
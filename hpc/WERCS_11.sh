#!/bin/bash
#PBS -N WERCS_11
#PBS -m abe
#PBS -M japheth.hpc.@gmail.com
#PBS -l nodes=1:ppn=1
#PBS -o hpc/WERCS_11.out
#PBS -e hpc/WERCS_11.err

cd /home/japheth/tomer_design_hpc

python hpc/WERCS_11.py
#!/bin/bash
#PBS -N WERCS_18
#PBS -m abe
#PBS -M japheth.hpc.@gmail.com
#PBS -l nodes=1:ppn=1
#PBS -o hpc/WERCS_18.out
#PBS -e hpc/WERCS_18.err

cd /home/japheth/tomer_design_hpc

python hpc/WERCS_18.py
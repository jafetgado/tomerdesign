#!/bin/bash
#PBS -N WERCS_23
#PBS -m abe
#PBS -M japheth.hpc.@gmail.com
#PBS -l nodes=1:ppn=1
#PBS -o hpc/WERCS_23.out
#PBS -e hpc/WERCS_23.err

cd /home/japheth/tomer_design_hpc

python hpc/WERCS_23.py
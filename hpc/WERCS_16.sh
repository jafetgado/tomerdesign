#!/bin/bash
#PBS -N WERCS_16
#PBS -m abe
#PBS -M japheth.hpc.@gmail.com
#PBS -l nodes=1:ppn=1
#PBS -o hpc/WERCS_16.out
#PBS -e hpc/WERCS_16.err

cd /home/japheth/tomer_design_hpc

python hpc/WERCS_16.py
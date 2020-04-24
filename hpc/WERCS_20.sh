#!/bin/bash
#PBS -N WERCS_20
#PBS -m abe
#PBS -M japheth.hpc.@gmail.com
#PBS -l nodes=1:ppn=1
#PBS -o hpc/WERCS_20.out
#PBS -e hpc/WERCS_20.err

cd /home/japheth/tomer_design_hpc

python hpc/WERCS_20.py
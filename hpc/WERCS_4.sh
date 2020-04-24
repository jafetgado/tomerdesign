#!/bin/bash
#PBS -N WERCS_4
#PBS -m abe
#PBS -M japheth.hpc.@gmail.com
#PBS -l nodes=1:ppn=1
#PBS -o hpc/WERCS_4.out
#PBS -e hpc/WERCS_4.err

cd /home/japheth/tomer_design_hpc

python hpc/WERCS_4.py
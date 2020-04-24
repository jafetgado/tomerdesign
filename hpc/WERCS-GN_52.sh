#!/bin/bash
#PBS -N WERCS-GN_52
#PBS -m abe
#PBS -M japheth.hpc.@gmail.com
#PBS -l nodes=1:ppn=1
#PBS -o hpc/WERCS-GN_52.out
#PBS -e hpc/WERCS-GN_52.err

cd /home/japheth/tomer_design_hpc

python hpc/WERCS-GN_52.py
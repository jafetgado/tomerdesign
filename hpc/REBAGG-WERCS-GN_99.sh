#!/bin/bash
#PBS -N REBAGG-WERCS-GN_99
#PBS -m abe
#PBS -M japheth.hpc.@gmail.com
#PBS -l nodes=1:ppn=1
#PBS -o hpc/REBAGG-WERCS-GN_99.out
#PBS -e hpc/REBAGG-WERCS-GN_99.err

cd /home/japheth/tomer_design_hpc

python hpc/REBAGG-WERCS-GN_99.py
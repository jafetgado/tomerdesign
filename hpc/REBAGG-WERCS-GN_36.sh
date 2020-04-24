#!/bin/bash
#PBS -N REBAGG-WERCS-GN_36
#PBS -m abe
#PBS -M japheth.hpc.@gmail.com
#PBS -l nodes=1:ppn=1
#PBS -o hpc/REBAGG-WERCS-GN_36.out
#PBS -e hpc/REBAGG-WERCS-GN_36.err

cd /home/japheth/tomer_design_hpc

python hpc/REBAGG-WERCS-GN_36.py
#!/bin/bash
#PBS -N REBAGG-WERCS_30
#PBS -m abe
#PBS -M japheth.hpc.@gmail.com
#PBS -l nodes=1:ppn=1
#PBS -o hpc/REBAGG-WERCS_30.out
#PBS -e hpc/REBAGG-WERCS_30.err

cd /home/japheth/tomer_design_hpc

python hpc/REBAGG-WERCS_30.py
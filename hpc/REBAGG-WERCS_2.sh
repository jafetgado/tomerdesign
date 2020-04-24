#!/bin/bash
#PBS -N REBAGG-WERCS_2
#PBS -m abe
#PBS -M japheth.hpc.@gmail.com
#PBS -l nodes=1:ppn=1
#PBS -o hpc/REBAGG-WERCS_2.out
#PBS -e hpc/REBAGG-WERCS_2.err

cd /home/japheth/tomer_design_hpc

python hpc/REBAGG-WERCS_2.py
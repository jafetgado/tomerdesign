#!/bin/bash
#PBS -N REBAGG-WERCS_46
#PBS -m abe
#PBS -M japheth.hpc.@gmail.com
#PBS -l nodes=1:ppn=1
#PBS -o hpc/REBAGG-WERCS_46.out
#PBS -e hpc/REBAGG-WERCS_46.err

cd /home/japheth/tomer_design_hpc

python hpc/REBAGG-WERCS_46.py
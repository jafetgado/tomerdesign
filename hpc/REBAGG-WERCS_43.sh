#!/bin/bash
#PBS -N REBAGG-WERCS_43
#PBS -m abe
#PBS -M japheth.hpc.@gmail.com
#PBS -l nodes=1:ppn=1
#PBS -o hpc/REBAGG-WERCS_43.out
#PBS -e hpc/REBAGG-WERCS_43.err

cd /home/japheth/tomer_design_hpc

python hpc/REBAGG-WERCS_43.py
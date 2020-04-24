#!/bin/bash
#PBS -N REBAGG-GN_12
#PBS -m abe
#PBS -M japheth.hpc.@gmail.com
#PBS -l nodes=1:ppn=1
#PBS -o hpc/REBAGG-GN_12.out
#PBS -e hpc/REBAGG-GN_12.err

cd /home/japheth/tomer_design_hpc

python hpc/REBAGG-GN_12.py
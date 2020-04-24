#!/bin/bash
#PBS -N REBAGG-GN_45
#PBS -m abe
#PBS -M japheth.hpc.@gmail.com
#PBS -l nodes=1:ppn=1
#PBS -o hpc/REBAGG-GN_45.out
#PBS -e hpc/REBAGG-GN_45.err

cd /home/japheth/tomer_design_hpc

python hpc/REBAGG-GN_45.py
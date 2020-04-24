#!/bin/bash
#PBS -N REBAGG-GN_31
#PBS -m abe
#PBS -M japheth.hpc.@gmail.com
#PBS -l nodes=1:ppn=1
#PBS -o hpc/REBAGG-GN_31.out
#PBS -e hpc/REBAGG-GN_31.err

cd /home/japheth/tomer_design_hpc

python hpc/REBAGG-GN_31.py
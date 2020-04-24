#!/bin/bash
#PBS -N GN_12
#PBS -m abe
#PBS -M japheth.hpc.@gmail.com
#PBS -l nodes=1:ppn=1
#PBS -o hpc/GN_12.out
#PBS -e hpc/GN_12.err

cd /home/japheth/tomer_design_hpc

python hpc/GN_12.py
#!/bin/bash
#PBS -N GN_14
#PBS -m abe
#PBS -M japheth.hpc.@gmail.com
#PBS -l nodes=1:ppn=1
#PBS -o hpc/GN_14.out
#PBS -e hpc/GN_14.err

cd /home/japheth/tomer_design_hpc

python hpc/GN_14.py
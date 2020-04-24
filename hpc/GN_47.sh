#!/bin/bash
#PBS -N GN_47
#PBS -m abe
#PBS -M japheth.hpc.@gmail.com
#PBS -l nodes=1:ppn=1
#PBS -o hpc/GN_47.out
#PBS -e hpc/GN_47.err

cd /home/japheth/tomer_design_hpc

python hpc/GN_47.py
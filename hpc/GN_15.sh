#!/bin/bash
#PBS -N GN_15
#PBS -m abe
#PBS -M japheth.hpc.@gmail.com
#PBS -l nodes=1:ppn=1
#PBS -o hpc/GN_15.out
#PBS -e hpc/GN_15.err

cd /home/japheth/tomer_design_hpc

python hpc/GN_15.py
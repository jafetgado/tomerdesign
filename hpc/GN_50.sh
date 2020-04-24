#!/bin/bash
#PBS -N GN_50
#PBS -m abe
#PBS -M japheth.hpc.@gmail.com
#PBS -l nodes=1:ppn=1
#PBS -o hpc/GN_50.out
#PBS -e hpc/GN_50.err

cd /home/japheth/tomer_design_hpc

python hpc/GN_50.py
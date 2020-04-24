#!/bin/bash
#PBS -N GN_25
#PBS -m abe
#PBS -M japheth.hpc.@gmail.com
#PBS -l nodes=1:ppn=1
#PBS -o hpc/GN_25.out
#PBS -e hpc/GN_25.err

cd /home/japheth/tomer_design_hpc

python hpc/GN_25.py
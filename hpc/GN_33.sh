#!/bin/bash
#PBS -N GN_33
#PBS -m abe
#PBS -M japheth.hpc.@gmail.com
#PBS -l nodes=1:ppn=1
#PBS -o hpc/GN_33.out
#PBS -e hpc/GN_33.err

cd /home/japheth/tomer_design_hpc

python hpc/GN_33.py
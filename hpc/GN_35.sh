#!/bin/bash
#PBS -N GN_35
#PBS -m abe
#PBS -M japheth.hpc.@gmail.com
#PBS -l nodes=1:ppn=1
#PBS -o hpc/GN_35.out
#PBS -e hpc/GN_35.err

cd /home/japheth/tomer_design_hpc

python hpc/GN_35.py
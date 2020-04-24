#!/bin/bash
#PBS -N GN_37
#PBS -m abe
#PBS -M japheth.hpc.@gmail.com
#PBS -l nodes=1:ppn=1
#PBS -o hpc/GN_37.out
#PBS -e hpc/GN_37.err

cd /home/japheth/tomer_design_hpc

python hpc/GN_37.py
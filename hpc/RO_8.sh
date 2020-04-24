#!/bin/bash
#PBS -N RO_8
#PBS -m abe
#PBS -M japheth.hpc.@gmail.com
#PBS -l nodes=1:ppn=1
#PBS -o hpc/RO_8.out
#PBS -e hpc/RO_8.err

cd /home/japheth/tomer_design_hpc

python hpc/RO_8.py
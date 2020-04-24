#!/bin/bash
#PBS -N RO_9
#PBS -m abe
#PBS -M japheth.hpc.@gmail.com
#PBS -l nodes=1:ppn=1
#PBS -o hpc/RO_9.out
#PBS -e hpc/RO_9.err

cd /home/japheth/tomer_design_hpc

python hpc/RO_9.py
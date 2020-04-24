#!/bin/bash
#PBS -N REBAGG-RO_12
#PBS -m abe
#PBS -M japheth.hpc.@gmail.com
#PBS -l nodes=1:ppn=1
#PBS -o hpc/REBAGG-RO_12.out
#PBS -e hpc/REBAGG-RO_12.err

cd /home/japheth/tomer_design_hpc

python hpc/REBAGG-RO_12.py
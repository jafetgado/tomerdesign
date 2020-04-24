#!/bin/bash
#PBS -N REBAGG-SMOTER_41
#PBS -m abe
#PBS -M japheth.hpc.@gmail.com
#PBS -l nodes=1:ppn=1
#PBS -o hpc/REBAGG-SMOTER_41.out
#PBS -e hpc/REBAGG-SMOTER_41.err

cd /home/japheth/tomer_design_hpc

python hpc/REBAGG-SMOTER_41.py
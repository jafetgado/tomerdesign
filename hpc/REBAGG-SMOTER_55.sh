#!/bin/bash
#PBS -N REBAGG-SMOTER_55
#PBS -m abe
#PBS -M japheth.hpc.@gmail.com
#PBS -l nodes=1:ppn=1
#PBS -o hpc/REBAGG-SMOTER_55.out
#PBS -e hpc/REBAGG-SMOTER_55.err

cd /home/japheth/tomer_design_hpc

python hpc/REBAGG-SMOTER_55.py
#!/bin/bash
#SBATCH --job-name=mid-flight      
#SBATCH --output=result_%j.out
#SBATCH --error=result_%j.err
#SBATCH --partition=amd
#SBATCH --nodes=1
#SBATCH --ntasks=16
#SBATCH -cpus-per-task=1
#SBATCH --mem=16G
#SBATCH --time=24:00:00

cd ~/OpenFOAM/studentLaunch/poster/alt

python3 ./mesh_solve.py

cd ~/OpenFOAM/studentLaunch/poster/mars

python3 ./mesh_solve.py
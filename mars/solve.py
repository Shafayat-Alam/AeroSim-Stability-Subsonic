#!/usr/bin/env python3
import subprocess
import os

def run_solver():
    if not os.path.exists('logs'): 
        os.makedirs('logs')
    
    # Updated to 14 to match the mesh script/Intruder physical cores
    n_procs = 16 
    
    tasks = [
        ("decomposePar -force", "logs/log.decomposePar"),
        (f"mpirun -np {n_procs} rhoSimpleFoam -parallel", "logs/log.rhoSimpleFoam"),
        ("reconstructPar", "logs/log.reconstructPar")
    ]

    for cmd, log_path in tasks:
        print(f"Executing: {cmd}...")
        try:
            with open(log_path, "w") as log_file:
                subprocess.run(cmd, shell=True, stdout=log_file, stderr=subprocess.STDOUT, check=True)
        except subprocess.CalledProcessError:
            print(f"Error: {cmd} failed. Check {log_path}")
            return

if __name__ == "__main__":
    run_solver()
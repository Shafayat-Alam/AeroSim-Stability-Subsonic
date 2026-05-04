#!/usr/bin/env python3
import os
import subprocess
import shutil
import glob

def run_mesh():
    # 1. Cleanup
    print("Cleaning up old mesh data and logs...")
    for path in glob.glob("processor*"):
        if os.path.isdir(path):
            shutil.rmtree(path)
    
    if os.path.exists('logs'):
        shutil.rmtree('logs')
    os.makedirs('logs')

    # Update to 16 for the supercomputer
    n_procs = 16

    # Step 1: Serial Prep
    prep_commands = [
        ("blockMesh", "logs/log.blockMesh"),
        ("surfaceFeatureExtract", "logs/log.surfaceFeatureExtract"),
        ("decomposePar -force", "logs/log.decomposeParMesh")
    ]

    for cmd, log_path in prep_commands:
        print(f"Running {cmd}...")
        try:
            with open(log_path, "w") as log_file:
                subprocess.run(cmd, shell=True, stdout=log_file, stderr=subprocess.STDOUT, check=True)
        except subprocess.CalledProcessError:
            print(f"Error: {cmd} failed. Check {log_path}")
            return

    # Step 2: Parallel snappyHexMesh
    # On a supercomputer, we usually don't need --oversubscribe or --use-hwthread-cpus
    # because every 'slot' is a physical core.
    print(f"Running snappyHexMesh in parallel on {n_procs} physical cores...")
    snappy_cmd = f"mpirun -np {n_procs} snappyHexMesh -overwrite -parallel"
    
    with open("logs/log.snappyHexMesh", "w") as log_file:
        try:
            subprocess.run(snappy_cmd, shell=True, stdout=log_file, stderr=subprocess.STDOUT, check=True)
        except subprocess.CalledProcessError:
            print("Error: snappyHexMesh failed. Check logs/log.snappyHexMesh for details.")
            return

    # Step 3: Reconstruct mesh
    print("Reconstructing mesh...")
    reconstruct_cmd = "reconstructParMesh -constant"
    with open("logs/log.reconstructParMesh", "w") as log_file:
        try:
            subprocess.run(reconstruct_cmd, shell=True, stdout=log_file, stderr=subprocess.STDOUT, check=True)
        except subprocess.CalledProcessError:
            print("Error: reconstructParMesh failed. Check logs/log.reconstructParMesh")
            return

    print("Mesh generation complete.")

if __name__ == "__main__":
    run_mesh()
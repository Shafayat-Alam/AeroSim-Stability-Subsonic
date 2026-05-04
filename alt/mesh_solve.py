#!/usr/bin/env python3
import subprocess
import os
import stat

# Ensure sub-scripts are executable
for script in ["mesh.py", "solve.py"]:
    if os.path.exists(script):
        st = os.stat(script)
        os.chmod(script, st.st_mode | stat.S_IEXEC)

# Run mesh.py
print("--- Starting Mesh Phase ---")
mesh_result = subprocess.run(["./mesh.py"])
if mesh_result.returncode != 0:
    print(f"mesh.py failed with exit code: {mesh_result.returncode}")
    exit(1)

# Run solve.py
print("\n--- Starting Solver Phase ---")
solve_result = subprocess.run(["./solve.py"])
if solve_result.returncode != 0:
    print(f"solve.py failed with exit code: {solve_result.returncode}")
    exit(1)

print("\nFull CFD workflow completed successfully!")
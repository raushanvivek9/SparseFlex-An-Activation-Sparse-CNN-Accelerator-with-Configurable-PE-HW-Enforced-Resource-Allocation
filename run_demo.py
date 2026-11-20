#!/usr/bin/env python3
"""
SparseFlex: Reconfigurable Activation-Sparse CNN Accelerator
Master Hardware Verification & Demo Runner (Compatible with Windows & Linux/WSL)
"""

import sys
import os
import shutil
import subprocess

def main():
    print("=" * 110)
    print("  SparseFlex: Reconfigurable Activation-Sparse CNN Accelerator -- Master Verification Suite")
    print("  Department of Computer Science and Engineering, Indian Institute of Technology Tirupati")
    print("=" * 110)

    # Check if native iverilog is available
    has_native_iverilog = shutil.which("iverilog") is not None

    if has_native_iverilog:
        # Run directly using native python in the RTL directory
        rtl_dir = os.path.join(os.path.dirname(__file__), "phase2_step1_microarchitecture_and_rtl")
        cmd = [sys.executable, "run_regression.py"]
        return subprocess.run(cmd, cwd=rtl_dir).returncode
    else:
        # Check if WSL is available
        has_wsl = shutil.which("wsl") is not None
        if has_wsl:
            print("[INFO] Native iverilog not found on Windows PATH. Transparently delegating to WSL Ubuntu EDA environment...\n")
            wsl_cmd = "cd /mnt/e/MTech/LanChain/MTP/phase2_step1_microarchitecture_and_rtl && python3 run_regression.py"
            proc = subprocess.run(["wsl", "bash", "-c", wsl_cmd])
            return proc.returncode
        else:
            print("[ERROR] Neither native 'iverilog' nor 'wsl' was detected on PATH.")
            print("Please ensure WSL or Icarus Verilog is installed.")
            return 1

if __name__ == "__main__":
    sys.exit(main())

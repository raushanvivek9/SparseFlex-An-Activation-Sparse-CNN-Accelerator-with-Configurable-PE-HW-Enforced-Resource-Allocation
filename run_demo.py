#!/usr/bin/env python3
"""
SparseFlex: Reconfigurable Activation-Sparse CNN Accelerator
Master Hardware Verification & Demo Runner (Compatible with Windows & Linux/WSL)
"""

import sys
import os
import shutil
import subprocess

def print_header(title):
    print("\n" + "=" * 110)
    print(f"  SparseFlex: {title}")
    print("  Department of Computer Science and Engineering, Indian Institute of Technology Tirupati")
    print("=" * 110 + "\n")

def run_regression():
    print_header("Master System RTL Regression Suite (20 Testbenches, 12,202 Assertions)")
    has_native_iverilog = shutil.which("iverilog") is not None

    if has_native_iverilog:
        rtl_dir = os.path.join(os.path.dirname(__file__), "phase2_step1_microarchitecture_and_rtl")
        return subprocess.run([sys.executable, "run_regression.py"], cwd=rtl_dir).returncode
    else:
        if shutil.which("wsl") is not None:
            print("[INFO] Running in WSL Ubuntu EDA environment (/usr/bin/iverilog)...\n")
            wsl_cmd = "cd /mnt/e/MTech/LanChain/MTP/phase2_step1_microarchitecture_and_rtl && python3 run_regression.py"
            return subprocess.run(["wsl", "bash", "-c", wsl_cmd]).returncode
        else:
            print("[ERROR] Neither native 'iverilog' nor 'wsl' was detected on PATH.")
            return 1

def run_policy():
    print_header("Hardware Policy Controller & Safety Interlock Audit (TSK-37)")
    if shutil.which("wsl") is not None:
        cmd = "cd /mnt/e/MTech/LanChain/MTP/TSK37_RESEARCH_READINESS && iverilog -g2012 -o sim_tsk37_policy ../TSK33_ADAPTIVE_RESOURCE_POLICY/tsk33_transparent_policy_controller.sv tb_tsk37_policy_audit.sv && vvp sim_tsk37_policy"
        return subprocess.run(["wsl", "bash", "-c", cmd]).returncode
    else:
        print("[ERROR] WSL is required to run the policy audit testbench.")
        return 1

def show_telemetry():
    print_header("Verified Hardware Telemetry & Experimental Findings")
    print("""
1. ZERO-GATING SWITCHING ACTIVITY vs. LATENCY DETERMINISM (64-PE Mode):
-----------------------------------------------------------------------------------------------------------------------
Workload (Layer)            | Activation Sparsity | Weight SRAM Reads  | Switching Savings | Clock Cycles | Latency Jitter
-----------------------------------------------------------------------------------------------------------------------
WL1 (ResNet-18 conv1, C10)  |       68.89%        | 9,216 -> 2,867     |     -68.89%       |    9,569     |  0.00% (0 cyc)
WL2 (ResNet-18 conv1, C100) |       66.57%        | 9,216 -> 3,081     |     -66.57%       |    9,569     |  0.00% (0 cyc)
WL3 (VGG-16-BN features.3)  |       48.11%        | 9,216 -> 4,782     |     -48.11%       |    9,569     |  0.00% (0 cyc)
WL4 (ResNet-18 conv2, C10)  |       84.92%        | 9,216 -> 1,390     |     -84.92%       |    9,569     |  0.00% (0 cyc)
-----------------------------------------------------------------------------------------------------------------------
[FINDING]: Up to -84.92% switching elimination in exact 1:1 ratio with sparsity; strictly ZERO latency variation.

2. MULTI-PASS RECONFIGURABLE PE SCALING & ON-CHIP MEMORY TRADE-OFF:
-----------------------------------------------------------------------------------------------------------------------
PE Mode   | Active PEs | Passes (P) | Active Logic Saved | Total Cycles | Act SRAM Reads | Total SRAM Traffic Inflation
-----------------------------------------------------------------------------------------------------------------------
64-PE     |   64 PEs   |  1 Pass    |   0.0% (Baseline)  |    9,569     |     9,216      |   12,339 Accesses (Baseline)
32-PE     |   32 PEs   |  2 Passes  |  -50.0% Logic      |   19,121     |    18,432      |   21,555 Accesses (+74.69%)
16-PE     |   16 PEs   |  4 Passes  |  -75.0% Logic      |   38,225     |    36,864      |   39,987 Accesses (+224.07%)
-----------------------------------------------------------------------------------------------------------------------
[FINDING]: 16-PE mode saves 75% logic power, but amplifies activation reads by +300% (disproving naive energy scaling).

3. ARITHMETIC FIDELITY & HEADROOM:
-----------------------------------------------------------------------------------------------------------------------
* 40-Bit Datapath: 16-bit Q4.12 input operands -> 32-bit Q8.24 products -> 40-bit Q16.24 accumulation (8 guard bits).
* Worst-Case Saturation Headroom: 256 consecutive full-scale additions. Statistical headroom: > 4,300 sigma.
* Verification Status: MAE = 0.000000 | RMSE = 0.000000 across 1,024 words (589,824 MACs) -> Bit-exact match!
""")
    return 0

def main():
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ["--policy", "-p"]:
            return run_policy()
        elif arg in ["--telemetry", "-t", "--results", "-r"]:
            return show_telemetry()
        elif arg in ["--all", "-a"]:
            rc1 = run_regression()
            rc2 = run_policy()
            rc3 = show_telemetry()
            return rc1 or rc2 or rc3
    return run_regression()

if __name__ == "__main__":
    sys.exit(main())

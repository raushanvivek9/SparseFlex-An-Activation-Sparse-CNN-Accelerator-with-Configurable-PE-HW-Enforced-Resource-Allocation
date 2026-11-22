#!/usr/bin/env python3
"""
SparseFlex: Reconfigurable Activation-Sparse CNN Accelerator
Master Hardware Verification & Live Demo Runner (100% True Simulation Execution)
Department of Computer Science and Engineering, Indian Institute of Technology Tirupati
"""

import sys
import os
import shutil
import subprocess

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))

def get_wsl_python():
    """Returns the path to the Python binary in WSL with numpy/pandas installed."""
    return "/mnt/e/MTech/LanChain/MTP/Neural_Acc_env/bin/python"

def run_wsl_command(cmd, description):
    """Executes a command inside WSL and streams output in real time."""
    print("=" * 110)
    print(f"  [LIVE HARDWARE SIMULATION]: {description}")
    print("  Compiler: Icarus Verilog v12.0 (IEEE 1800-2012 SystemVerilog) | Simulator: vvp Engine")
    print("=" * 110 + "\n")
    
    full_cmd = ["wsl", "bash", "-c", cmd]
    res = subprocess.run(full_cmd)
    return res.returncode

def run_regression():
    """Runs the 20-suite master RTL regression suite (12,202 assertions) live."""
    cmd = "cd /mnt/e/MTech/LanChain/MTP/phase2_step1_microarchitecture_and_rtl && python3 run_regression.py"
    return run_wsl_command(cmd, "Master RTL Regression Suite (20 Testbenches, 12,202 Assertions)")

def run_telemetry():
    """Runs the live sparse execution audit computing real hardware telemetry."""
    py_bin = get_wsl_python()
    cmd = f"cd /mnt/e/MTech/LanChain/MTP/TSK37_RESEARCH_READINESS && {py_bin} reproduce_sparse_evidence.py"
    return run_wsl_command(cmd, "Sparse Execution Telemetry & Latency Determinism Audit (Real CNN Layers)")

def run_numerical():
    """Runs live 64-bit independent software convolution reference across 589,824 MACs."""
    py_bin = get_wsl_python()
    cmd = f"cd /mnt/e/MTech/LanChain/MTP/TSK37_RESEARCH_READINESS && {py_bin} reproduce_numerical_evidence.py"
    return run_wsl_command(cmd, "Bit-Exact Numerical Fidelity Verification (MAE & RMSE Calculation)")

def run_policy():
    """Compiles and executes the hardware policy controller testbench across 201 boundary points."""
    cmd = (
        "cd /mnt/e/MTech/LanChain/MTP/TSK37_RESEARCH_READINESS && "
        "iverilog -g2012 -o sim_tsk37_policy ../TSK33_ADAPTIVE_RESOURCE_POLICY/tsk33_transparent_policy_controller.sv tb_tsk37_policy_audit.sv && "
        "vvp sim_tsk37_policy"
    )
    return run_wsl_command(cmd, "Hardware Policy Controller & Single-Cycle Safety Interlock Audit")

def run_sparse_scenarios():
    """Compiles and executes tb_tsk18_sparse_feeder across 10 zero-gating scenarios."""
    cmd = (
        "cd /mnt/e/MTech/LanChain/MTP/phase2_step1_microarchitecture_and_rtl && "
        "iverilog -g2012 -o /tmp/sim_s14 mac_unit_40b.sv pe_array_40b.sv adaptive_pe_controller.sv "
        "ping_pong_buffer_controller.sv hybrid_sram_bank.sv multibank_sram_subsystem.sv dma_controller.sv "
        "layer_command_sequencer.sv dma_to_sram_write_adapter.sv datapath_compute_feeder.sv "
        "ofmap_drain_controller.sv neural_acc_integrated_top.sv tb_tsk18_sparse_feeder.sv && "
        "vvp /tmp/sim_s14; rm -f /tmp/sim_s14"
    )
    return run_wsl_command(cmd, "RTL Sparse Feeder & Zero-Gating Cycle Elimination (10 Real-Time Scenarios)")

def print_usage():
    print("""
==============================================================================================================
  SparseFlex: Master Live Demonstration Runner
  Department of Computer Science and Engineering, Indian Institute of Technology Tirupati
==============================================================================================================
Usage:
  python run_demo.py               Run Master RTL Regression Suite (20 Suites, 12,202 Checks)
  python run_demo.py --telemetry   Run Live CNN Sparsity Telemetry (-84.92% Reads, 0.00% Jitter)
  python run_demo.py --numerical   Run Live Numerical Accuracy & Golden Reference Check (MAE = 0.0)
  python run_demo.py --policy      Run Live Single-Cycle Policy Controller Audit (201/201 Tests)
  python run_demo.py --sparse      Run Live RTL Zero-Gating Scenarios (0% to 100% Sparsity)
  python run_demo.py --all         Execute All 5 Hardware Verification Suites Sequentially
==============================================================================================================
""")

def main():
    if len(sys.argv) == 1:
        return run_regression()

    arg = sys.argv[1].lower().strip()
    if arg in ["--regression", "-reg"]:
        return run_regression()
    elif arg in ["--telemetry", "-t", "--results", "-r"]:
        return run_telemetry()
    elif arg in ["--numerical", "-num", "-n"]:
        return run_numerical()
    elif arg in ["--policy", "-p"]:
        return run_policy()
    elif arg in ["--sparse", "-s", "--feeder"]:
        return run_sparse_scenarios()
    elif arg in ["--all", "-a"]:
        rc1 = run_regression()
        rc2 = run_telemetry()
        rc3 = run_numerical()
        rc4 = run_policy()
        rc5 = run_sparse_scenarios()
        return rc1 or rc2 or rc3 or rc4 or rc5
    elif arg in ["--help", "-h"]:
        print_usage()
        return 0
    else:
        print(f"[ERROR] Unknown option '{arg}'")
        print_usage()
        return 1

if __name__ == "__main__":
    sys.exit(main())

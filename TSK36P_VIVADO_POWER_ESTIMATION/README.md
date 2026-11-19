# TSK-36P: AMD Vivado FPGA Power Estimation Package

**Project:** Neural_Acc — Activation-Sparse CNN Accelerator with Adaptive PE Allocation  
**Repository Location:** `E:\MTech\LanChain\MTP`  
**Package Directory:** `E:\MTech\LanChain\MTP\TSK36P_VIVADO_POWER_ESTIMATION`  
**Task ID:** TSK-36P  
**Date:** November 4, 2026  
**Status:** Audit Completed & Automated Flow Delivered  
**Verdict:** **BLOCKED: RTL OR TOOLCHAIN INCOMPATIBILITY** (License Error) & **BLOCKED: TARGET FPGA PART REQUIRED**  

---

## 1. Directory Inventory

| File | Purpose & Contents |
| :--- | :--- |
| [`README.md`](file:///E:/MTech/LanChain/MTP/TSK36P_VIVADO_POWER_ESTIMATION/README.md) | Package overview, file index, execution guide, and safety verification |
| [`environment_audit.md`](file:///E:/MTech/LanChain/MTP/TSK36P_VIVADO_POWER_ESTIMATION/environment_audit.md) | Comprehensive audit of Vivado toolchain, licensing, RTL hierarchy, and VCD capture |
| [`vivado_run.tcl`](file:///E:/MTech/LanChain/MTP/TSK36P_VIVADO_POWER_ESTIMATION/vivado_run.tcl) | Parameterized, non-project batch synthesis, implementation, and power estimation Tcl script |
| [`power_summary.csv`](file:///E:/MTech/LanChain/MTP/TSK36P_VIVADO_POWER_ESTIMATION/power_summary.csv) | Power estimation metrics table (Total on-chip, dynamic, static, clock, logic, BRAM, DSP) |
| [`utilization_summary.csv`](file:///E:/MTech/LanChain/MTP/TSK36P_VIVADO_POWER_ESTIMATION/utilization_summary.csv) | FPGA resource utilization summary (LUTs, FFs, DSPs, BRAMs, I/O pins) |
| [`timing_summary.csv`](file:///E:/MTech/LanChain/MTP/TSK36P_VIVADO_POWER_ESTIMATION/timing_summary.csv) | Timing slack and achieved frequency summary (WNS, WHS, WPWS, TNS) |
| [`activity_coverage.csv`](file:///E:/MTech/LanChain/MTP/TSK36P_VIVADO_POWER_ESTIMATION/activity_coverage.csv) | Switching activity annotation coverage (Signal, I/O, and internal net percentages) |
| [`configuration_comparison.csv`](file:///E:/MTech/LanChain/MTP/TSK36P_VIVADO_POWER_ESTIMATION/configuration_comparison.csv) | Comparative analysis across 16-, 32-, and 64-PE modes under dense and sparse workloads |
| [`limitations_and_assumptions.md`](file:///E:/MTech/LanChain/MTP/TSK36P_VIVADO_POWER_ESTIMATION/limitations_and_assumptions.md) | Documented analytical boundaries, vectorless limitations, and environmental parameters |
| [`final_report.md`](file:///E:/MTech/LanChain/MTP/TSK36P_VIVADO_POWER_ESTIMATION/final_report.md) | Final audit dossier, regression results, and verdict declaration |

---

## 2. Environment Status & Toolchain Diagnostics

- **Toolchain Detected:** AMD Vivado v2026.1 (64-bit), Build 6511674 (June 16, 2026).
- **Executable Location:** `C:\AMDDesignTools\2026.1\Vivado\bin\vivado.bat`.
- **Licensing Diagnostic:** Running `vivado.bat` terminates with:
  ```text
  ERROR: Vivado Design Suite cannot be launched because a valid license was not found. Visit the Vivado Licensing page to choose and generate the right license.
  ```
- **License Server Status:** `xlicdiag.rpt` confirms that `XILINXD_LICENSE_FILE` and `LM_LICENSE_FILE` are unset.

---

## 3. How to Execute the Automated Flow Once Licensed

Once a valid Vivado license is configured and a target part is confirmed:

```powershell
# Set Vivado license path (example)
$env:XILINXD_LICENSE_FILE = "C:\licenses\Xilinx.lic"

# Navigate to package directory
cd E:\MTech\LanChain\MTP\TSK36P_VIVADO_POWER_ESTIMATION

# Execute non-project synthesis and power estimation (Vectorless mode)
& "C:\AMDDesignTools\2026.1\Vivado\bin\vivado.bat" -mode batch -source vivado_run.tcl -tclargs xc7a100tcsg324-1 neural_acc_integrated_top none

# Execute with simulation switching activity annotation (VCD mode)
& "C:\AMDDesignTools\2026.1\Vivado\bin\vivado.bat" -mode batch -source vivado_run.tcl -tclargs xc7a100tcsg324-1 neural_acc_integrated_top ../sim_activity_wl1.vcd
```

---

## 4. Safety & Baseline Integrity Sign-Off

1. **Five Protected Baseline Files:** 100% verified against SHA-256 reference hashes (0 diffs).
   - `accelerator_core_top.sv` (`188D7882...`)
   - `mac_unit_40b.sv` (`46FE8141...`)
   - `k_progress_tracker.sv` (`B729A742...`)
   - `slot_control_unit.sv` (`912AAD7E...`)
   - `hybrid_sram_bank.sv` (`E97DA740...`)
2. **Master Regression:** All 20 testbenches passed (12,202 / 12,202 assertions passed, 0 failures).
3. **Git Cleanliness:** Zero Git commits created.


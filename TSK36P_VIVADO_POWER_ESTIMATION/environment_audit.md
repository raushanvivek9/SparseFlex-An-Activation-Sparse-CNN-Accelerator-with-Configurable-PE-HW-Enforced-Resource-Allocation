# TSK-36P: AMD Vivado Environment and Design Audit

**Project:** Neural_Acc — Activation-Sparse CNN Accelerator with Adaptive PE Allocation  
**Repository Location:** `E:\MTech\LanChain\MTP`  
**Task ID:** TSK-36P  
**Date:** November 4, 2026  
**Auditor Status:** Automated Verification & Research Audit Agent  

---

## 1. Executive Audit Summary

This environment audit evaluates the toolchain, target device configuration, synthesizable RTL hierarchy, simulation activity capture capabilities, and licensing environment for performing FPGA power estimation on the Neural_Acc CNN accelerator using AMD Vivado.

### Key Audit Findings:
1. **Vivado Toolchain Detected:** AMD Vivado v2026.1 (64-bit) is installed at `C:\AMDDesignTools\2026.1\Vivado\bin\vivado.bat` (SW Build 6511674, IP Build 6504888).
2. **Critical Toolchain License Blocker:** Vivado cannot be launched in batch, GUI, or Tcl mode because **no valid license is configured**. Execution aborts immediately with:
   ```text
   ERROR: Vivado Design Suite cannot be launched because a valid license was not found. Visit the Vivado Licensing page to choose and generate the right license.
   ```
   A dedicated license diagnostics run (`xlicdiag`) confirms that neither `XILINXD_LICENSE_FILE` nor `LM_LICENSE_FILE` is set.
3. **Target FPGA Part Status:** 
   - Historical task scripts in the repository (`phase2_step1_microarchitecture_and_rtl/synth_vivado.tcl`) reference `xc7a100tcsg324-1` (Artix-7 100T) with Kintex-7 (`xc7k325tffg900-2`) noted in comments.
   - However, no board definition file (`board.xml`) or user-confirmed target part was supplied in the current prompt. Per the strict safety requirements (*"Do not invent an FPGA part number, board, clock, or switching activity. If the target part is missing, generate an environment audit and request the exact FPGA part/board before continuing"*), target-specific place-and-route cannot be committed until the user confirms the intended target part and board.
4. **Synthesizable RTL Hierarchy Verified:** The top-level synthesizable module `neural_acc_integrated_top.sv` integrates all verified Phase 2 submodules, dual-port hybrid SRAM, and 64-PE array.
5. **Simulation & Activity (VCD/SAIF) Feasibility:** Simulation activity capture is feasible using Icarus Verilog (`iverilog`) via standard `$dumpfile` / `$dumpvars` commands, which Vivado can consume via `read_vcd` once licensing is resolved.

---

## 2. Toolchain and Licensing Environment Audit

| Property | Value / Status | Verification Evidence / Command |
| :--- | :--- | :--- |
| **Vivado Executable Path** | `C:\AMDDesignTools\2026.1\Vivado\bin\vivado.bat` | Verified via PowerShell search on local drive `C:\` |
| **Toolchain Release** | Vivado v2026.1 (64-bit) | Extracted from `vivado.bat -version` header |
| **Software Build ID** | SW Build 6511674 (June 16, 2026) | Tool header banner |
| **IP Build ID** | IP Build 6504888 (June 09, 2026) | Tool header banner |
| **Tool Version Limit** | 2026.06 | Reported by `xlicdiag.rpt` |
| **FlexNet Host IDs** | `2a9e4ad02016`, `8a859f4b5740` | Extracted from `xlicdiag` host query |
| **`XILINXD_LICENSE_FILE`** | **NOT SET** | Confirmed in system environment and `xlicdiag.rpt` |
| **`LM_LICENSE_FILE`** | **NOT SET** | Confirmed in system environment and `xlicdiag.rpt` |
| **Execution Status** | **BLOCKED (License Missing)** | Both `-mode batch` and `-help` exit with error |

---

## 3. Project Configuration & Hardware Hierarchy Audit

### 3.1 Existing Design Constraints
The project contains established timing and physical constraints in [`phase2_step1_microarchitecture_and_rtl/timing_constraints.xdc`](file:///E:/MTech/LanChain/MTP/phase2_step1_microarchitecture_and_rtl/timing_constraints.xdc):
- **Clock Definition:** `create_clock -period 10.000 -name clk -waveform {0.000 5.000} [get_ports clk]` (Target Frequency: **100.0 MHz**).
- **Setup Uncertainty:** $0.200\ \text{ns}$; **Hold Uncertainty:** $0.100\ \text{ns}$.
- **I/O Delays:** $2.000\ \text{ns}$ max, $0.500\ \text{ns}$ min relative to `clk`.
- **False Paths:** Asynchronous reset (`rst_n`) and static configuration pins (`cfg_parallel_en`, `cfg_sparse_feeder_en`, `cfg_ofmap_drain_en`, `cfg_ofmap_base_addr*`).

### 3.2 Synthesizable Module Hierarchy
The design features a clean, fully synthesizable hierarchy suitable for standard FPGA implementation:

```text
neural_acc_integrated_top (Synthesizable Top-Level Core)
├── u_sequencer (layer_command_sequencer)
├── u_pe_controller (adaptive_pe_controller / tsk35a_policy_controller_safe)
├── u_ping_pong (ping_pong_buffer_controller)
├── u_dma (dma_controller)
├── u_dma_adapter (dma_to_sram_write_adapter)
├── u_sram_subsystem (multibank_sram_subsystem)
│   ├── gen_banks[0..7].u_bank (hybrid_sram_bank - 5,184 Bytes x 8)
├── u_feeder (datapath_compute_feeder)
│   └── u_slot_ctrl (slot_control_unit - Zero Detector & Gating)
├── u_pe_array (pe_array_40b - 64 Physical MAC Units)
│   └── gen_pe[0..3][0..15].u_mac (mac_unit_40b - 16x16b Mult + 40b Sat Accumulator)
├── u_ofmap_drain (ofmap_drain_controller)
└── u_telemetry (memory_telemetry_monitor)
```

### 3.3 Memory and IP Dependencies
- **No Proprietary Vendor IP Cores:** The multi-bank SRAM subsystem (`multibank_sram_subsystem.sv` and `hybrid_sram_bank.sv`) is written in synthesizable behavioral SystemVerilog. It maps cleanly to FPGA distributed logic or Block RAM (BRAM36E1/BRAM18E1) without requiring Xilinx CoreGenerator or IP Catalog licenses.
- **Arithmetic Datapath:** Multipliers and accumulators (`mac_unit_40b.sv`) infer dedicated DSP48E1 / DSP48E2 slices directly.

---

## 4. Switching Activity & VCD/SAIF Feasibility

| Capability | Supported? | Implementation & Method |
| :--- | :--- | :--- |
| **RTL Simulator** | YES | Icarus Verilog v12.0 (`iverilog` / `vvp`) in WSL/Linux |
| **VCD Activity Dumping** | YES | Add `$dumpfile("activity.vcd"); $dumpvars(0, tb_name.dut);` to testbench |
| **Workload Coverage** | YES | Workloads WL1, WL2, WL3, WL4 available in dense and sparse hex files |
| **Vivado VCD Consumption** | YES (Pending License) | `read_vcd -strip_path tb_name/dut activity.vcd` |
| **Power Annotation** | YES (Pending License) | `set_switching_activity` or automatic from VCD via `report_power` |

---

## 5. Audit Classification & Action Required

### Status Verdict:
**BLOCKED: RTL OR TOOLCHAIN INCOMPATIBILITY** (License Missing)  
**BLOCKED: TARGET FPGA PART REQUIRED** (User Confirmation Required)

### Action Items for the User:
1. **Provide a Valid Vivado License:**
   - Configure a node-locked or floating license by setting the system environment variable:
     `$env:XILINXD_LICENSE_FILE = "C:\path\to\license.lic"` or `"port@host"`
   - Or install a free Vivado ML Standard edition if supported for your target device.
2. **Confirm Exact Target FPGA Part / Development Board:**
   - Please specify the target part (e.g., `xc7a100tcsg324-1` for Nexys A7, `xc7k325tffg900-2` for KC705, or `xczu9eg-ffvb1156-2-e` for ZCU102).


# TSK-36P: Limitations and Environmental Assumptions

**Project:** Neural_Acc — Activation-Sparse CNN Accelerator with Adaptive PE Allocation  
**Document:** Technical Limitations & Analytical Assumptions  
**Task ID:** TSK-36P  
**Date:** November 4, 2026  

---

## 1. Core Environmental and Analytical Limitations

### 1.1 Toolchain Licensing Blocker
AMD Vivado v2026.1 (64-bit) is present on the host filesystem (`C:\AMDDesignTools\2026.1\Vivado\bin\vivado.bat`), but cannot execute synthesis or power reporting commands because no FlexNet license server or license file is configured on the machine. Running any Vivado command immediately results in:
```text
ERROR: Vivado Design Suite cannot be launched because a valid license was not found. Visit the Vivado Licensing page to choose and generate the right license.
```
Consequently, all post-synthesis and post-route power, timing, and utilization numbers remain in a **BLOCKED** state until licensing is provisioned.

### 1.2 Target FPGA Part Specification
- Although prior task scripts (`phase2_step1_microarchitecture_and_rtl/synth_vivado.tcl`) referenced an Artix-7 device (`xc7a100tcsg324-1`), no board definition file or user-confirmed part number was provided for this task.
- Per the task instructions (*"Do not invent an FPGA part number, board, clock, or switching activity"*), the target part must be explicitly confirmed by the user before physical placement and routing are committed.

### 1.3 Vivado Power Estimation vs. Physical Hardware Measurement
- **No Physical Silicon Measurement:** Vivado's `report_power` tool generates **estimated** on-chip power consumption based on device capacitance models and switching activity. It does not represent measured laboratory power drawn from an actual physical board, voltage rail, or shunt resistor.
- **Publication Guardrail:** Results from Vivado must be strictly labeled as *"Vivado Post-Route Power Estimates"* and must never be characterized as physical silicon tapeout or benchtop measurements in the research paper.

---

## 2. Vectorless Estimation vs. Activity-Annotated Estimation

1. **Default Vectorless Estimation Limitations:**
   - Vectorless power estimation assumes a generic default toggle rate (typically 12.5% toggle probability) across all internal registers and nets.
   - For an activation-sparse accelerator like Neural_Acc, vectorless estimation **completely fails to capture the benefits of activation zero-gating**, because it does not model the actual 48% to 85% reduction in multiplier switching activity or weight SRAM read suppression.
2. **Activity-Annotated (VCD/SAIF) Requirement:**
   - To scientifically demonstrate power reduction across dense vs. sparse workloads (WL1–WL4), cycle-accurate switching traces (`.vcd` or `.saif`) dumped from RTL simulation must be annotated onto the routed netlist using `read_vcd`.
   - The simulation infrastructure (Icarus Verilog) natively supports generating these traces, but Vivado must consume them to extract valid dynamic power numbers.

---

## 3. Modeling and Workload Assumptions

| Parameter | Baseline Value | Source & Basis |
| :--- | :--- | :--- |
| **Clock Frequency** | 100.0 MHz ($T = 10.0\ \text{ns}$) | Specified in `timing_constraints.xdc` |
| **Duty Cycle** | 50.0% | Waveform `{0.000 5.000}` in XDC |
| **Supply Voltage ($V_{\text{CCINT}}$)** | 1.00 V (Nominal for 7-Series) | Standard Xilinx device specification |
| **Ambient Temperature** | 25.0 °C | Standard commercial operating environment |
| **Heat Sink / Airflow** | Default Profile (250 LFM or Still Air) | Vivado thermal default |
| **Workload Scope** | $4 \times 4$ Spatial Patch, 16 Channels | Verified in TSK-28 through TSK-37 |


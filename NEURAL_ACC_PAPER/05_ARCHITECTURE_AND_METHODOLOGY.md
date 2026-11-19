# Phase 5: Architecture, Implementation, and Methodology

**Project:** Neural_Acc — Activation-Sparse CNN Accelerator with Adaptive PE Allocation  
**Document:** `05_ARCHITECTURE_AND_METHODOLOGY.md`  
**Date:** November 4, 2026  

---

# 1. System Microarchitecture Overview

The `Neural_Acc` accelerator is implemented in parameterizable, cycle-accurate SystemVerilog. The microarchitecture is partitioned into five tightly coupled subsystems:
1. **Integrated Top & Command Sequencer (`neural_acc_integrated_top.sv`, `layer_command_sequencer.sv`):** Interprets layer dispatch descriptors, tracks tile and channel progression, and coordinates hardware phase handshakes.
2. **Transparent Hardware Policy Controller (`tsk33_transparent_policy_controller.sv`):** Evaluates host-supplied latency budgets and PE caps in a single clock cycle, resolving the active PE configuration and asserting safety interlocks.
3. **Multi-Bank Hybrid SRAM Subsystem (`multibank_sram_subsystem.sv`, `hybrid_sram_bank.sv`):** Multi-ported on-chip memory banks providing parallel, conflict-free operand delivery for activations and weights.
4. **Activation-Sparse Datapath Feeder (`datapath_compute_feeder.sv`):** Performs synchronous zero-activation inspection, generating selective clock-enables and weight-memory read strobes.
5. **Configurable 40-bit PE Array & Accumulator (`pe_array_40b.sv`, `mac_unit_40b.sv`):** Array of up to 64 saturating Multiply-Accumulate units with 40-bit internal accumulation depth.

```mermaid
graph TD
    subgraph Host / SoC Interface
        Host["Host CPU / SoC Master"]
        CmdFIFO["Layer Command FIFO"]
    end

    subgraph Control & Arbitration
        PolicyCtrl["Hardware Policy Controller<br/>(Policy A / B Arbitrator)"]
        Seq["Layer Command Sequencer<br/>(Tile & Pass State Machine)"]
        KTracker["K-Progress Tracker<br/>(K=576 Counter)"]
    end

    subgraph Memory Hierarchy
        ActSRAM["Activation Multi-Bank SRAM<br/>(Ping-Pong Bank Pairs)"]
        WtSRAM["Weight Multi-Bank SRAM<br/>(Parallel Sub-Banks)"]
        DrainCtrl["OFMAP Drain Controller<br/>(Requantization & Writeback)"]
    end

    subgraph Datapath & Execution
        ZeroDetect["Datapath Compute Feeder<br/>(Zero-Activation Detection)"]
        PEArray["Configurable 40-bit PE Array<br/>(16 / 32 / 64 Saturating PEs)"]
    end

    Host -->|Layer Parameters, Budget, Cap| CmdFIFO
    CmdFIFO --> PolicyCtrl
    PolicyCtrl -->|Resolved Mode, Exec Enable, Passes| Seq
    Seq --> KTracker
    Seq --> ActSRAM
    Seq --> WtSRAM
    ActSRAM --> ZeroDetect
    ZeroDetect -->|Clock Enable / Strobe Suppression| WtSRAM
    ZeroDetect -->|Unmasked Operands| PEArray
    WtSRAM -->|Weights (if Act != 0)| PEArray
    PEArray -->|Accumulated OFMAPs| DrainCtrl
    DrainCtrl --> Host
```

---

# 2. Configurable PE Array and Multi-Pass Execution

## 2.1 PE Operating Modes
The processing element array consists of 64 identical 40-bit MAC units organized into four 16-PE clusters:
- **64-PE Mode (`resolved_pe_mode = 2'b10`):** All 64 PEs are enabled. The array computes all 16 output channels concurrently in a single pass ($P = 1$).
- **32-PE Mode (`resolved_pe_mode = 2'b01`):** Two clusters (32 PEs) are active; the remaining 32 PEs are clock-gated. Execution requires two sequential passes ($P = 2$), computing 8 output channels per pass.
- **16-PE Mode (`resolved_pe_mode = 2'b00`):** One cluster (16 PEs) is active; 48 PEs are clock-gated. Execution requires four sequential passes ($P = 4$), computing 4 output channels per pass.

## 2.2 Execution Latency Formulations
For a representative workload evaluating a $4 \times 4$ spatial grid (16 tiles) over reduction depth $K = 576$ (organized as 9 chunks of 64 elements each), the execution cycle counts are governed by exact hardware equations:

$$\text{Compute Cycles} = P \times (16 \text{ tiles} \times 9 \text{ chunks} \times 64 \text{ terms}) = P \times 9,216 \text{ cycles}$$

$$\text{Overhead Cycles} = 1 \text{ (setup)} + P \times \left(9 \text{ chunks} \times 32 \text{ barrier/switch} + 64 \text{ drain}\right)$$

Evaluating for each mode yields:
- **64-PE Mode ($P=1$):** $9,216 \text{ compute} + 353 \text{ overhead} = \mathbf{9,569 \text{ cycles}}$ ($95.69\ \mu\text{s}$ at 100 MHz).
- **32-PE Mode ($P=2$):** $18,432 \text{ compute} + 689 \text{ overhead} = \mathbf{19,121 \text{ cycles}}$ ($191.21\ \mu\text{s}$ at 100 MHz).
- **16-PE Mode ($P=4$):** $36,864 \text{ compute} + 1,361 \text{ overhead} = \mathbf{38,225 \text{ cycles}}$ ($382.25\ \mu\text{s}$ at 100 MHz).

The execution cycles scale deterministically by exactly $2.00\times$ (32-PE) and $4.00\times$ (16-PE) relative to the 64-PE baseline.

---

# 3. Activation-Sparse Execution Mechanism

## 3.1 Zero-Detection and Clock Gating
Convolutional activation tensors contain a large proportion of zeros post-ReLU. The `datapath_compute_feeder.sv` inspects the 16-bit signed activation operand $A_{i}$ prior to issuing memory read requests for the corresponding weight $W_{i, c}$:

$$\text{zero\_active} = (A_{i} == 16'h0000)$$

When $\text{zero\_active}$ is true:
1. **Weight SRAM Read Suppression:** The weight SRAM chip-select and output enable signals (`wt_sram_ren`) are deasserted, preventing the weight memory bank from discharging its internal bitlines.
2. **MAC Clock Enable Suppression:** The clock enable signal (`mac_ce`) to the target MAC unit is deasserted, freezing the 40-bit internal accumulator and preventing dynamic toggle activity in the multiplier carry-save array.

## 3.2 Synchronous Stepping Guarantee
Crucially, **`Neural_Acc` maintains strict synchronous pipeline progression**. The `k_progress_tracker` and tile counters increment on every clock cycle regardless of $\text{zero\_active}$. 

*Architectural Distinction:* Unlike asynchronous architectures (e.g., Cnvlutin, Cambricon-X) that collapse zero cycles using queue buffers, `Neural_Acc` sacrifices latency compression to achieve **guaranteed cycle-deterministic timing**. Zero activations eliminate dynamic switching power and SRAM read power, but total execution cycles remain invariant ($0.00\%$ latency change).

---

# 4. Hardware Resource Allocation Policies

The `tsk33_transparent_policy_controller.sv` evaluates three host inputs on the clock edge: `policy_select`, `latency_budget_cycles` ($L_{\text{budget}}$), and `max_active_pe_limit` ($P_{\max}$).

## 4.1 Policy A: Minimum Resource Allocation
Policy A minimizes instantaneous active PE logic footprint, satisfying the latency budget with the smallest feasible PE configuration:

$$\text{PE}_{\text{selected}} = \begin{cases}
16 \text{ PEs}, & \text{if } P_{\max} \ge 16 \text{ and } L_{\text{budget}} \ge 38,225 \\
32 \text{ PEs}, & \text{else if } P_{\max} \ge 32 \text{ and } L_{\text{budget}} \ge 19,121 \\
64 \text{ PEs}, & \text{else if } P_{\max} \ge 64 \text{ and } L_{\text{budget}} \ge 9,569 \\
\text{Fallback}(P_{\max}), & \text{otherwise (assert } \text{budget\_violation})
\end{cases}$$

When the latency budget allows 38,225 cycles, Policy A allocates 16 PEs, reducing active datapath logic by **75.0%**.

## 4.2 Policy B: Maximum Performance
Policy B maximizes throughput, selecting the largest PE configuration permitted by the resource cap:

$$\text{PE}_{\text{selected}} = \begin{cases}
64 \text{ PEs}, & \text{if } P_{\max} \ge 64 \text{ and } L_{\text{budget}} \ge 9,569 \\
32 \text{ PEs}, & \text{else if } P_{\max} \ge 32 \text{ and } L_{\text{budget}} \ge 19,121 \\
16 \text{ PEs}, & \text{else if } P_{\max} \ge 16 \text{ and } L_{\text{budget}} \ge 38,225 \\
\text{Fallback}(P_{\max}), & \text{otherwise (assert } \text{budget\_violation})
\end{cases}$$

## 4.3 Hardware Safety Interlocks and Gating
If the host specifies an infeasible resource cap ($P_{\max} < 16$):
1. The controller immediately drives `invalid_pe_limit = 1` and `execution_enable = 0`.
2. The mode bits are forced to `resolved_pe_mode = 2'b11` (invalid/halt state).
3. The downstream command sequencer positively inhibits execution dispatch, generating zero `compute_start` pulses.
4. If a valid configuration is presented on the subsequent cycle, the controller recovers cleanly in a single clock cycle without requiring a system-level reset.

---

# 5. Fixed-Point Numerical Representation & Quantization

To ensure numerical stability across deep accumulation, `Neural_Acc` employs:
- **Input Operands:** 16-bit signed fixed-point integers formatted as **Q4.12** (1 sign bit, 3 integer bits, 12 fractional bits), providing dynamic range $[-8.0, +7.999755]$ with resolution $2^{-12} \approx 2.44 \times 10^{-4}$.
- **Accumulator Datapath:** 40-bit signed accumulator (`mac_unit_40b.sv`). A 16-bit by 16-bit multiplication produces a 32-bit signed product (Q8.24). Accumulating over reduction depth $K = 576$ requires $\lceil \log_2(576) \rceil = 10$ guard bits. The 40-bit accumulator provides 8 guard bits above the product, accommodating up to 256 full-scale additions without overflow.
- **Saturation Behavior:** If an accumulation exceeds $[-2^{39}, +2^{39}-1]$, the hardware saturates symmetrically to the maximum representable signed boundary.
- **Requantization Unit (`requantization_unit.sv`):** Following accumulation, the 40-bit result is arithmetic-right-shifted by 12 bits and saturated back to signed 16-bit format for OFMAP writeback.

---

# 6. Experimental Methodology

## 6.1 CNN Workload Selection and Provenance
Four representative convolutional workloads were extracted from canonical PyTorch models pretrained on CIFAR datasets:
1. **WL1:** ResNet-18 `layer1.0.conv1` on CIFAR-10 ($3 \times 3$ kernel, 64 input channels, 64 output channels, post-ReLU sparsity = 68.89%).
2. **WL2:** ResNet-18 `layer1.0.conv1` on CIFAR-100 ($3 \times 3$ kernel, 64 input channels, 64 output channels, post-ReLU sparsity = 66.57%).
3. **WL3:** VGG-16-BN `features.3` on CIFAR-10 ($3 \times 3$ kernel, 64 input channels, 64 output channels, post-ReLU sparsity = 48.11%).
4. **WL4:** ResNet-18 `layer2.1.conv2` on CIFAR-10 ($3 \times 3$ kernel, 128 input channels tiled to 64, post-ReLU sparsity = 84.92%).

## 6.2 Workload Evaluation Scope Delineation
Each workload evaluates a **$4 \times 4$ spatial output region (16 tiles)** computing **16 output channels** over reduction depth $K = 576$ ($3 \times 3 \times 64$).
- **Total MACs Evaluated per Workload:** $16 \text{ tiles} \times 16 \text{ Cout} \times 576 = \mathbf{147,456 \text{ MAC operations}}$.
- **Total Across 4 Workloads:** $\mathbf{589,824 \text{ MAC operations}}$, yielding 1,024 40-bit output elements.
- **Host vs. Accelerator Boundary:** Generating full $32 \times 32$ CIFAR feature maps requires 64 sequential accelerator dispatch passes orchestrated by host DMA. Non-linear pooling and classification heads are executed on the host CPU.

## 6.3 Simulation Tooling & Independent Reference Verification
All RTL simulations were executed using **Icarus Verilog 12.0** under Linux WSL2, driven by Python verification harnesses. An independent reference model (`reproduce_numerical_evidence.py`) computes 40-bit integer dot products directly from raw input hex tensors using 64-bit integer arithmetic without referencing DUT internal signals or observed RTL state.


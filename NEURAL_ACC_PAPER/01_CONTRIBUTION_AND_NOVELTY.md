# Phase 1: Research Contribution, Novelty Assessment, and Problem Formulation

**Project:** Neural_Acc — Activation-Sparse CNN Accelerator with Adaptive PE Allocation  
**Document:** `01_CONTRIBUTION_AND_NOVELTY.md`  
**Date:** November 4, 2026  

---

## 1. Research Problem Definition

Deep Convolutional Neural Networks (CNNs) widely employ Rectified Linear Unit (ReLU) and related non-linear activations, which introduce substantial dynamic activation sparsity (typically 40% to 85% zero-valued activations across convolutional layers). In conventional dense spatial hardware accelerators (e.g., standard systolic arrays), these zero activations are fetched from memory and processed through arithmetic multiply-accumulate (MAC) units, resulting in redundant SRAM read energy and unnecessary dynamic switching activity in the datapath.

Simultaneously, edge-deployed inference accelerators must operate under heterogeneous and dynamically changing system constraints:
1. **Dynamic Resource Availability:** Silicon floorplans and thermal budgets fluctuate based on concurrent SoC workloads, requiring hardware datapaths to scale their active logic footprint dynamically.
2. **Strict Latency Deadlines:** Real-time perception frames require deterministic latency guarantees; violating frame deadlines can compromise system safety.
3. **Memory Bandwidth Bottlenecks:** On-chip SRAM and off-chip memory traffic dominate edge energy consumption. Lowering the number of active compute units forces channel-tiling algorithms into multi-pass execution, which re-reads activations repeatedly and risks offsetting any datapath power savings.

The core research problem addressed by `Neural_Acc` is:
> *How can an edge CNN accelerator combine activation zero-skipping with dynamic, deterministic PE allocation under strict latency deadlines, and what are the exact microarchitectural and memory-traffic trade-offs introduced by multi-pass channel tiling?*

---

## 2. Established Concepts vs. Implemented Neural_Acc Architecture

To maintain rigorous scientific honesty, we distinguish between established techniques in the literature and the specific microarchitectural implementation of `Neural_Acc`:

| Architectural Feature | Literature Status | Implemented in `Neural_Acc` | Distinctive Implementation Detail |
| :--- | :--- | :--- | :--- |
| **Activation Zero-Skipping** | Established (Eyeriss, Cnvlutin, SCNN) | Yes (`datapath_compute_feeder.sv`) | Gates MAC clock enables and suppresses weight SRAM read strobes cycle-by-cycle synchronously. |
| **Configurable PE Sizing** | Established (MorphSys, FlexASIC, Eyeriss v2) | Yes (`pe_array_40b.sv`, 16/32/64 PEs) | Clocks and gates PEs in exact power-of-two partitions (16, 32, 64) with deterministic multi-pass channel tiling. |
| **Multi-Pass Channel Tiling** | Established (General CNN tiling theory) | Yes (`tsk28_complete_convolution_engine.sv`) | Autonomous hardware loop over 1, 2, or 4 passes to accumulate 16 output channels with zero numerical loss. |
| **Cycle-Accurate Policy Controller** | Distinctive | Yes (`tsk33_transparent_policy_controller.sv`) | Deterministic hardware arbitrator executing Policy A (Min Resource) and Policy B (Max Performance) based on physical cycle counts. |
| **Hardware Safety Interlock Gating** | Distinctive | Yes (`tsk35a_invalid_pe_safety`) | Hard combinatorial and registered interlock rejecting infeasible resource caps ($P_{\max} < 16$), blocking execution dispatch with zero latency penalty upon recovery. |
| **Quantified SRAM Traffic Trade-Off** | Distinctive Empirical Finding | Yes (Verified via TSK-30 to TSK-37) | Direct hardware counter proof that multi-pass tiling incurs $+100\%$ to $+300\%$ activation SRAM read penalties, debunking naive energy claims. |

---

## 3. Candidate Research Contributions and Critical Audit

We evaluate 7 candidate contributions and determine whether each belongs in the primary publication contribution list:

### 1. Configurable 16-, 32-, and 64-PE Execution Modes
- **Implementation:** `pe_array_40b.sv`, `channel_tile_controller.sv`.
- **Validation Experiment:** Master regression suite (`tb_pe_array_40b.sv`, 28 checks) and multi-workload validation (`TSK30_RESULTS.csv`).
- **Literature Context:** PE partitioning and subarray gating are established concepts in coarse-grained reconfigurable arrays (CGRAs).
- **Novelty Classification:** *Plausible engineering implementation; not independently novel as an isolated architectural concept.*
- **Verdict:** Included as a structural mechanism supporting the broader contribution.

### 2. Activation Zero-Skipping with Weight Memory Read Suppression
- **Implementation:** `datapath_compute_feeder.sv`, `hybrid_sram_bank.sv`.
- **Validation Experiment:** Matched Dense vs Sparse execution across 12 configurations (`TSK37_SPARSE_EXECUTION_RESULTS.csv`).
- **Telemetry Finding:** Weight SRAM reads and active compute cycles drop by exactly 48.11% to 84.92%, matching layer sparsity. Total latency is completely unchanged (0.00% speedup).
- **Literature Context:** Prior architectures (e.g., Cnvlutin, Cambricon-X) use asynchronous indexing or offset FIFOs to skip cycles and gain latency speedup. `Neural_Acc` intentionally preserves synchronous channel-chunk stepping to guarantee deterministic timing.
- **Novelty Classification:** *Established principle implemented with synchronous determinism rather than latency acceleration.*
- **Verdict:** Primary contribution focused on *dynamic switching activity reduction under deterministic latency*.

### 3. Hardware-Automated Multi-Pass Channel Tiling
- **Implementation:** `tsk28_complete_convolution_engine.sv`, `k_progress_tracker.sv`.
- **Validation Experiment:** Bit-exact accumulation across 4 CNN layers (1,024 elements, $\text{MAE} = 0.0$).
- **Literature Context:** Software compilers (TVM, Halide) typically perform loop tiling. `Neural_Acc` implements autonomous hardware loop sequencing across chunks and passes.
- **Novelty Classification:** *Practical microarchitectural integration.*
- **Verdict:** Supporting contribution.

### 4. Constraint-Driven Deterministic Resource Allocation Controller
- **Implementation:** `tsk33_transparent_policy_controller.sv`.
- **Validation Experiment:** 201-point exhaustive boundary sweep (`TSK37_ADAPTIVE_POLICY_RESULTS.csv`).
- **Telemetry Finding:** Successfully arbitrates between Policy A (minimizing active PE logic by up to 75% when budget permits) and Policy B (maximizing throughput up to cap).
- **Literature Context:** Most dynamic resource allocation in published accelerators is managed by runtime software drivers or heuristics. `Neural_Acc` embeds the policy directly in hardware RTL, resolving in a single clock cycle.
- **Novelty Classification:** *Distinctive hardware implementation.*
- **Verdict:** **Primary contribution**.

### 5. Explicit Rejection of Invalid PE Caps with Hardware Interlock Gating
- **Implementation:** `tsk33_transparent_policy_controller.sv` (TSK-35A patch).
- **Validation Experiment:** 240 invalid request simulations; 0 compute pulses dispatched; immediate single-cycle recovery.
- **Literature Context:** Many published academic accelerator papers ignore invalid configuration states or assume a benevolent compiler. `Neural_Acc` demonstrates hardware-level fail-safe interlocks.
- **Novelty Classification:** *High-value practical contribution for robust system integration.*
- **Verdict:** Highlighted as a key robustness feature.

### 6. RTL-Level Numerical Correctness Across Real CNN Layers
- **Implementation:** Full microarchitectural stack evaluated against PyTorch pretrained models.
- **Validation Experiment:** Bit-exact 40-bit accumulator verification across 4 real workloads (ResNet-18, VGG-16-BN).
- **Novelty Classification:** *Methodological rigor and reproducibility evidence.*
- **Verdict:** Essential validation evidence.

### 7. Quantitative Characterization of the Resource–SRAM Bandwidth Trade-Off
- **Implementation:** Measured across internal multi-bank SRAM subsystem.
- **Telemetry Finding:** Multi-pass channel tiling causes $+100\%$ (32-PE) and $+300\%$ (16-PE) activation read amplification. Total SRAM accesses increase by up to $+87.18\%$.
- **Literature Context:** Many adaptive accelerator papers claim "energy proportionality" when reducing active PEs, ignoring memory amplification. Our work exposes the fundamental trade-off: reducing PE footprint increases memory traffic.
- **Novelty Classification:** *Distinctive empirical and scientific insight.*
- **Verdict:** **Primary scientific contribution**.

---

## 4. Formal Research Questions

The paper is structured around four tightly focused research questions directly aligned with our empirical evidence:

* **RQ1 (Numerical Correctness):** *Can an activation-sparse CNN accelerator with autonomous multi-pass channel tiling maintain bit-exact integer numerical equivalence against full-precision reference convolution across real CNN workloads?*  
  $\rightarrow$ **Answer:** Yes. Verified bit-exact ($\text{MAE} = 0.0$, $\text{RMSE} = 0.0$) across 1,024 outputs in 4 real CNN layers.

* **RQ2 (Sparsity & Switching Dynamics):** *How does synchronous activation zero-skipping affect active compute cycles, weight SRAM traffic, and wall-clock execution latency?*  
  $\rightarrow$ **Answer:** It eliminates 48.11% to 84.92% of weight SRAM reads and active MAC compute strobes in exact proportion to layer activation sparsity, while execution latency remains constant (0.00% speedup) due to synchronous channel stepping.

* **RQ3 (Resource–Memory Trade-Off):** *What are the quantitative execution latency and on-chip SRAM access trade-offs when throttling processing elements from 64 to 32 or 16 PEs?*  
  $\rightarrow$ **Answer:** Execution cycles scale deterministically by $2.00\times$ (19,121 cycles) and $4.00\times$ (38,225 cycles), but activation SRAM read traffic amplifies by $+100\%$ and $+300\%$ respectively, increasing total SRAM accesses by up to $+87.18\%$.

* **RQ4 (Hardware Policy Arbitrability & Safety):** *Can a hardware policy controller deterministically select optimal PE configurations under latency budgets and PE caps while guaranteeing absolute execution safety against infeasible resource constraints?*  
  $\rightarrow$ **Answer:** Yes. Verified across 201 boundary points with 100% adherence, zero unauthorized executions under $P_{\max} < 16$, and single-cycle recovery.

---

## 5. Novelty Assessment Matrix

| Statement of Novelty | Evidentiary Status | Literature Dependency | Publication Positioning |
| :--- | :--- | :--- | :--- |
| **Deterministic Hardware Policy Controller** | **Established by Evidence** | Low (Controller RTL fully simulated & verified) | Emphasize hardware arbitration speed and deterministic cycle latency |
| **Fail-Safe Hardware Interlock Gating** | **Established by Evidence** | Low (Verified at RTL dispatch interface) | Present as essential for reliable multi-tenant edge deployment |
| **Quantified Multi-Pass SRAM Amplification** | **Established by Evidence** | Medium (Requires comparison with tiled accelerators) | Present as a critical trade-off exposing the fallacy of naive energy proportionality |
| **Synchronous Sparsity Switching Gating** | **Established by Evidence** | High (Known concept; distinct in its deterministic timing) | Position as deterministic energy throttle rather than latency accelerator |
| **Silicon Power/Energy Proportionality** | **Unsupported (Not Measured)** | High (Requires post-layout gate-level power) | **Must NOT be claimed** |
| **End-to-End Autonomous Network Inference** | **Unsupported (Spatial Patch Only)** | High (Requires full host driver & DMA loop) | **Must NOT be claimed** |

---

## 6. Recommended Scientific Positioning

To guarantee maximum review defensibility:
1. **Position as an Architecture & Trade-Off Analysis Paper:** Position `Neural_Acc` as an *architectural study and microarchitectural implementation of adaptive resource allocation and activation-sparse clock gating in edge CNN inference*, highlighting the measured trade-offs between logic footprint and memory bandwidth.
2. **Emphasize Determinism and Transparency:** Highlight that unlike speculative asynchronous sparse accelerators, `Neural_Acc` preserves exact cycle determinism, enabling reliable real-time scheduling.
3. **Transparent Reporting of Limitations:** Be upfront about the 0.00% sparsity latency speedup and the $2\times$ to $4\times$ memory read amplification. Reviewers respect rigorous, honest evaluations far more than inflated claims.


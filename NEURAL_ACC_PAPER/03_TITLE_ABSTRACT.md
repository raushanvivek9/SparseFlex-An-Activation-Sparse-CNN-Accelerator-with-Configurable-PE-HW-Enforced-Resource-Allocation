# Phase 3: Title, Abstract, and Keywords

**Project:** Neural_Acc — Activation-Sparse CNN Accelerator with Adaptive PE Allocation  
**Document:** `03_TITLE_ABSTRACT.md`  
**Date:** November 4, 2026  

---

## 1. Candidate Titles and Selection

To ensure technical precision and avoid unverified claims (such as "energy-optimal", "silicon-proven", or "state-of-the-art"), we evaluate five candidate titles:

1. **Title 1:** *Neural_Acc: An Activation-Sparse CNN Accelerator with Configurable Processing Elements and Deterministic Resource Allocation*  
   - *Evaluation:* Strong and descriptive. Emphasizes the configurable nature of the PE array and the deterministic resource controller. Accurately reflects the RTL implementation.
2. **Title 2:** *Adaptive Resource Allocation and Activation-Sparse Zero-Gating in Edge CNN Accelerators: Architecture and Memory Trade-Offs*  
   - *Evaluation:* Excellent balance between architectural contribution and empirical trade-off findings (highlighting the multi-pass memory amplification).
3. **Title 3:** *Deterministic PE Throttling and Synchronous Activation Sparsity for Convolutional Neural Network Accelerators*  
   - *Evaluation:* Very precise regarding synchrony and deterministic behavior, though slightly narrower in scope.
4. **Title 4:** *A Cycle-Accurate Convolution Accelerator with Dynamic PE Allocation, Activation Zero-Gating, and Fail-Safe Resource Scheduling*  
   - *Evaluation:* Highlights the safety interlocks and cycle-accurate verification rigor, though somewhat lengthy.
5. **Title 5:** *Neural_Acc: Architecture, Verification, and Trade-Off Analysis of an Activation-Sparse CNN Accelerator with Adaptive Processing Elements*  
   - *Evaluation:* Comprehensive and well-rounded, covering design, verification, and empirical trade-offs.

### Recommended Title
> **"Neural_Acc: An Activation-Sparse CNN Accelerator with Configurable Processing Elements and Hardware-Enforced Resource Allocation"**

**Justification:**  
This title is scientifically defensible, concise, and accurately reflects the verified contributions:
- *"Activation-Sparse"* accurately captures the zero-activation clock-gating mechanism.
- *"Configurable Processing Elements"* reflects the verified 16-, 32-, and 64-PE operating modes.
- *"Hardware-Enforced Resource Allocation"* highlights the distinctive single-cycle RTL policy controller and its fail-safe hardware safety interlocks.
- It omits unsupported buzzwords ("energy-optimal", "real-time", "silicon-proven").

---

## 2. Research Abstract

### Abstract Text (228 words)
Convolutional Neural Network (CNN) accelerators for edge systems must balance strict latency deadlines against dynamic silicon resource constraints while minimizing unproductive datapath switching. This paper presents **Neural_Acc**, a cycle-accurate, parameterizable hardware accelerator featuring configurable processing element (PE) allocation and synchronous activation zero-gating. Neural_Acc dynamically partitions its arithmetic array into 16-, 32-, or 64-PE configurations, employing an autonomous hardware sequencer for multi-pass channel tiling and a single-cycle hardware policy controller that arbitrates between resource-minimization (Policy A) and throughput-maximization (Policy B). Hard fail-safe interlocks strictly reject infeasible resource caps ($P_{\max} < 16$), positively blocking compute dispatch. Evaluated across representative $4 \times 4$ spatial patches of convolutional layers from ResNet-18 and VGG-16-BN using real pretrained weights and activations, Neural_Acc achieves bit-exact integer numerical equivalence ($\text{MAE} = 0.0$, $\text{RMSE} = 0.0$) against an independent 40-bit fixed-point reference across 1,024 elements ($589,824$ MAC operations). Hardware counter telemetry demonstrates that synchronous activation zero-skipping eliminates 48.11% to 84.92% of weight SRAM reads and active MAC compute cycles in exact proportion to layer sparsity, while maintaining constant wall-clock execution latency (0.00% speedup). Furthermore, empirical trade-off analysis reveals that reducing active PEs from 64 to 32 or 16 increases activation SRAM read traffic by $+100.0\%$ and $+300.0\%$ due to multi-pass tiling, demonstrating that logic footprint reduction introduces significant memory bandwidth overheads.

---

## 3. Abstract Claim Verification and Boundary Check

To uphold strict scientific integrity, every statement in the abstract is mapped directly to verified evidence:

| Abstract Statement | Evidentiary Basis | Taxonomy Category |
| :--- | :--- | :--- |
| Configurable 16-, 32-, 64-PE partitions | `pe_array_40b.sv`, `tb_pe_array_40b.sv` | RTL Simulation Measurement |
| Policy A and Policy B hardware controller | `tsk33_transparent_policy_controller.sv` | RTL Simulation Measurement |
| Hardware safety interlocks for $P_{\max} < 16$ | `tb_tsk37_policy_audit.sv` (201 checks) | RTL Simulation Measurement |
| Bit-exact numerical equivalence ($\text{MAE} = 0.0$) | `TSK37_NUMERICAL_EVIDENCE.csv` (1,024 words) | Independent Software Reference |
| 48.11% to 84.92% weight read & compute drop | `TSK37_SPARSE_EXECUTION_RESULTS.csv` | RTL Simulation Measurement |
| Constant wall-clock latency (0.00% speedup) | `TSK37_SPARSE_EXECUTION_RESULTS.csv` | RTL Simulation Measurement |
| $+100\%$ and $+300\%$ activation SRAM read penalty | `TSK37_SPARSE_EXECUTION_RESULTS.csv` | RTL Simulation Measurement |
| Evaluated on representative $4 \times 4$ spatial patches | `TSK30_RESULTS.csv`, `TSK37_NUMERICAL_EVIDENCE.csv` | Workload Boundary Delineation |

---

## 4. Keywords

1. Convolutional Neural Network Accelerator
2. Activation Sparsity
3. Zero-Gating
4. Configurable Processing Elements
5. Hardware Resource Allocation
6. Multi-Pass Channel Tiling
7. Embedded Computer Architecture
8. Cycle-Accurate RTL Verification


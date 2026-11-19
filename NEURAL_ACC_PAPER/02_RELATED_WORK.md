# Phase 2: Literature Review and Related Work

**Project:** Neural_Acc — Activation-Sparse CNN Accelerator with Adaptive PE Allocation  
**Document:** `02_RELATED_WORK.md`  
**Date:** November 4, 2026  

---

## 1. Introduction to Hardware Acceleration for CNNs

Hardware accelerators for Deep Convolutional Neural Networks (CNNs) have evolved rapidly from dense systolic arrays (such as the Google TPU v1 [Jouppi et al., ISCA 2017] and DianNao [Chen et al., ASPLOS 2014]) toward architectures that exploit mathematical and structural properties of neural workloads. Among these properties, **dynamic activation sparsity**—arising from non-linear activation functions such as ReLU—and **resource reconfigurability** have received substantial attention. 

However, existing literature predominantly treats these two axes independently: sparsity-aware accelerators focus on maximizing computational throughput or minimizing arithmetic energy via asynchronous queues, while reconfigurable accelerators focus on tiling flexibility across layer topologies. `Neural_Acc` addresses the intersection of these domains, analyzing how dynamic PE allocation interacts with synchronous activation zero-skipping and exposing the memory-traffic trade-offs introduced by multi-pass channel tiling.

---

## 2. Activation Sparsity Exploitation Techniques

In typical CNNs, 40% to 85% of post-ReLU activations are zero. Prior research exploits this redundancy through three primary mechanisms:

### 2.1 Dynamic Clock Gating and Zero-Gating
Early sparse accelerators, notably **Eyeriss** [Chen et al., ISSCC 2016 / JSSC 2017], implement clock gating at the Processing Element (PE) level. When an input activation is zero, Eyeriss disables the PE clock and suppresses reads from the local register file, preventing unnecessary dynamic switching activity in the arithmetic multiplier. However, Eyeriss employs a fixed 168-PE spatial array with a rigid Row-Stationary (RS) dataflow and does not resize the active datapath to match system resource caps.

### 2.2 Asynchronous Zero-Skipping and Index Matching
To convert sparsity into wall-clock latency acceleration, architectures such as **Cnvlutin** [Judd et al., ISCA 2016] and **Cambricon-X** [Zhang et al., MICRO 2016] decouple compute lanes using asynchronous FIFO queues or indexing matching logic. Cnvlutin eliminates ineffectual multiplications by storing only non-zero activations and advancing lane pointers asynchronously. While this achieves average execution speedups of $1.37\times$, it introduces significant hardware complexity: FIFO synchronization buffers, crossbar interconnects, load-imbalance stalls between parallel lanes, and non-deterministic execution times.

### 2.3 Dual-Sparsity Cartesian Crossbars
Architectures such as **SCNN** [Parashar et al., ISCA 2017] and **SparTen** [Gondimalla et al., MICRO 2019] exploit both weight and activation sparsity simultaneously. SCNN uses a Cartesian product multiplier grid where compressed coordinates are matched. However, dual-sparsity designs suffer from high crossbar routing complexity, extensive scratchpad bank conflicts, and substantial area overheads for index coordinate tracking.

---

## 3. Configurable Processing-Element Architectures

Scalable and reconfigurable PE arrays have been explored to adapt to varying layer dimensions:

- **Eyeriss v2** [Chen et al., IEEE JETCAS 2019] introduces a hierarchical mesh network-on-chip (NoC) connecting 8 processing clusters (192 PEs total) that can be dynamically routed to accommodate depthwise separable convolutions or high-density layers.
- **MorphSys** [Singh et al., IEEE TVLSI 2000] and modern Coarse-Grained Reconfigurable Arrays (CGRAs) support dynamic reconfiguration of 2D arithmetic arrays, but typically lack hardware-integrated zero-detection and automatic multi-pass accumulation.
- **NullHop** [Aimar et al., IEEE TNNLS 2018] utilizes a 128-MAC spatial engine with a compressed bitmask index table, implemented on FPGA, but fixes its spatial MAC width across all operational regimes.

---

## 4. Hardware Resource Allocation & Multi-Pass Channel Tiling

When the physical PE array is smaller than the required number of output channels, convolution engines must tile the channel dimension across multiple sequential passes:

- **Loop Tiling in Classical Compilers:** Compilers such as TVM [Chen et al., OSDI 2018] and Halide decompose large convolutional tensors into spatial and channel tiles ($T_h, T_w, T_c, T_k$). However, tiling is typically scheduled statically in host software or firmware, assuming invariant hardware capacity.
- **Near-Memory Zero Skipping (nZESPA):** **nZESPA** [Das and Kapoor, IEEE TCAD 2021] proposes placing zero-skipping logic inside 3D Hybrid Memory Cube (HMC) vaults, reducing off-chip traffic. While effective, it relies on complex 3D memory technologies that are cost-prohibitive for edge embedded systems.
- **Dynamic Resource Adaptation:** Most existing edge systems adjust throughput via Dynamic Voltage and Frequency Scaling (DVFS). Architectural PE array partitioning (e.g., dynamically disabling half or three-quarters of the array) has rarely been coupled with single-cycle hardware policy controllers that simultaneously enforce latency deadlines and physical safety boundaries.

---

## 5. Architectural Comparison with Neural_Acc

Table 2.1 summarizes the key architectural distinctions between `Neural_Acc` and prior published accelerators:

### Table 2.1: Architectural Feature Comparison

| Accelerator | Publication / Venue | Sparsity Mechanism | Datapath Synchrony | Active PE Reconfigurability | Hardware Policy Arbitrator | Multi-Pass Memory Trade-off Modeled | Evaluation Platform |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **DianNao** | ASPLOS 2014 | None (Dense) | Synchronous | Fixed (64 MACs) | None | No | 65nm ASIC |
| **Eyeriss** | ISSCC 2016 / JSSC 2017 | Activation Zero-Gating | Synchronous | Fixed (168 PEs) | None | No | 65nm Silicon Tape-Out |
| **Cnvlutin** | ISCA 2016 | Activation Zero-Skipping | Asynchronous (Queues) | Fixed (16 Lanes) | None | No | 65nm Sim + Power Model |
| **Cambricon-X** | MICRO 2016 | Weight Zero-Skipping | Asynchronous | Fixed (16 PEs) | None | No | 65nm ASIC Model |
| **SCNN** | ISCA 2017 | Dual Sparsity (Wt & Act) | Asynchronous Crossbar | Fixed (4x4 Array) | None | No | 16nm TSMC Model |
| **NullHop** | IEEE TNNLS 2018 | Activation Bitmask | Compressed Stream | Fixed (128 MACs) | None | No | 28nm FPGA / ASIC |
| **Eyeriss v2** | IEEE JETCAS 2019 | Dual Sparsity (CSC) | Hierarchical Mesh NoC | Hierarchical Routing | Software Driver | No | 65nm Sim + CACTI |
| **SparTen** | MICRO 2019 | Dual Sparsity | Greedy Coordination | Fixed (16 PEs) | None | No | 28nm FDSOI Model |
| **nZESPA** | IEEE TCAD 2021 | Activation Zero-Skipping | Near-Memory Vaults | Fixed Near-Memory | None | No | 28nm Gem5 Sim |
| **Neural_Acc** | *This Work* | **Activation Zero-Gating** | **Synchronous** | **Dynamic (16, 32, 64 PEs)** | **Hardware RTL (Policy A & B)** | **Yes (Empirically Quantified)** | **Cycle-Accurate RTL (SystemVerilog)** |

---

## 6. Honest Novelty Evaluation

To avoid overclaiming, we answer seven explicit novelty questions directly from our implementation and literature review:

### 1. Are configurable PE modes already common?
**Yes.** Dynamic array partitioning and coarse-grained reconfigurability are well-established in general CGRA literature and modern scalable accelerators (e.g., Eyeriss v2, FlexASIC). Implementing 16-, 32-, and 64-PE operating modes in `Neural_Acc` is an engineering implementation, not an unprecedented architectural invention.

### 2. Is activation zero-skipping already established?
**Yes.** Exploiting ReLU zeros to gate switching activity dates back to Eyeriss (2016), Cnvlutin (2016), and earlier designs. The basic detection condition ($A == 0$) is standard.

### 3. Do existing designs combine sparsity with dynamic PE allocation?
**Rarely at the hardware controller level.** While some architectures support both concepts orthogonally, prior designs almost universally rely on software runtime schedulers or compile-time static mapping. `Neural_Acc` embeds the allocation policy directly into a single-cycle hardware controller (`tsk33_transparent_policy_controller.sv`) with fail-safe interlocks.

### 4. How do prior designs handle multi-pass execution?
Prior designs typically delegate multi-pass channel accumulation to host software, compiler-generated command streams, or external DMA reloads. `Neural_Acc` incorporates autonomous hardware-level multi-pass sequencing (`tsk28_complete_convolution_engine.sv`) that tracks chunk progression ($K=576$) and channel passes (1, 2, or 4) directly in the datapath controller with zero software intervention during the layer run.

### 5. What is genuinely distinctive about the current implementation?
Two aspects are genuinely distinctive:
1. **Deterministic Hardware Latency Budgeting with Fail-Safe Gating:** The policy controller deterministically guarantees latency deadlines based on verified physical cycle equations, while implementing hard interlocks that positively block execution ($P_{\max} < 16$) with clean single-cycle recovery.
2. **Empirical Exposure of the Multi-Pass SRAM Bandwidth Trade-Off:** While prior literature often claims energy savings from PE throttling, our measurements prove that multi-pass tiling increases activation SRAM reads by $+100\%$ (32-PE) and $+300\%$ (16-PE), demonstrating that lower PE allocation does not necessarily translate to lower overall system energy.

### 6. Is the contribution architectural, methodological, experimental, or a combination?
It is a **combination of architectural integration, control methodology, and empirical trade-off characterization**:
- *Architectural:* Clean integration of synchronous zero-gating, multi-bank SRAM, and a configurable 16/32/64-PE array.
- *Methodological:* A deterministic hardware resource controller with physical safety interlocks.
- *Experimental:* Comprehensive cycle-accurate RTL verification across real CNN layers exposing memory bandwidth trade-offs.

### 7. What additional experiment would most improve the novelty claim?
Performing post-layout gate-level power simulation (e.g., using Synopsys PrimeTime PX with a commercial 28nm standard-cell library) driven by the cycle-accurate switching traces generated during TSK-30 to TSK-37. This would provide the exact crossover point where activation SRAM read amplification exceeds PE arithmetic clock-gating energy savings.

---

## 7. Identified Research Gap

Despite extensive research into sparse accelerators, a critical gap remains:
> *Existing sparse accelerators focus primarily on algorithmic speedup via complex, non-deterministic asynchronous queues, while reconfigurable accelerators focus on topological mapping. There is a lack of rigorous, cycle-accurate hardware implementations that analyze the deterministic interaction between dynamic PE throttling, synchronous zero-gating, and multi-pass on-chip memory bandwidth amplification under hard real-time latency constraints.*

`Neural_Acc` bridges this gap through a fully synthesizable SystemVerilog implementation and an exhaustive, reproducible empirical evidence package.


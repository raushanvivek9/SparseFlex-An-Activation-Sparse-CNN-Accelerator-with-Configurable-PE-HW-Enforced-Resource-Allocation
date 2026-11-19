# Phase 4: Introduction and Motivation

**Project:** Neural_Acc — Activation-Sparse CNN Accelerator with Adaptive PE Allocation  
**Document:** `04_INTRODUCTION.md`  
**Date:** November 4, 2026  

---

# 1. Introduction

## 1.1 Background
Deep Convolutional Neural Networks (CNNs) remain a foundational workload across computer vision applications, ranging from autonomous robotic navigation and unmanned aerial vehicles to edge perception and medical image analysis [LeCun et al., 2015; He et al., 2016]. The computational backbone of modern CNN inference consists of multi-channel 2D convolutions, which require billions of Multiply-Accumulate (MAC) operations per input frame. In edge-embedded platforms, executing these operations under tight thermal, area, and power envelopes presents severe microarchitectural challenges [Chen et al., 2016; Sze et al., 2017].

Standard edge hardware implementations, such as spatial systolic arrays and SIMD vector processors [Jouppi et al., 2017; Chen et al., 2014], rely on regular, dense compute grids. These architectures fetch every weight and activation from on-chip SRAM scratchpads and broadcast them to arithmetic units regardless of their numerical value. However, modern CNN architectures universally employ non-linear activation functions—most prominently the Rectified Linear Unit ($\text{ReLU}(x) = \max(0, x)$)—which clamp all negative post-convolution values to zero. Consequently, real-world convolutional layers exhibit substantial dynamic activation sparsity, where 40% to 85% of input activations are zero-valued [Judd et al., 2016; Aimar et al., 2018]. In a dense datapath, multiplying by zero represents wasted energy, redundant SRAM read bandwidth, and unproductive dynamic switching activity.

## 1.2 Motivation
Two competing paradigms have emerged in response to the computational demands of edge inference:
1. **Sparsity Exploitation:** Prior sparse architectures (e.g., Cnvlutin [Judd et al., 2016], Cambricon-X [Zhang et al., 2016], SCNN [Parashar et al., 2017]) attempt to convert zero activations into latency speedups by using asynchronous queues, compressed coordinate lists, and crossbars. However, asynchronous zero-skipping introduces significant microarchitectural penalties: non-deterministic execution latency, load-imbalance stalls between parallel lanes, and complex hazard management. For safety-critical real-time edge applications, deterministic timing is often far more vital than opportunistic speedup.
2. **Dynamic Resource Allocation:** Multi-tenant edge SoCs host concurrent tasks (e.g., perception, localization, communication) whose compute demands fluctuate dynamically. When silicon power or thermal headroom is constrained, accelerators must throttle active logic. While coarse-grained reconfigurability has been studied [Singh et al., 2000; Chen et al., 2019], reducing active Processing Elements (PEs) forces the accelerator to process output channels across multiple sequential passes (multi-pass channel tiling).

Crucially, **multi-pass execution introduces a fundamental memory bandwidth trade-off**: when fewer PEs are active, input activations must be re-read from SRAM for each channel pass. Naively assuming that halving active PEs halves total energy overlooks this memory read amplification. A rigorous, cycle-accurate investigation into the interaction between synchronous zero-skipping, hardware resource throttling, and multi-pass SRAM traffic is urgently needed.

## 1.3 Research Problem
The central problem addressed in this work is:
> *How can an edge CNN accelerator simultaneously provide synchronous, deterministic activation zero-skipping and dynamic PE array reconfigurability under strict host-specified latency deadlines, and what are the exact empirical memory-bandwidth and execution trade-offs incurred when throttling active compute resources?*

## 1.4 Research Gap
A comprehensive survey of existing hardware accelerators reveals a prominent gap:
- Accelerators that exploit activation sparsity (e.g., Cnvlutin, NullHop, SCNN) predominantly use fixed spatial PE configurations and asynchronous scheduling, forfeiting cycle determinism.
- Accelerators that support dynamic tiling or PE scaling (e.g., Eyeriss v2, MorphSys) typically rely on software runtime schedulers or compile-time static mapping, lacking single-cycle hardware policy arbitration and fail-safe hardware interlocks.
- Furthermore, published literature rarely characterizes the exact SRAM traffic amplification that occurs when an accelerator falls back from a 64-PE single-pass execution to a 32-PE or 16-PE multi-pass regime, often leading to oversimplified energy-proportionality claims.

## 1.5 Proposed Approach: Neural_Acc
To address this gap, we present **Neural_Acc**, an activation-sparse CNN accelerator designed in cycle-accurate SystemVerilog. Neural_Acc combines:
1. **Configurable PE Datapath:** A parameterizable processing element array capable of operating in 16-, 32-, or 64-PE configurations.
2. **Synchronous Activation Zero-Gating:** A datapath compute feeder that detects zero-valued activations, immediately suppressing weight SRAM read strobes and gating MAC clock enables, eliminating dynamic switching without altering pipeline cycle timing.
3. **Hardware Multi-Pass Sequencing:** An autonomous hardware loop sequencer that manages channel-tiling passes (1, 2, or 4 passes) and chunk accumulation ($K=576$) with zero host intervention during execution.
4. **Transparent Hardware Policy Controller:** A single-cycle hardware arbitrator implementing **Policy A** (minimum resource allocation meeting latency budget) and **Policy B** (maximum throughput under resource cap), backed by hard fail-safe interlocks that strictly reject invalid PE caps ($P_{\max} < 16$).

## 1.6 Contributions
The primary contributions of this paper are:
1. **Microarchitectural Implementation & Hardware Policy Arbitration:** We design and implement a complete, synthesizable accelerator in SystemVerilog featuring a 16/32/64-PE array, multi-bank SRAM subsystem, autonomous channel sequencer, and a single-cycle hardware policy controller with fail-safe interlocks that positively block execution under infeasible constraints ($P_{\max} < 16$).
2. **Bit-Exact Numerical Validation Across Real CNN Workloads:** We independently verify numerical equivalence against an independent 40-bit fixed-point software model across 1,024 output elements ($589,824$ MAC operations) extracted from pretrained ResNet-18 and VGG-16-BN layers, confirming zero mismatches ($\text{MAE} = 0.0$, $\text{RMSE} = 0.0$).
3. **Quantitative Characterization of Activation Zero-Gating:** Through cycle-accurate hardware telemetry across 12 matched configurations, we demonstrate that synchronous zero-skipping eliminates 48.11% to 84.92% of weight SRAM reads and active MAC compute operations in exact proportion to layer sparsity, while maintaining constant wall-clock execution cycles (0.00% speedup) to preserve cycle determinism.
4. **Empirical Analysis of Multi-Pass Memory Amplification:** We quantify the trade-off between active compute footprint and on-chip SRAM traffic, demonstrating that throttling from 64 to 32 or 16 PEs increases activation SRAM reads by $+100.0\%$ (2 passes) and $+300.0\%$ (4 passes), increasing total SRAM traffic by up to $+87.18\%$ and highlighting that lower PE allocation does not imply lower total energy.

## 1.7 Paper Organization
The remainder of this paper is organized as follows: Section 2 reviews related work. Section 3 presents the problem formulation and background. Section 4 details the `Neural_Acc` microarchitecture and datapath. Section 5 describes the hardware resource allocation policies and safety interlocks. Section 6 presents the experimental methodology. Section 7 analyzes experimental results, including numerical accuracy, sparsity dynamics, and memory trade-offs. Section 8 provides a discussion and explicit limitations. Section 9 concludes the paper and outlines future directions.


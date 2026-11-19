# Phase 7: Complete Publication Tables and Figures Specification

**Project:** Neural_Acc — Activation-Sparse CNN Accelerator with Adaptive PE Allocation  
**Document:** `07_TABLES_AND_FIGURES.md`  
**Date:** November 4, 2026  

---

# Part I: Publication Tables

### Table 1: Comparative Analysis with State-of-the-Art CNN Accelerators
| Architecture | Venue / Year | Precision | Sparsity Target | Datapath Synchrony | PE Reconfigurability | Hardware Safety Interlock | Evaluation Platform |
| :--- | :--- | :---: | :--- | :--- | :--- | :---: | :--- |
| **DianNao** | ASPLOS 2014 | 16-bit Fixed | None (Dense) | Synchronous | Fixed (64 MACs) | No | 65nm ASIC Tape-Out |
| **Eyeriss** | JSSC 2017 | 16-bit Fixed | Activation (Zero-Gating) | Synchronous | Fixed (168 PEs) | No | 65nm Silicon Tape-Out |
| **Cnvlutin** | ISCA 2016 | 16-bit Fixed | Activation (Zero-Skipping)| Asynchronous (Queues) | Fixed (16 Lanes) | No | 65nm Sim + Power Model |
| **Cambricon-X** | MICRO 2016 | 16-bit Fixed | Weight Sparsity | Asynchronous | Fixed (16 PEs) | No | 65nm ASIC Model |
| **SCNN** | ISCA 2017 | 16-bit Fixed | Dual (Wt & Act) | Asynchronous Crossbar | Fixed (4x4 Array) | No | 16nm TSMC Model |
| **NullHop** | TNNLS 2018 | 16-bit Fixed | Activation (Bitmask) | Compressed Stream | Fixed (128 MACs) | No | 28nm FPGA / ASIC |
| **Eyeriss v2** | JETCAS 2019 | 8-bit Fixed | Dual (CSC) | Hierarchical Mesh NoC | Hierarchical Routing | No | 65nm Sim + CACTI |
| **SparTen** | MICRO 2019 | 8-bit Fixed | Dual Sparsity | Greedy Coordination | Fixed (16 PEs) | No | 28nm FDSOI Model |
| **nZESPA** | TCAD 2021 | 16-bit Fixed | Activation Sparsity | Near-Memory Vaults | Fixed Near-Memory | No | 28nm Gem5 Sim |
| **Neural_Acc** | *This Work* | **16b Q4.12** | **Activation Zero-Gating** | **Synchronous** | **Dynamic (16/32/64 PEs)** | **Yes (Pmax < 16 Gated)** | **Cycle-Accurate RTL (SystemVerilog)** |

---

### Table 2: Neural_Acc Accelerator Configuration Parameters
| Parameter | Value | Description |
| :--- | :--- | :--- |
| **Target Clock Frequency** | 100 MHz ($T_{\text{period}} = 10.0\ \text{ns}$) | Nominal operating clock for synthesis and cycle conversion |
| **Operand Precision** | Signed 16-bit Fixed-Point (Q4.12) | Dynamic range $[-8.0, +7.999755]$, resolution $2^{-12} \approx 2.44 \times 10^{-4}$ |
| **Accumulator Width** | Signed 40-bit Saturating Integer | 8 guard bits above 32-bit product; accommodates up to 256 additions without overflow |
| **Maximum PE Array Size** | 64 Processing Elements | Configurable into 16, 32, or 64 active PEs |
| **SRAM Memory Subsystem** | 8 Multi-Bank Hybrid SRAM Banks | 1,024 words $\times$ 16-bit dual-port per bank (16 KB total on-chip scratchpad) |
| **Reduction Depth Chunking** | 9 Chunks $\times$ 64 Terms ($K = 576$) | Tiled accumulation over 64 input channels $\times 3 \times 3$ kernel |
| **Autonomous Spatial Tiling** | $4 \times 4$ Spatial Output Grid (16 Tiles) | Autonomous hardware outer loop over 16 spatial tiles |
| **Output OFMAP Buffer** | 256 Words $\times$ 40-bit | Ping-pong drain buffer with rounding and requantization to signed 16-bit |

---

### Table 3: Evaluated CNN Workload Characteristics
| Workload ID | Neural Network | Evaluated Layer | Input Dimensions $(C_{\text{in}} \times H \times W)$ | Kernel Size $(K_h \times K_w)$ | Output Channels ($C_{\text{out}}$) | Spatial Patch | Total MACs Evaluated | Post-ReLU Sparsity (%) |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **WL1** | ResNet-18 (CIFAR-10) | `layer1.0.conv1` | $64 \times 32 \times 32$ | $3 \times 3$ | 16 (tiled from 64) | $4 \times 4$ (16 tiles) | 147,456 | 68.89% |
| **WL2** | ResNet-18 (CIFAR-100)| `layer1.0.conv1` | $64 \times 32 \times 32$ | $3 \times 3$ | 16 (tiled from 64) | $4 \times 4$ (16 tiles) | 147,456 | 66.57% |
| **WL3** | VGG-16-BN (CIFAR-10) | `features.3` | $64 \times 32 \times 32$ | $3 \times 3$ | 16 (tiled from 64) | $4 \times 4$ (16 tiles) | 147,456 | 48.11% |
| **WL4** | ResNet-18 (CIFAR-10) | `layer2.1.conv2` | $128 \times 16 \times 16$ (tiled 64) | $3 \times 3$ | 16 (tiled from 128) | $4 \times 4$ (16 tiles) | 147,456 | 84.92% |
| **TOTAL** | — | — | — | — | — | — | **589,824** | — |

---

### Table 4: Numerical Correctness and Golden Reference Verification
| Workload | Evaluated Elements | Reference Checksum | Hardware Output Checksum | Mismatches | Max Absolute Error | Mean Absolute Error (MAE) | Root Mean Square Error (RMSE) | Verification Status |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **WL1** | 256 | `0x64fc98` | `0x64fc98` | 0 | 0 | 0.0 | 0.0 | **PASS (100% Match)** |
| **WL2** | 256 | `0x510169` | `0x510169` | 0 | 0 | 0.0 | 0.0 | **PASS (100% Match)** |
| **WL3** | 256 | `0xc90fe0` | `0xc90fe0` | 0 | 0 | 0.0 | 0.0 | **PASS (100% Match)** |
| **WL4** | 256 | `0x42efc2` | `0x42efc2` | 0 | 0 | 0.0 | 0.0 | **PASS (100% Match)** |
| **TOTAL**| **1,024** | — | — | **0** | **0** | **0.0** | **0.0** | **BIT-EXACT EQUIVALENCE** |

---

### Table 5: Dense vs. Sparse Execution Hardware Telemetry Comparison
| Workload | PE Mode | Dense Total Cycles | Sparse Total Cycles | Latency Δ (%) | Dense Compute Cycles | Sparse Compute Cycles | Compute Cycle Δ (%) | Dense Wt Reads | Sparse Wt Reads | Wt Read Δ (%) | Act Sparsity |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **WL1** | 64-PE | 9,569 | 9,569 | **0.00%** | 9,216 | 2,867 | **-68.89%** | 9,216 | 2,867 | **-68.89%** | 68.89% |
| **WL1** | 32-PE | 19,121 | 19,121 | **0.00%** | 18,432 | 5,734 | **-68.89%** | 9,216 | 2,867 | **-68.89%** | 68.89% |
| **WL1** | 16-PE | 38,225 | 38,225 | **0.00%** | 36,864 | 11,468 | **-68.89%** | 9,216 | 2,867 | **-68.89%** | 68.89% |
| **WL2** | 64-PE | 9,569 | 9,569 | **0.00%** | 9,216 | 3,081 | **-66.57%** | 9,216 | 3,081 | **-66.57%** | 66.57% |
| **WL2** | 32-PE | 19,121 | 19,121 | **0.00%** | 18,432 | 6,162 | **-66.57%** | 9,216 | 3,081 | **-66.57%** | 66.57% |
| **WL2** | 16-PE | 38,225 | 38,225 | **0.00%** | 36,864 | 12,324 | **-66.57%** | 9,216 | 3,081 | **-66.57%** | 66.57% |
| **WL3** | 64-PE | 9,569 | 9,569 | **0.00%** | 9,216 | 4,782 | **-48.11%** | 9,216 | 4,782 | **-48.11%** | 48.11% |
| **WL3** | 32-PE | 19,121 | 19,121 | **0.00%** | 18,432 | 9,564 | **-48.11%** | 9,216 | 4,782 | **-48.11%** | 48.11% |
| **WL3** | 16-PE | 38,225 | 38,225 | **0.00%** | 36,864 | 19,128 | **-48.11%** | 9,216 | 4,782 | **-48.11%** | 48.11% |
| **WL4** | 64-PE | 9,569 | 9,569 | **0.00%** | 9,216 | 1,390 | **-84.92%** | 9,216 | 1,390 | **-84.92%** | 84.92% |
| **WL4** | 32-PE | 19,121 | 19,121 | **0.00%** | 18,432 | 2,780 | **-84.92%** | 9,216 | 1,390 | **-84.92%** | 84.92% |
| **WL4** | 16-PE | 38,225 | 38,225 | **0.00%** | 36,864 | 5,560 | **-84.92%** | 9,216 | 1,390 | **-84.92%** | 84.92% |

---

### Table 6: Architectural Trade-Off Comparison Across PE Operating Modes
| Metric | 64-PE Mode | 32-PE Mode | 16-PE Mode | 32-PE vs 64-PE | 16-PE vs 64-PE |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Active Processing Elements** | 64 PEs | 32 PEs | 16 PEs | -50.0% logic footprint | -75.0% logic footprint |
| **Channel Passes ($P$)** | 1 Pass | 2 Passes | 4 Passes | $2.00\times$ passes | $4.00\times$ passes |
| **Verified Execution Cycles** | 9,569 cycles | 19,121 cycles | 38,225 cycles | $2.00\times$ latency | $4.00\times$ latency |
| **Derived Time at 100 MHz\*** | $95.69\ \mu\text{s}$ | $191.21\ \mu\text{s}$ | $382.25\ \mu\text{s}$ | $2.00\times$ latency | $4.00\times$ latency |
| **Relative Compute Throughput** | $1.000\times$ | $0.500\times$ | $0.250\times$ | -50.0% throughput | -75.0% throughput |
| **Activation SRAM Reads** | **9,216** | **18,432** | **36,864** | **+100.0% read traffic** | **+300.0% read traffic** |
| **Weight SRAM Reads (WL1 Sparse)** | 2,867 | 2,867 | 2,867 | 0.0% change | 0.0% change |
| **Output SRAM Writes** | 256 | 256 | 256 | 0.0% change | 0.0% change |
| **Total SRAM Accesses (WL1 Sparse)** | **12,339** | **21,555** | **39,987** | **+74.69% traffic** | **+224.07% traffic** |

*\*Note: Execution times are derived analytically from verified RTL cycle counts assuming a nominal 100 MHz clock frequency ($T = 10.0\ \text{ns}$). Physical silicon PLL timing closure is not measured.*

---

### Table 7: Adaptive Hardware Policy Decision Sweep
| Policy | PE Cap ($P_{\max}$) | Latency Budget ($L_{\text{bgt}}$) | Feasibility | Selected Mode | Active PEs | Active Logic Saved (%) | Passes | Execution Enable | Budget Violation | Safety Status |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Policy A** | 64 | $\ge 38,225$ | Feasible | `2'b00` | 16 PEs | **75.0%** | 4 | 1 | 0 | Throttled (Min Resource) |
| **Policy A** | 64 | $19,121 - 38,224$ | Feasible | `2'b01` | 32 PEs | **50.0%** | 2 | 1 | 0 | Balanced Allocation |
| **Policy A** | 64 | $9,569 - 19,120$ | Feasible | `2'b10` | 64 PEs | **0.0%** (Baseline) | 1 | 1 | 0 | Max Logic Required |
| **Policy A** | 64 | $< 9,569$ | Infeasible | `2'b10` | 64 PEs | **0.0%** (Baseline) | 1 | 1 | **1** | Fallback (Violation Flag) |
| **Policy B** | 64 | $\ge 9,569$ | Feasible | `2'b10` | 64 PEs | **0.0%** (Baseline) | 1 | 1 | 0 | Max Performance |
| **Policy B** | 32 | $\ge 19,121$ | Feasible | `2'b01` | 32 PEs | **50.0%** | 2 | 1 | 0 | Max Under Cap |
| **Both** | $< 16$ (0, 8, 15) | Any Budget | **Invalid** | **`2'b11`** | **0 PEs** | **100.0%** (All Gated) | **0** | **0** | **1** | **Positively Gated / Blocked** |

---

### Table 8: Master RTL Regression and Functional Assertion Suite
| Testbench Suite | Category | Checks Evaluated | Checks Passed | Failures | Status | Execution Time |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| `tb_accelerator_core` | Baseline Microarchitecture | 4 | 4 | 0 | **PASS** | < 0.5s |
| `tb_mac_saturation` | Arithmetic Datapath | 11 | 11 | 0 | **PASS** | < 0.5s |
| `tb_k_progress_tracker` | Reduction Progress | 4 | 4 | 0 | **PASS** | < 0.5s |
| `tb_hybrid_sram_bank` | Memory Bank Verification | 13 | 13 | 0 | **PASS** | < 0.5s |
| `tb_drain_backpressure` | Output Drain & Flow Control | 15 | 15 | 0 | **PASS** | < 0.5s |
| `tb_acceptance_integrated` | Acceptance Testbench | 29 | 29 | 0 | **PASS** | < 0.5s |
| `tb_pe_array_40b` | Multi-PE Array Partitioning | 28 | 28 | 0 | **PASS** | < 0.5s |
| `tb_adaptive_pe_controller`| Legacy Controller | 53 | 53 | 0 | **PASS** | < 0.5s |
| `tb_multibank_sram_subsystem`| Multi-Bank SRAM Access | 137 | 137 | 0 | **PASS** | < 0.8s |
| `tb_ping_pong_buffer_controller`| Ping-Pong Control | 117 | 117 | 0 | **PASS** | < 0.8s |
| `tb_layer_command_sequencer`| Command Sequencer | 110 | 110 | 0 | **PASS** | < 0.8s |
| `tb_dma_controller` | DMA Engine | 87 | 87 | 0 | **PASS** | < 0.8s |
| `tb_ofmap_drain_controller` | OFMAP Drain & Requant | 732 | 732 | 0 | **PASS** | < 1.0s |
| `tb_neural_acc_integrated_top`| Top-Level System Integration| 132 | 132 | 0 | **PASS** | < 1.0s |
| `tb_workload_validation` | Workload Integration | 58 | 58 | 0 | **PASS** | < 0.8s |
| `tb_parallel_pe_operand_delivery`| Parallel Operand Delivery | 226 | 226 | 0 | **PASS** | < 1.0s |
| `tb_tsk10_cnn_workload` | CNN Layer Functional | 667 | 667 | 0 | **PASS** | < 1.5s |
| `tb_tsk11_ofmap_integration`| OFMAP Pipeline Integration | 3,443 | 3,443 | 0 | **PASS** | < 2.5s |
| `tb_tsk12_adaptive_experiment`| Adaptive PE Scaling | 5,846 | 5,846 | 0 | **PASS** | < 3.0s |
| `tb_tsk18_sparse_feeder` | Activation Zero-Gating | 490 | 490 | 0 | **PASS** | < 1.0s |
| **TOTAL REGRESSION** | **All 20 Testbenches** | **12,202** | **12,202** | **0** | **ALL PASS** | **17.351s** |

---

### Table 9: Scientific Evidence Taxonomy and Measurement Boundaries
| Evidence Domain | Claimed Finding | Evidentiary Basis | Taxonomy Classification | Publication Guardrail / Caveat |
| :--- | :--- | :--- | :--- | :--- |
| **Numerical Equivalence** | Bit-exact 40-bit output match | 1,024 words evaluated vs independent Python model | Verified (Bit-Exact) | Evaluated on $4 \times 4$ spatial patches of 16 channels, not full CNN models. |
| **Sparsity Switching Reduction** | 48.1% to 84.9% weight reads and compute cycles saved | Cycle-accurate RTL counter telemetry across 12 configurations | Verified | Dynamic switching power reduction only; static leakage unmodeled. |
| **Sparsity Latency Speedup** | Zero wall-clock latency reduction (0.00% speedup) | Identical cycle counts across dense and sparse runs (9,569 / 19,121 / 38,225) | Verified (Refutes Speedup) | Hardware preserves synchronous sequencing; do not claim latency speedup. |
| **Resource Policy Determinism** | Policy A saves up to 75% logic; Policy B maximizes throughput | Exhaustive 201-point RTL simulation sweep | Verified | Hardware controller requires host-supplied latency budgets and caps. |
| **Hardware Safety Gating** | 100% positive gating when $P_{\max} < 16$; 0 compute starts | 240 invalid requests tested in RTL simulation | Verified | Fail-safe interlock functions at hardware dispatch interface. |
| **Multi-Pass Memory Overhead** | Activation reads increase by $+100\%$ (32-PE) and $+300\%$ (16-PE) | Direct on-chip SRAM access counters | Verified | Exposes trade-off: logic reduction amplifies memory traffic. |
| **Total System Energy Reduction** | Lower PE modes reduce total system energy | None (Counter reductions offset by memory traffic and $4\times$ runtime) | **NOT MEASURED** | **MUST NOT BE CLAIMED** without physical post-layout power signoff. |
| **Full-Network Inference** | Complete end-to-end inference through accelerator | Single-layer convolution patches tested | **NOT MEASURED** | **MUST NOT BE CLAIMED**; multi-layer execution requires host driver. |

---

# Part II: Figure Specifications

### Figure 1: Top-Level System Microarchitecture
- **Source:** Implemented in `neural_acc_integrated_top.sv`.
- **Generated Output Files:** 
  - [`NEURAL_ACC_PAPER/plots/fig01_system_architecture.png`](file:///e:/MTech/LanChain/MTP/NEURAL_ACC_PAPER/plots/fig01_system_architecture.png) (300 DPI High-Resolution)
  - [`NEURAL_ACC_PAPER/plots/fig01_system_architecture.svg`](file:///e:/MTech/LanChain/MTP/NEURAL_ACC_PAPER/plots/fig01_system_architecture.svg) (Scalable Vector Graphic)
- **Description:** Complete block diagram illustrating host command FIFO, transparent hardware policy controller, layer command sequencer, 8-bank hybrid SRAM subsystem, activation-sparse datapath compute feeder, synchronous zero-detector with weight read suppression, and 64-PE array partitioned into 4 quadrants with OFMAP drain requantization unit.
- **Specification:** Provided as Mermaid block diagram in Section 1 of `05_ARCHITECTURE_AND_METHODOLOGY.md` and synthesized into high-resolution graphics.

### Figure 2: Configurable 64-PE Array Organization
- **Source:** Implemented in `pe_array_40b.sv`.
- **Generated Output Files:**
  - [`NEURAL_ACC_PAPER/plots/fig02_pe_array_organization.png`](file:///e:/MTech/LanChain/MTP/NEURAL_ACC_PAPER/plots/fig02_pe_array_organization.png) (300 DPI High-Resolution)
  - [`NEURAL_ACC_PAPER/plots/fig02_pe_array_organization.svg`](file:///e:/MTech/LanChain/MTP/NEURAL_ACC_PAPER/plots/fig02_pe_array_organization.svg) (Scalable Vector Graphic)
- **Description:** Structural partitioning of the 64 processing elements into four 16-PE clusters (Quadrants 0 to 3), showing independent clock-gating domains, row-broadcast activation buses, column-specific filter weight buses, and mode decoding for 16-, 32-, and 64-PE operating modes.

### Figure 3: Synchronous Activation Zero-Gating Datapath
- **Source:** Implemented in `datapath_compute_feeder.sv` and `slot_control_unit.sv`.
- **Generated Output Files:**
  - [`NEURAL_ACC_PAPER/plots/fig03_zero_gating_circuit.png`](file:///e:/MTech/LanChain/MTP/NEURAL_ACC_PAPER/plots/fig03_zero_gating_circuit.png) (300 DPI High-Resolution)
  - [`NEURAL_ACC_PAPER/plots/fig03_zero_gating_circuit.svg`](file:///e:/MTech/LanChain/MTP/NEURAL_ACC_PAPER/plots/fig03_zero_gating_circuit.svg) (Scalable Vector Graphic)
- **Description:** Detailed circuit schematic showing the fine-grained zero-detection comparator (`A == 16'h0000`), weight SRAM read strobe gating logic (`wt_sram_ren`), and MAC dynamic clock enable gating (`mac_ce`), along with timing comparisons proving zero latency impact (0.00% delta).

### Figure 4: Multi-Pass Channel Tiling Execution Timeline
- **Source:** Implemented in `tsk28_complete_convolution_engine.sv`.
- **Generated Output Files:**
  - [`NEURAL_ACC_PAPER/plots/fig04_multipass_timing_diagram.png`](file:///e:/MTech/LanChain/MTP/NEURAL_ACC_PAPER/plots/fig04_multipass_timing_diagram.png) (300 DPI High-Resolution)
  - [`NEURAL_ACC_PAPER/plots/fig04_multipass_timing_diagram.svg`](file:///e:/MTech/LanChain/MTP/NEURAL_ACC_PAPER/plots/fig04_multipass_timing_diagram.svg) (Scalable Vector Graphic)
- **Description:** Timing diagram illustrating channel tiling across sequential passes: 1 pass of 16 channels (64-PE, 9,569 cycles), 2 passes of 8 channels (32-PE, 19,121 cycles), and 4 passes of 4 channels (16-PE, 38,225 cycles), highlighting chunk progression over $K=576$ and re-fetch memory penalties.

### Figure 5: Hardware Policy Controller Flowchart
- **Source:** Implemented in `tsk33_transparent_policy_controller.sv` and `tsk35a_policy_controller_safe.sv`.
- **Generated Output Files:**
  - [`NEURAL_ACC_PAPER/plots/fig05_policy_flowchart.png`](file:///e:/MTech/LanChain/MTP/NEURAL_ACC_PAPER/plots/fig05_policy_flowchart.png) (300 DPI High-Resolution)
  - [`NEURAL_ACC_PAPER/plots/fig05_policy_flowchart.svg`](file:///e:/MTech/LanChain/MTP/NEURAL_ACC_PAPER/plots/fig05_policy_flowchart.svg) (Scalable Vector Graphic)
- **Description:** Single-cycle arbitration decision tree for Policy A (Min Resource) and Policy B (Max Performance), depicting constraint evaluation, fallback branches, budget violation assertion, and unconditional $P_{\max} < 16$ safety interlock gating.

---

### Figure 6: Total Execution Cycles Across PE Configurations
- **Generated Output File:** [`NEURAL_ACC_PAPER/plots/fig06_total_cycles_pe_modes.png`](file:///e:/MTech/LanChain/MTP/NEURAL_ACC_PAPER/plots/fig06_total_cycles_pe_modes.png) (and `.svg`)
- **Data Source:** `TSK37_SPARSE_EXECUTION_RESULTS.csv`
- **Axes:** X-axis: PE Configuration (64-PE, 32-PE, 16-PE); Y-axis: Total Execution Latency (Clock Cycles, 0 to 44,000).
- **Key Insight:** Demonstrates exact deterministic $2.00\times$ and $4.00\times$ scaling across PE modes, and visually confirms that dense and sparse runs have **identical cycle counts** (0.00% delta).

### Figure 7: Active MAC Compute Cycles Across CNN Workloads
- **Generated Output File:** [`NEURAL_ACC_PAPER/plots/fig07_compute_cycles_sparsity.png`](file:///e:/MTech/LanChain/MTP/NEURAL_ACC_PAPER/plots/fig07_compute_cycles_sparsity.png) (and `.svg`)
- **Data Source:** `TSK37_SPARSE_EXECUTION_RESULTS.csv`
- **Axes:** X-axis: CNN Workloads (WL1 to WL4 with activation sparsity %); Y-axis: Active MAC Compute Cycles (0 to 11,500).
- **Key Insight:** Demonstrates that active compute cycles drop by exactly the layer activation sparsity: -68.9% (WL1), -66.6% (WL2), -48.1% (WL3), and -84.9% (WL4).

### Figure 8: On-Chip SRAM Access Traffic Breakdown
- **Generated Output File:** [`NEURAL_ACC_PAPER/plots/fig08_sram_traffic_breakdown.png`](file:///e:/MTech/LanChain/MTP/NEURAL_ACC_PAPER/plots/fig08_sram_traffic_breakdown.png) (and `.svg`)
- **Data Source:** `TSK37_SPARSE_EXECUTION_RESULTS.csv` (WL1 Sparse)
- **Axes:** X-axis: PE Operating Mode (64-PE, 32-PE, 16-PE); Y-axis: Total On-Chip SRAM Accesses (Words, 0 to 47,000).
- **Key Insight:** Stacked bar chart showing constant weight reads (2,867 words) and constant OFMAP writes (256 words), but dramatic amplification of activation reads: 9,216 (64-PE) $\rightarrow$ 18,432 (+100%, 32-PE) $\rightarrow$ 36,864 (+300%, 16-PE). Total SRAM accesses increase by $+74.7\%$ and $+224.1\%$.

### Figure 9: Execution Latency vs. Active PE Allocation
- **Generated Output File:** [`NEURAL_ACC_PAPER/plots/fig09_latency_vs_pes.png`](file:///e:/MTech/LanChain/MTP/NEURAL_ACC_PAPER/plots/fig09_latency_vs_pes.png) (and `.svg`)
- **Data Source:** `TSK36_RESOURCE_LATENCY_AUDIT.csv`
- **Axes:** X-axis: Active Processing Elements (16, 32, 64 PEs); Y-axis: Execution Latency ($\mu\text{s}$ at 100 MHz, 50 to 430 $\mu\text{s}$).
- **Key Insight:** Depicts the smooth hyperbolic throughput scaling ($95.69\ \mu\text{s} \rightarrow 191.21\ \mu\text{s} \rightarrow 382.25\ \mu\text{s}$).

### Figure 10: Architectural Trade-Off Summary: Logic Footprint vs. Memory Overhead
- **Generated Output File:** [`NEURAL_ACC_PAPER/plots/fig10_tradeoff_summary.png`](file:///e:/MTech/LanChain/MTP/NEURAL_ACC_PAPER/plots/fig10_tradeoff_summary.png) (and `.svg`)
- **Data Source:** `TSK35B_ALL_SCENARIOS_MEASURED.csv` and `TSK37_SPARSE_EXECUTION_RESULTS.csv`
- **Axes:** Primary Y-axis: Active Logic Footprint Reduction (%); Secondary Y-axis: SRAM Access Traffic Increase (%).
- **Key Insight:** Directly contrasts the benefit (reducing active logic footprint by 50% in 32-PE and 75% in 16-PE) against the penalty (increasing total SRAM accesses by $+74.7\%$ and $+224.1\%$), visually capturing the core scientific thesis of the paper.

---

# Part III: Supplemental Thesis Figures

### Figure 11: Datapath Precision, Sizing, and Guard Bit Headroom Analysis
- **Source:** Implemented in `mac_unit_40b.sv`.
- **Generated Output Files:**
  - [`NEURAL_ACC_PAPER/plots/fig11_accumulator_headroom.png`](file:///e:/MTech/LanChain/MTP/NEURAL_ACC_PAPER/plots/fig11_accumulator_headroom.png) (300 DPI High-Resolution)
  - [`NEURAL_ACC_PAPER/plots/fig11_accumulator_headroom.svg`](file:///e:/MTech/LanChain/MTP/NEURAL_ACC_PAPER/plots/fig11_accumulator_headroom.svg) (Scalable Vector Graphic)
- **Description:** Bitfield allocation breakdown comparing 16-bit Q4.12 input operands, 32-bit multiplier product, and 40-bit saturating accumulator, with mathematical proof demonstrating 14.83 bits of overflow safety margin over $K=576$ inner products ($\text{MAE} = 0.000000$).

### Figure 12: Dual-Port Ping-Pong Buffer Execution Waveform
- **Source:** Implemented in `ping_pong_buffer_controller.sv`.
- **Generated Output Files:**
  - [`NEURAL_ACC_PAPER/plots/fig12_ping_pong_waveform.png`](file:///e:/MTech/LanChain/MTP/NEURAL_ACC_PAPER/plots/fig12_ping_pong_waveform.png) (300 DPI High-Resolution)
  - [`NEURAL_ACC_PAPER/plots/fig12_ping_pong_waveform.svg`](file:///e:/MTech/LanChain/MTP/NEURAL_ACC_PAPER/plots/fig12_ping_pong_waveform.svg) (Scalable Vector Graphic)
- **Description:** Cycle-by-cycle pipeline timing waveform illustrating mutual exclusion invariants between DMA ingestion (Port A0) and compute datapath (Port B), demonstrating zero-compute-stall double-buffering.

### Figure 13: 2D Operational Constraint Space and Allocation Decisions
- **Source:** Implemented in `tsk33_transparent_policy_controller.sv` and `tsk34_constraint_sweep.py`.
- **Generated Output Files:**
  - [`NEURAL_ACC_PAPER/plots/fig13_policy_space_heatmap.png`](file:///e:/MTech/LanChain/MTP/NEURAL_ACC_PAPER/plots/fig13_policy_space_heatmap.png) (300 DPI High-Resolution)
  - [`NEURAL_ACC_PAPER/plots/fig13_policy_space_heatmap.svg`](file:///e:/MTech/LanChain/MTP/NEURAL_ACC_PAPER/plots/fig13_policy_space_heatmap.svg) (Scalable Vector Graphic)
- **Description:** 2D heatmap diagram spanning $P_{\max} \in [0, 64]$ and $L_{\max} \in [0, 50,000]$ cycles under Policy A, illustrating the partition of operating regimes: Fail-Safe Interlock ($P_{\max} < 16$), 16-PE, 32-PE, 64-PE, and Fallback violation zones.


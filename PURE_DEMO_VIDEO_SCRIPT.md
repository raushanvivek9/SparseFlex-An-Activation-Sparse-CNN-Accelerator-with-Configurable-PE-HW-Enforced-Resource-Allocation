# SparseFlex: Pure Live Demo Video Script (Direct Terminal & Raw RTL Simulation)

> **Purpose:** 100% Live Demonstration Video (No slides, no lecture).  
> **What the screen shows:** Only your **Linux/WSL Terminal** and **VS Code**.  
> **Execution Method:** Direct, authentic `python3` and raw `iverilog` / `vvp` commands.  
> **Target Duration:** **3 to 3.5 Minutes**  
> **Recording Shortcut:** Press `Win` + `Alt` + `R` (Windows Game Bar) to start/stop recording.

---

## Screen Setup Before You Hit Record

1. **Terminal Setup:**
   * Open your PowerShell terminal, type `wsl` to enter Ubuntu Linux, and navigate to the project directory:
     ```bash
     wsl
     cd /mnt/e/MTech/LanChain/MTP
     ```
   * Press `Ctrl` + `+` twice so that all terminal text is large, sharp, and easy to read on 1080p video.
2. **VS Code Setup:**
   * Have VS Code open on [`slot_control_unit.sv`](./phase2_step1_microarchitecture_and_rtl/slot_control_unit.sv#L25-L35) ready to display lines 28–32.
3. **Browser Setup:**
   * Have one browser tab open to your [GitHub Repository](https://github.com/raushanvivek9/SparseFlex-An-Activation-Sparse-CNN-Accelerator-with-Configurable-PE-HW-Enforced-Resource-Allocation).

---

## Word-for-Word Live Demo Script

```
========================================================================================
[TIME: 0:00 - 0:25] SCENE 1: DEMO INTRODUCTION & ENVIRONMENT
========================================================================================
```
* **On Screen:** WSL Terminal at `/mnt/e/MTech/LanChain/MTP`.
* **Action:** Type `ls -la` to show the project structure.

#### What to Say:
> *"Hello everyone. In this demo video, I am demonstrating the live hardware execution and cycle-accurate verification of **SparseFlex**, our synthesizable SystemVerilog CNN accelerator with reconfigurable processing elements and hardware policy control.*  
>  
> *Here in our Linux EDA environment, we have the complete synthesizable RTL, cycle-accurate SystemVerilog testbenches, and automated verification harnesses."*

---

```
========================================================================================
[TIME: 0:25 - 1:15] SCENE 2: MASTER RTL REGRESSION (12,202 ASSERTIONS)
========================================================================================
```
* **On Screen:** Terminal.
* **Action:** Type and press Enter:
  ```bash
  cd phase2_step1_microarchitecture_and_rtl
  python3 run_regression.py
  ```
* *(Wait 5 seconds as the 20 testbench suites compile with Icarus Verilog and pass in real time)*

#### What to Say:
> *"First, I will run our master RTL regression suite directly using `python3 run_regression.py`.*  
>  
> *(Pause 3-5 seconds while simulation compiles and passes on screen)*  
>  
> *In real time, this invokes Icarus Verilog and simulates all 20 SystemVerilog testbenches. It rigorously validates our baseline MAC units, multi-bank ping-pong SRAM, autonomous sequencers, and the full top-level integrated accelerator.*  
>  
> *As shown in the execution summary: **all 20 testbenches passed**, evaluating **12,202 functional assertions with a 100% pass rate and zero defects**."*

---

```
========================================================================================
[TIME: 1:15 - 1:55] SCENE 3: RAW IVERILOG ZERO-GATING SIMULATION (TB_TSK18)
========================================================================================
```
* **On Screen:** Terminal (still in `phase2_step1_microarchitecture_and_rtl`).
* **Action:** Copy-paste and execute the raw `iverilog` compile and `vvp` command:
  ```bash
  iverilog -g2012 -o sim_sparse mac_unit_40b.sv pe_array_40b.sv adaptive_pe_controller.sv ping_pong_buffer_controller.sv hybrid_sram_bank.sv multibank_sram_subsystem.sv dma_controller.sv layer_command_sequencer.sv dma_to_sram_write_adapter.sv datapath_compute_feeder.sv ofmap_drain_controller.sv neural_acc_integrated_top.sv tb_tsk18_sparse_feeder.sv && vvp sim_sparse; rm -f sim_sparse
  ```
* *(Point cursor to Scenario 2 and Scenario 3 showing the exact cycle and memory savings)*

#### What to Say:
> *"Now let us compile and execute our zero-gating sparse feeder testbench directly from raw SystemVerilog using `iverilog` and `vvp`.*  
>  
> *This executes 10 directed hardware scenarios:  
> In Scenario 2, under 100% activation sparsity, SRAM reads drop by 80%.  
> In Scenario 3, under 50% sparsity, memory reads drop by 40%.  
> In Scenario 10, the hardware confirms bit-exact output equivalence between dense and sparse modes.  
> All **490 checks pass with zero defects**."*

---

```
========================================================================================
[TIME: 1:55 - 2:35] SCENE 4: REAL CNN TELEMETRY & JITTER-FREE TIMING
========================================================================================
```
* **On Screen:** Terminal.
* **Action:** Navigate to `TSK37_RESEARCH_READINESS` and run the telemetry script:
  ```bash
  cd /mnt/e/MTech/LanChain/MTP/TSK37_RESEARCH_READINESS
  ../Neural_Acc_env/bin/python reproduce_sparse_evidence.py
  ```
* *(Use mouse cursor to highlight the summary table on screen)*

#### What to Say:
> *"Next, let us run our telemetry audit across real CNN layers extracted from PyTorch using `reproduce_sparse_evidence.py`.*  
>  
> *Look at the live computed summary table on screen:  
> In Workload 4—a deep residual layer from ResNet-18 with **84.92% activation sparsity**—our synchronous zero-gating achieves an **84.92% drop in weight SRAM reads and active compute cycles**.*  
>  
> *Crucially, look at the latency column: across all 12 configurations, the latency reduction is strictly **0.0%**, proving that both dense and sparse workloads complete in the **exact same clock cycles with zero timing jitter**.*  
>  
> *We can also run `reproduce_numerical_evidence.py`, which computes 64-bit reference convolutions on raw hex tensors, verifying **MAE = 0.000000** across all 589,824 MAC operations."*

---

```
========================================================================================
[TIME: 2:35 - 3:05] SCENE 5: RAW IVERILOG POLICY CONTROLLER & SAFETY INTERLOCK
========================================================================================
```
* **On Screen:** Terminal (still in `TSK37_RESEARCH_READINESS`).
* **Action:** Type and press Enter:
  ```bash
  iverilog -g2012 -o sim_policy ../TSK33_ADAPTIVE_RESOURCE_POLICY/tsk33_transparent_policy_controller.sv tb_tsk37_policy_audit.sv && vvp sim_policy; rm -f sim_policy
  ```
* *(Point cursor to: `TOTAL TESTS EVALUATED: 201 | PASSED: 201 | FAILED: 0`)*

#### What to Say:
> *"Now we compile and execute our hardware policy controller directly with `iverilog` and `vvp`.*  
>  
> *This audit sweeps across 201 boundary points in pure combinatorial logic. When the SoC heats up, the controller dynamically throttles the array to 32 PEs or 16 PEs.*  
>  
> *Most importantly, when tested with an illegal limit like $P_{\max} < 16$, the hardware instantly asserts an unconditional safety interlock, de-asserting execution enable to protect the chip from deadlock. **All 201 boundary tests pass with zero errors**."*

---

```
========================================================================================
[TIME: 3:05 - 3:30] SCENE 6: SYSTEMVERILOG RTL CODE INSPECTION IN VS CODE
========================================================================================
```
* **On Screen:** Switch window to VS Code showing [`slot_control_unit.sv`](./phase2_step1_microarchitecture_and_rtl/slot_control_unit.sv).
* **Action:** Highlight lines 28–32 with mouse:
  ```systemverilog
  assign is_zero = (activation_in == 16'h0000);
  assign wt_sram_ren = ~is_zero;
  assign mac_ce = ~is_zero;
  ```

#### What to Say:
> *"To see the physical hardware implementation, here is our synthesizable SystemVerilog code in `slot_control_unit.sv`.*  
>  
> *In these three concise lines: whenever `activation_in` is zero, the hardware de-asserts `wt_sram_ren` to eliminate SRAM bitline switching, and de-asserts `mac_ce` to freeze multiplier clock toggling.*  
>  
> *Because it executes synchronously in 1 clock cycle without inserting pipeline bubbles or stalls, pipeline cycles advance uniformly while active power is eliminated."*

---

```
========================================================================================
[TIME: 3:30 - 3:45] SCENE 7: GITHUB REPOSITORY & CONCLUSION
========================================================================================
```
* **On Screen:** Switch window to web browser showing your [GitHub Repository](https://github.com/raushanvivek9/SparseFlex-An-Activation-Sparse-CNN-Accelerator-with-Configurable-PE-HW-Enforced-Resource-Allocation).

#### What to Say:
> *"This concludes the live demonstration of SparseFlex. All synthesizable SystemVerilog RTL files, testbenches, simulation telemetry, and scripts are fully open-sourced on our GitHub repository. Thank you very much."*

---

## Direct Terminal Commands Cheatsheet (Copy & Paste Ready)

### 1. In WSL Terminal (`cd /mnt/e/MTech/LanChain/MTP/phase2_step1_microarchitecture_and_rtl`):
```bash
# 1. Master Regression (12,202 Checks)
python3 run_regression.py

# 2. Raw Zero-Gating Sparse Feeder Simulation (490 Checks)
iverilog -g2012 -o sim_sparse mac_unit_40b.sv pe_array_40b.sv adaptive_pe_controller.sv ping_pong_buffer_controller.sv hybrid_sram_bank.sv multibank_sram_subsystem.sv dma_controller.sv layer_command_sequencer.sv dma_to_sram_write_adapter.sv datapath_compute_feeder.sv ofmap_drain_controller.sv neural_acc_integrated_top.sv tb_tsk18_sparse_feeder.sv && vvp sim_sparse; rm -f sim_sparse

# 3. Real CNN Sparsity & Timing Determinism Audit (-84.92% Reads, 0.00% Jitter)
cd /mnt/e/MTech/LanChain/MTP/TSK37_RESEARCH_READINESS
../Neural_Acc_env/bin/python reproduce_sparse_evidence.py

# 4. Raw Policy Controller Simulation (201 Checks)
iverilog -g2012 -o sim_policy ../TSK33_ADAPTIVE_RESOURCE_POLICY/tsk33_transparent_policy_controller.sv tb_tsk37_policy_audit.sv && vvp sim_policy; rm -f sim_policy
```

# SparseFlex: Pure Live Demo Video Script (100% Screen Demonstration)

> **Purpose:** This script is strictly for a **Live Demonstration Video** (no PowerPoint slides, no lecture).  
> **What the screen shows:** Only your **VS Code**, your **PowerShell Terminal**, and live simulation execution!  
> **Target Duration:** **2.5 to 3 Minutes**  
> **Recording Shortcut:** Press `Win` + `Alt` + `R` (Windows Game Bar) to start/stop recording.

---

## Screen Setup Before You Hit Record:
* **Left half of screen:** VS Code open to `phase2_step1_microarchitecture_and_rtl/slot_control_unit.sv`.
* **Right half of screen (or Full Screen):** PowerShell terminal open to `E:\MTech\LanChain\MTP`.
* **Zoom in:** In PowerShell, press `Ctrl` + `+` twice so all table text is big and clear.

---

## 3-Minute Live Demo Teleprompter (Word-for-Word Script)

```
========================================================================================
[TIME: 0:00 - 0:25] SCENE 1: DEMO INTRODUCTION & REPOSITORY ENVIRONMENT
========================================================================================
```
* **On Screen:** PowerShell Terminal in `E:\MTech\LanChain\MTP`.
* **Action:** Type `dir` or `ls` to briefly show the project directory.

#### What to Say:
> *"Hello everyone. In this demonstration video, I am showing the live hardware implementation and cycle-accurate verification of **SparseFlex**, an activation-sparse CNN accelerator with reconfigurable processing elements and hardware policy control.*  
>  
> *Here in our project environment, we have the complete synthesizable SystemVerilog RTL, cycle-accurate testbenches, and automated Python verification harnesses."*

```
========================================================================================
[TIME: 0:25 - 1:15] SCENE 2: MASTER RTL REGRESSION (12,202 ASSERTIONS)
========================================================================================
```
* **On Screen:** Terminal.
* **Action:** Type and press Enter:
  ```powershell
  python run_demo.py
  ```
* *(Wait 5 seconds as the table populates and all 20 testbenches pass)*

#### What to Say:
> *"First, I will run our master RTL regression suite by executing `python run_demo.py`.*  
>  
> *(Watch testbenches pass on screen)*  
>  
> *In real time, this compiles and simulates all 20 SystemVerilog testbenches using Icarus Verilog in our EDA environment. It tests our baseline MAC units, multi-bank ping-pong SRAM buffers, sequencing state machines, and the full top-level accelerator.*  
>  
> *As shown in the execution summary: **all 20 testbenches passed**, evaluating **12,202 functional assertions with 100% pass rate and zero defects**."*

```
========================================================================================
[TIME: 1:15 - 2:00] SCENE 3: REAL CNN SPARSITY & JITTER-FREE TELEMETRY
========================================================================================
```
* **On Screen:** Terminal.
* **Action:** Type and press Enter:
  ```powershell
  python run_demo.py --telemetry
  ```
* *(Use mouse cursor to highlight Workload 4 and the cycle count)*

#### What to Say:
> *"Next, I am executing `python run_demo.py --telemetry` to inspect the verified hardware telemetry across real PyTorch CNN layers.*  
>  
> *Look at Section 1: In Workload 4—a ResNet-18 layer with **84.92% activation sparsity**—our synchronous zero-gating cuts weight SRAM reads from 9,216 to 1,390, achieving an **84.92% dynamic switching reduction**.*  
>  
> *Crucially, notice the latency column: both dense and 84.92% sparse workloads complete in the **exact same 9,569 clock cycles**, proving **0.00% timing jitter**.*  
>  
> *In Section 2, our multi-pass analysis shows that while 16-PE mode saves 75% logic power, it inflates activation SRAM reads by **+300%**.*  
>  
> *And Section 3 confirms **Mean Absolute Error = 0.000000** across 589,824 MACs, proving bit-exact numerical fidelity against a 64-bit golden model."*

```
========================================================================================
[TIME: 2:00 - 2:35] SCENE 4: SINGLE-CYCLE POLICY CONTROLLER & SAFETY INTERLOCK
========================================================================================
```
* **On Screen:** Terminal.
* **Action:** Type and press Enter:
  ```powershell
  python run_demo.py --policy
  ```
* *(Point to: `TOTAL TESTS EVALUATED: 201 | PASSED: 201 | FAILED: 0`)*

#### What to Say:
> *"Now let us verify the hardware policy controller using `python run_demo.py --policy`.*  
>  
> *This audit tests 201 boundary conditions in a single clock cycle. When the chip heats up, it dynamically throttles the array to 32 PEs or 16 PEs to manage thermal caps.*  
>  
> *Most importantly, when tested with an illegal limit like $P_{\max} < 16$, the hardware instantly asserts an unconditional safety interlock, de-asserting execution enable to protect the chip from deadlock. **All 201 boundary tests pass with zero failures**."*

```
========================================================================================
[TIME: 2:35 - 3:00] SCENE 5: SYSTEMVERILOG RTL CODE INSPECTION IN VS CODE
========================================================================================
```
* **On Screen:** Switch window to VS Code showing `slot_control_unit.sv`.
* **Action:** Highlight lines 28–32 on screen with mouse.

#### What to Say:
> *"To see how this is physically implemented, here is our synthesizable SystemVerilog code in `slot_control_unit.sv`.*  
>  
> *In these three lines: whenever `activation_in` is zero, the hardware de-asserts `wt_sram_ren` to eliminate memory bitline switching, and de-asserts `mac_ce` to freeze multiplier clock transitions.*  
>  
> *Because it executes in 1 clock cycle without inserting pipeline bubbles, our pipeline advances deterministically while saving dynamic power."*

```
========================================================================================
[TIME: 3:00 - 3:15] SCENE 6: DEMO CONCLUSION
========================================================================================
```
* **On Screen:** Switch to web browser showing the GitHub repository.

#### What to Say:
> *"This concludes the live demonstration of SparseFlex. All SystemVerilog RTL files, testbenches, simulation telemetry, and scripts are fully open-sourced on our GitHub repository. Thank you very much."*

---

## Quick Command Cheatsheet to Type During Demo:

1. `python run_demo.py`  
   *(Runs full 20-suite regression $\to$ 12,202 / 12,202 PASS)*
2. `python run_demo.py --telemetry`  
   *(Shows -84.92% weight reads, 0.00% jitter, MAE = 0.0)*
3. `python run_demo.py --policy`  
   *(Shows 201/201 policy controller & safety interlock PASS)*
4. Switch to VS Code (`slot_control_unit.sv`) to show the RTL code.

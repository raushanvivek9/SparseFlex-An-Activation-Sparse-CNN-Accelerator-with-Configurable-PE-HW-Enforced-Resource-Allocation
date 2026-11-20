# SparseFlex: M.Tech Project (MTP) Demo Video Script

**Project Title:** SparseFlex: An Activation-Sparse CNN Accelerator with Reconfigurable Processing Elements (16/32/64) and Hardware-Enforced Resource Allocation  
**Author / Presenter:** Raushan Kumar (Roll No: CS23MXXX)  
**Department:** Department of Computer Science and Engineering, Indian Institute of Technology Tirupati  
**Supervisor:** Prof. Supervisor Name  
**Target Duration:** ~4 to 4.5 Minutes  
**Resolution:** 1080p (1920 $\times$ 1080) at 30 or 60 fps  
**Screen Recording Tools:** OBS Studio, Windows Xbox Game Bar (`Win + Alt + R`), or Loom  

---

## Pre-Recording Checklist & Environment Setup

1. **Terminal Font Size:** Open Windows Terminal / PowerShell, press `Ctrl` + `+` twice to make the font size large and crisp for 1080p video.
2. **VS Code Setup:** Open `phase2_step1_microarchitecture_and_rtl/slot_control_unit.sv` and zoom in (`Ctrl` + `=`).
3. **Browser Tabs Prepared:**
   * Tab 1: Slide 1 of [`MTECH_PRESENTATION_SLIDE_DECK.md`](./MTECH_PRESENTATION_SLIDE_DECK.md) or PowerPoint.
   * Tab 2: High-resolution architecture diagram ([`Neural_Acc_Architecture_Presentation.png`](./Neural_Acc_Architecture_Presentation.png)).
   * Tab 3: Overleaf showing [`poster_A1_portrait.tex`](./poster_A1_portrait.tex) / compiled PDF.
   * Tab 4: GitHub Repository: `https://github.com/raushanvivek9/SparseFlex-An-Activation-Sparse-CNN-Accelerator-with-Configurable-PE-HW-Enforced-Resource-Allocation`
4. **Microphone Check:** Do a 10-second test recording to ensure your voice is loud, clear, and without background hum.

---

## Scene-by-Scene Video Recording Script

```
================================================================================
TOTAL ESTIMATED TIME: 4 Minutes 30 Seconds
================================================================================
```

---

### Scene 1: Introduction, Problem Statement & Motivation
* **Timestamp:** `0:00` – `0:40` (Duration: 40 sec)
* **Visual on Screen:** Presentation **Slide 1** (*Motivation & Problem Statement: The Real-Time Edge AI Bottleneck*).
* **Action:** Keep mouse still, speak with steady confidence.

#### Word-for-Word Spoken Script:
> *"Good morning, respected committee members. My name is Raushan Kumar, and my M.Tech project is titled **SparseFlex: A Reconfigurable Activation-Sparse CNN Accelerator with Hardware-Enforced Resource Allocation**.*  
>  
> *Modern Convolutional Neural Networks for edge devices exhibit between 40% and 85% activation sparsity post-ReLU. Conventional sparse accelerators attempt asynchronous zero-skipping to compress time, but this introduces non-deterministic timing jitter, severe spatial load imbalance, and complex FIFO queues—making them unsuitable for hard real-time edge environments like autonomous driving or robotics.*  
>  
> *In SparseFlex, we solve this fundamental challenge by designing a cycle-deterministic, synchronous zero-gating architecture with dynamic 16, 32, and 64 PE scaling, and single-cycle hardware safety interlocks."*

---

### Scene 2: Top-Level Hardware Microarchitecture
* **Timestamp:** `0:40` – `1:25` (Duration: 45 sec)
* **Visual on Screen:** Full-screen view of [`Neural_Acc_Architecture_Presentation.png`](./Neural_Acc_Architecture_Presentation.png) (or Slide 4).
* **Action:** Use your mouse cursor to point to each numbered hardware block as you name it.

#### Word-for-Word Spoken Script:
> *"Here is the complete synthesizable SystemVerilog microarchitecture of SparseFlex. The architecture coordinates five hardware subsystems:  
>  
> 1. **An 8-Bank Dual-Port Hybrid SRAM (41 KB):** Provides ping-pong buffering for continuous, conflict-free memory delivery.  
> 2. **The Slot Control Unit (Zero Feeder):** Performs single-cycle synchronous zero-detection, gating weight memory reads and multiplier clocks without altering pipeline timing.  
> 3. **The Configurable 64-PE Compute Array:** Organized into 4 rows of 16 columns with quadrant-level clock gating, supporting 16-PE, 32-PE, and 64-PE operating modes.  
> 4. **40-Bit Saturating Accumulators:** Sized with 8 guard bits above 32-bit products to mathematically guarantee zero overflow across deep accumulations.  
> 5. **Single-Cycle Policy Controller:** Arbitrates between Policy A (energy minimization) and Policy B (performance slack maximization), with a fail-safe hardware interlock."*

---

### Scene 3: Live Master RTL Regression (12,202 Assertions)
* **Timestamp:** `1:25` – `2:20` (Duration: 55 sec)
* **Visual on Screen:** PowerShell Terminal window in `E:\MTech\LanChain\MTP`.
* **Action:** Type and execute the master verification command:
  ```powershell
  python run_demo.py
  ```
* **Watch as the terminal compiles and evaluates 20 testbench suites.**

#### Word-for-Word Spoken Script:
> *"Now let us demonstrate the live hardware execution. I am running our master regression suite directly from our project root using `python run_demo.py`.*  
>  
> *(Pause 3-5 seconds while simulation compiles and passes)*  
>  
> *As you can see on screen, our automated regression compiles and executes all 20 SystemVerilog testbenches using Icarus Verilog in our EDA environment. It evaluates baseline arithmetic units, memory subsystems, sequencing FSMs, and the full integrated accelerator across real CNN layers.*  
>  
> *Here is the grand total: **all 12,202 functional assertions pass with 100% success and zero defects**."*

---

### Scene 4: Real CNN Workloads, Sparsity Savings & Timing Determinism
* **Timestamp:** `2:20` – `3:10` (Duration: 50 sec)
* **Visual on Screen:** Same terminal window.
* **Action:** Type and execute:
  ```powershell
  python run_demo.py --telemetry
  ```
* **Hover mouse over the table showing Workload 4 and the Multi-Pass Memory Trade-off.**

#### Word-for-Word Spoken Script:
> *"Next, let us inspect the verified hardware telemetry across real PyTorch CNN layers, executed via `python run_demo.py --telemetry`.*  
>  
> *Look at Section 1: In Workload 4—a deep residual layer from ResNet-18 with **84.92% activation sparsity**—our synchronous zero-gating reduces weight SRAM reads from 9,216 down to exactly 1,390, achieving **84.92% switching activity elimination**.*  
>  
> *Crucially, notice the latency column: dense execution and 84.92% sparse execution both complete in the **exact same 9,569 clock cycles**—achieving **0.00% timing jitter**.*  
>  
> *In Section 2, we reveal a critical finding: down-scaling to 16 PEs saves 75% active logic, but multi-pass tiling inflates activation SRAM reads by **+300%** (from 9,216 to 36,864 reads). This empirically disproves naive claims in literature that logic throttling guarantees proportional energy savings.*  
>  
> *Finally, Section 3 confirms that our 40-bit accumulation achieves **Mean Absolute Error equal to 0.000000**—bit-exact equivalence against a 64-bit golden model across all 589,824 MAC operations."*

---

### Scene 5: Single-Cycle Policy Controller & Fail-Safe Interlock
* **Timestamp:** `3:10` – `3:50` (Duration: 40 sec)
* **Visual on Screen:** Same terminal window.
* **Action:** Type and execute:
  ```powershell
  python run_demo.py --policy
  ```
* **Point mouse to: `TOTAL TESTS EVALUATED: 201 | PASSED: 201 | FAILED: 0`.**

#### Word-for-Word Spoken Script:
> *"Now we evaluate our single-cycle hardware policy controller using `python run_demo.py --policy`.*  
>  
> *This audit sweeps across 201 boundary points, evaluating latency deadlines, dynamic PE caps, and fail-safe recovery.*  
>  
> *When the edge SoC heats up, the controller instantly throttles the array to 32 PEs (19,121 cycles) or 16 PEs (38,225 cycles). Most importantly, if the host ever specifies an illegal cap like $P_{\max} < 16$, the hardware detects it in pure combinatorial logic, de-asserts `execution_enable`, and locks the mode to prevent silicon deadlocks or memory corruption. All 201 boundary conditions pass with zero errors."*

---

### Scene 6: Synthesizable SystemVerilog RTL in VS Code
* **Timestamp:** `3:50` – `4:20` (Duration: 30 sec)
* **Visual on Screen:** Switch to VS Code, showing [`slot_control_unit.sv`](./phase2_step1_microarchitecture_and_rtl/slot_control_unit.sv).
* **Action:** Highlight lines 25–35 containing `is_zero`, `wt_sram_ren`, and `mac_ce`.

#### Word-for-Word Spoken Script:
> *"Here is the physical SystemVerilog implementation of our zero-gating in `slot_control_unit.sv`.*  
>  
> *Notice these three concise lines: whenever `activation_in` is zero, `wt_sram_ren` de-asserts to eliminate bitline precharge power, and `mac_ce` de-asserts to freeze multiplier internal capacitance toggling.*  
>  
> *Because this decision is made synchronously in 1 clock cycle without inserting pipeline bubbles or stalls, clock cycles advance uniformly while active power is suppressed."*

---

### Scene 7: A1 Poster, GitHub Repository & Closing Sign-Off
* **Timestamp:** `4:20` – `4:45` (Duration: 25 sec)
* **Visual on Screen:** 
  1. Show Overleaf / PDF of [`poster_A1_portrait.pdf`](./poster_A1_portrait.tex) with the IIT Tirupati logo and QR code.
  2. Switch to web browser showing the GitHub repository.

#### Word-for-Word Spoken Script:
> *"Finally, here is our A1 portrait poster designed to the official IIT Tirupati MTP format, incorporating all 7 graded evaluation criteria and our scannable repository QR code.*  
>  
> *All synthesizable RTL modules, testbenches, mathematical documentation, presentation slides, and poster files are open-sourced on our GitHub repository.*  
>  
> *Thank you very much for your time and evaluation."*

---

## Post-Recording Guide: Uploading & Submitting

### 1. Uploading to YouTube (Recommended)
1. Go to **YouTube Studio** (`studio.youtube.com`) $\rightarrow$ Click **Create** $\rightarrow$ **Upload Videos**.
2. Select your recorded `.mp4` file.
3. Under **Visibility**, select **"Unlisted"**.
4. Set Title:  
   `M.Tech Project Demo: SparseFlex — Reconfigurable Activation-Sparse CNN Accelerator | IIT Tirupati`
5. Set Description:
   ```text
   M.Tech Project Demo Video
   Project: SparseFlex — An Activation-Sparse CNN Accelerator with Reconfigurable Processing Elements and Hardware-Enforced Resource Allocation
   Student: Raushan Kumar (Roll No: CS23MXXX)
   Department: Department of Computer Science and Engineering, IIT Tirupati
   Supervisor: Prof. Supervisor Name
   GitHub Repository: https://github.com/raushanvivek9/SparseFlex-An-Activation-Sparse-CNN-Accelerator-with-Configurable-PE-HW-Enforced-Resource-Allocation
   ```

### 2. Linking in Your Deliverables
Once you copy your YouTube video link (e.g., `https://youtu.be/abc123xyz`):
* Add it to **Slide 8** and **Slide 10** of [`MTECH_PRESENTATION_SLIDE_DECK.md`](./MTECH_PRESENTATION_SLIDE_DECK.md).
* Add a badge to your GitHub [`README.md`](./README.md).
* You can also paste the link in your chat so I can update all files and push them to GitHub automatically for you!

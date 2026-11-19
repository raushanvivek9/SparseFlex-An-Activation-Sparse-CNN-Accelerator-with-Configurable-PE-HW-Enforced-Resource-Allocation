# Check exact character lengths of all 4 fields
text1 = """Key learnings in DNN accelerator architecture, arithmetic, and EDA:
1. CNN Dataflow & Tiling: Spatial mapping on 2D PE arrays (4x16), channel tiling, and reduction depth (K = Kh x Kw x Cin = 3x3x64 = 576 ops/output).
2. Sparsity & Zero-Gating: Analyzed post-ReLU dynamic activation sparsity (40-85%). Designed synchronous zero-gating that suppresses weight SRAM reads and gates MAC clock enables, saving dynamic power with 0.00% latency jitter (deterministic WCET).
3. Fixed-Point & Headroom: Signed Q4.12 arithmetic (S=4096.0). Sized a 40-bit accumulator with 24 guard bits, mathematically proving zero overflow across 16.7M MACs (bit-exact MAE = 0.000000).
4. Memory Hierarchy: 8-bank dual-port SRAM (41,472 B) with ping-pong buffering. Discovered multi-pass channel tiling inflates activation reads by +100% (32-PE) and +300% (16-PE).
5. EDA Tools: Synthesizable SystemVerilog (IEEE 1800), Icarus Verilog, PyTorch, and AMD Vivado timing constraints (100 MHz XDC)."""

text2 = """Key contributions in the Neural_Acc research project:
1. Synthesizable RTL Design: Built complete CNN accelerator in SystemVerilog: 64-PE reconfigurable array (16/32/64 modes), 8-bank dual-port SRAM (41,472 B), DMA master, sequencer, and zero-gating feeder.
2. Bit-Exact Precision: Q4.12 datapath with 40-bit accumulation. Verified 1,024 activation outputs against double-precision float with zero error (MAE = 0.000000).
3. Synchronous Zero-Gating: Evaluated real CNN layers (ResNet-18, VGG-16). Zero-gating reduced active compute cycles and weight reads by -48.1% to -84.9% with 0.00% latency delta.
4. Memory Trade-Off Discovery: Proved downsizing to 32 or 16 PEs forces multi-pass tiling, inflating activation reads by +100% and +300%.
5. 1-Cycle Safety Policy: Built Policy A/B controller; verified fail-safe lock on Pmax < 16 within 1 cycle.
6. Verification & Paper: Passed 20/20 testbenches (12,202 checks) and prepared a full research paper."""

text3 = """Exam Topics: 1. PE Arrays 2. Zero-Gating 3. Q4.12 Fixed-Point 4. Multi-Bank SRAM 5. Multi-Pass Tiling 6. Hardware Policy 7. Timing Constraints

20 Questions (Answers in brackets):
1. ReLU causes activation [sparsity].
2. 3x3 conv with Cin=64: K=[576] ops.
3. In Q4.12, 1.0 is 16'h[1000].
4. Accumulator width is [40] bits.
5. Accumulator gives [24] guard bits.
6. Max products without overflow: [16,777,216].
7. Zero activation gates MAC [clock enable].
8. Dense vs sparse latency delta: [0.00]%.
9. Physical PE grid: [4] rows, [16] cols.
10. In 16-PE mode, active cols are [0 to 3].
11. SRAM subsystem has [8] banks.
12. 32-PE mode requires [2] passes.
13. 16-PE mode increases act reads by [+300]%.
14. Ping-pong buffers keep [mutual exclusion].
15. Policy A minimizes PEs under [L_max].
16. Policy B maximizes slack under [P_max].
17. Pmax < 16 forces mode to 2'b[11].
18. XDC clock period is [10.0] ns.
19. Output MAE vs float is [0.000000].
20. Master regression passed [12,202] checks."""

text4 = """Additional Points:
1. Paper Readiness: Authored an 11-section research paper titled "Neural_Acc: An Activation-Sparse CNN Accelerator with Configurable Processing Elements and Hardware-Enforced Resource Allocation" with 13 high-resolution vector plots and 18 verified literature citations (with DOIs).
2. Target Publication: Prepared for submission to IEEE ASAP and IEEE/ACM DATE, with an extension path to IEEE TVLSI.
3. Thesis Scope: Forms a complete, self-contained M.Tech dissertation combining RTL microarchitecture, mathematical overflow proofs, dynamic zero-gating, on-chip memory hierarchy analysis, and hardware safety interlocking.
4. Next Steps: FPGA bitstream and post-route switching power extraction using AMD Vivado."""

print("Length of Field 1:", len(text1))
print("Length of Field 2:", len(text2))
print("Length of Field 3:", len(text3))
print("Length of Field 4:", len(text4))

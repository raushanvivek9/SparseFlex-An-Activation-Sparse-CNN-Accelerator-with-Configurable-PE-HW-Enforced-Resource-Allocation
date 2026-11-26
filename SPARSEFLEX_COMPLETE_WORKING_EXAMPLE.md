# SparseFlex: Complete Working Example

## 1. Introduction

In this example, I will take one input activation matrix and one weight matrix and show how SparseFlex processes them from input to output.

The main idea of SparseFlex is that instead of always using all processing elements, we identify zero-valued activations and avoid unnecessary computation.

The accelerator supports configurable numbers of active Processing Elements, or PEs:

**64 PEs, 32 PEs, and 16 PEs.**

The computation uses:

- Q4.12 fixed-point representation
- 40-bit accumulators
- Synchronous zero-gating
- Multi-pass channel tiling
- Dual-bank ping-pong SRAM
- Configurable PE utilization

---

## 2. Step 1 — Input Activation Matrix

Let us take a simple activation matrix:

$$
A =
\begin{bmatrix}
1 & 0 & 2 & 0\\
0 & 3 & 0 & 1\\
2 & 0 & 1 & 0\\
0 & 1 & 0 & 2
\end{bmatrix}
$$

This matrix contains:

$$
4 \times 4 = 16
$$

activation values.

Now count the zero values.

There are 8 zeros.

Therefore,

$$
\text{Zero Count}=8
$$

and the activation sparsity is:

$$
\text{Sparsity}
=
\frac{\text{Number of zeros}}
{\text{Total activations}}
=
\frac{8}{16}
=
0.5
$$

So,

$$
\boxed{\text{Sparsity}=50\%}
$$

This means that half of the activation values are zero.

These zero values are important because SparseFlex can use them to avoid unnecessary computation.

---

## 3. Step 2 — Weight Matrix

Now suppose our weight matrix is:

$$
W =
\begin{bmatrix}
1 & 2 & 1 & 1\\
2 & 1 & 2 & 1\\
1 & 1 & 2 & 2\\
2 & 1 & 1 & 2
\end{bmatrix}
$$

For simplicity, we perform element-wise row multiplication followed by accumulation across each row $i \in \{0, 1, 2, 3\}$.

The basic computation is:

$$
Y_i = \sum_{j=0}^{3} A_{ij}W_{ij}
$$

---

## 4. Step 3 — Normal Dense Computation

First, suppose we do not use sparsity.

We calculate every multiplication.

For the first row:

$$
(1\times1)+(0\times2)+(2\times1)+(0\times1)
=1+0+2+0
=3
$$

For the second row:

$$
(0\times2)+(3\times1)+(0\times2)+(1\times1)
=0+3+0+1
=4
$$

For the third row:

$$
(2\times1)+(0\times1)+(1\times2)+(0\times2)
=2+0+2+0
=4
$$

For the fourth row:

$$
(0\times2)+(1\times1)+(0\times1)+(2\times2)
=0+1+0+4
=5
$$

Therefore the output vector is:

$$
\boxed{
Y=
\begin{bmatrix}
3\\
4\\
4\\
5
\end{bmatrix}
}
$$

---

## 5. Step 4 — Where SparseFlex Helps

Now look at the first row again:

$$
[1,\;0,\;2,\;0]
$$

The zero values give:

$$
0\times2 \quad \text{and} \quad 0\times1
$$

These multiplications do not contribute anything to the result.

Normally, a conventional accelerator sends these operations through the datapath.

SparseFlex detects the zero activation and performs zero-gating.

So instead of performing:

$$
1\times1, \quad 0\times2, \quad 2\times1, \quad 0\times1
$$

we only perform:

$$
1\times1 \quad \text{and} \quad 2\times1
$$

Therefore, only **2 useful MAC operations** are required instead of 4.

The same happens for the other rows.

---

## 6. Step 5 — Calculate MAC Reduction

Without zero-gating:

$$
16
$$

multiplications are performed.

Because 8 activation values are zero:

$$
8
$$

multiplications can be skipped.

Therefore:

$$
\text{Skipped MACs}=8
$$

and useful MACs are:

$$
16-8=8
$$

Therefore:

$$
\boxed{\text{Useful MACs}=8}
$$

The MAC reduction is:

$$
\frac{16-8}{16}\times100
=
\frac{8}{16}\times100
=\boxed{50\%}
$$

So, for this example, SparseFlex eliminates **50% of the multiplication operations** because the activation matrix has 50% sparsity.

---

## 7. Step 6 — Synchronous Zero-Gating

This is where the hardware implementation becomes important.

SparseFlex does not simply remove data randomly or drop pipeline slots asymmetrically.

Zero detection is performed synchronously with the accelerator pipeline across two RTL levels:
- **Per-PE Exact-Zero Bypass (`mac_unit_40b.sv`):** For every row element where `act_data == 0` (`bypass_mac = 1`), the multiplier output is gated to `0`, the accumulator register update is disabled, and `cycle_skipped` is asserted.
- **All-Zero Column-Group Weight Skip (`datapath_compute_feeder.sv`):** When feeding the 4 PE rows simultaneously, if all 4 activations in a step are zero (`all_acts_zero`), the feeder also skips reading weight words from SRAM (`ST_SPARSE_WAIT_A`).

For Row 0, the per-PE MAC behavior is:

```text
Activation       Weight        Operation

1                1             MAC
0                2             SKIP (bypass_mac = 1)
2                1             MAC
0                1             SKIP (bypass_mac = 1)
```

So the PE does not waste switching activity on the zero computation.

The important point is:

**The pipeline timing remains deterministic while unnecessary computation is disabled.**

This is why we call it **synchronous zero-gating**.

---

## 8. Step 7 — Processing Elements

Now consider the PE array (`pe_array_40b.sv`, organized as $4\text{ rows} \times 16\text{ columns} = 64\text{ PEs}$).

At runtime, the policy controller (`tsk33_transparent_policy_controller.sv`) evaluates the latency budget ($L_{\max}$), PE limit ($P_{\max}$), and policy objective (`policy_select`), selecting:

$$
64,\;32,\;\text{or } 16
$$

active PEs (or blocking execution via `resolved_pe_mode = 2'b11` if $P_{\max} < 16$).

If we use all 64 PEs:

$$
N_{\text{active}}=64
$$

then all available PEs (`col_active = 16'hFFFF`) participate in the computation.

If the policy selects only 32 active PEs:

$$
N_{\text{active}}=32
$$

only half of the PE columns (`col_active = 16'h00FF`) are active:

$$
\frac{32}{64}\times100 = 50\% \text{ active} \implies 100-50=\boxed{50\%} \text{ active PE logic saved}
$$

Similarly, with 16 active PEs (`col_active = 16'h000F`):

$$
\frac{16}{64}\times100 = 25\% \text{ active} \implies 100-25=\boxed{75\%} \text{ active PE logic saved}
$$

---

## 9. Step 8 — Multi-Pass Channel Tiling

When physically 64 PEs exist (`16` output columns across `4` rows), running with fewer active PEs means we cannot process all 64 accumulators/channels simultaneously.

Therefore, SparseFlex (`channel_tile_controller.sv`) divides the computation into multiple passes.

The number of passes is:

$$
P=\frac{64}{N_{\text{active}}}
$$

For 64 PEs:

$$
P=\frac{64}{64}=\boxed{1\text{ pass}}
$$

For 32 PEs:

$$
P=\frac{64}{32}=\boxed{2\text{ passes}}
$$

For 16 PEs:

$$
P=\frac{64}{16}=\boxed{4\text{ passes}}
$$

This is the basic multi-pass channel tiling mechanism.

---

## 10. Step 9 — 64-PE Configuration

First, consider:

$$
N_{\text{active}}=64 \implies P=1
$$

Therefore the accelerator processes all 64 channels (128 packed output words) in a single pass.

```text
64 channels
     |
     v
+----------------+
|    64 PEs      |
+----------------+
     |
     v
   Output
```

No additional channel pass is required.

---

## 11. Step 10 — 32-PE Configuration

Now configure:

$$
N_{\text{active}}=32 \implies P=\frac{64}{32}=2
$$

So the accelerator performs:

```text
Pass 1:
Channels 0 - 31 (64 words)
      |
      v
   32 PEs

Pass 2:
Channels 32 - 63 (64 words)
      |
      v
   32 PEs
```

The outputs from both passes are combined into the output buffer:

$$
Y = Y_{\text{pass1}} \cup Y_{\text{pass2}} \quad (\text{128 words total preserved})
$$

This reduces active PE logic by 50% while preserving every output channel.

---

## 12. Step 11 — 16-PE Configuration

Now suppose:

$$
N_{\text{active}}=16 \implies P=\frac{64}{16}=4
$$

Therefore:

```text
Pass 1 -> Channels  0 - 15 (32 words)
Pass 2 -> Channels 16 - 31 (32 words)
Pass 3 -> Channels 32 - 47 (32 words)
Pass 4 -> Channels 48 - 63 (32 words)
```

All four output tiles are written sequentially into OFMAP SRAM across the four passes:

$$
Y = Y_1 \cup Y_2 \cup Y_3 \cup Y_4
$$

This is how SparseFlex trades computation passes for reduced active hardware resources.

---

## 13. Step 12 — SRAM and Ping-Pong Operation

SparseFlex uses a **41,472-byte, 8-bank interleaved SRAM subsystem** (`multibank_sram_subsystem.sv`, 8 banks $\times$ 5,184 bytes/bank) partitioned by `ping_pong_buffer_controller.sv` into two logical ping-pong buffers:

```text
Buffer A  (Producer/Consumer Ping)
Buffer B  (Consumer/Producer Pong)
```

While one buffer feeds the PE array via SRAM Port B, the other buffer is filled by DMA via SRAM Port A:

```text
Layer / Tile 1:
Buffer A -> PE computation (Read via Port B)
Buffer B -> DMA loads next data (Write via Port A)

Layer / Tile 2:
Buffer B -> PE computation (Read via Port B)
Buffer A -> DMA loads next data (Write via Port A)

Layer / Tile 3:
Buffer A -> PE computation (Read via Port B)
Buffer B -> DMA loads next data (Write via Port A)
```

This overlaps DMA memory transfers with compute without bank stalls or read-after-write conflicts.

---

## 14. Step 13 — Q4.12 Fixed-Point Representation

SparseFlex uses signed **Q4.12** fixed-point representation:

- 1 sign bit + 3 integer bits (4 integer/sign bits total)
- 12 fractional bits

The total width is:

$$
4+12=16\text{ bits}
$$

For example, suppose we want to represent $1.5$:

$$
1.5\times2^{12}
=1.5\times4096
=\boxed{6144} \quad (\mathbf{16\text{'h}1800})
$$

Similarly, integer operands in our matrix example map cleanly into Q4.12 inside its $[-8.0, +7.999755]$ range:
- $1.0 \to 4096$ (`16'h1000`)
- $2.0 \to 8192$ (`16'h2000`)
- $3.0 \to 12288$ (`16'h3000`)

---

## 15. Step 14 — Accumulation & Requantization

Multiplying two 16-bit Q4.12 values yields a 32-bit **Q8.24** product ($B_{\text{frac}} = 24$). Accumulating across large reduction depths would overflow a 16-bit register, so SparseFlex uses a:

$$
\boxed{40\text{-bit accumulator}} \quad (\text{Q16.24, with 8 guard bits})
$$

Each active product contributes to the 40-bit accumulator (`mac_unit_40b.sv`):

$$
Y=A_1W_1+A_2W_2+A_3W_3+A_4W_4
$$

For Row 0 ($3.0$ in real arithmetic):
- Accumulator value in Q16.24: $3.0 \times 2^{24} = 50,331,648$ (`40'h00_0300_0000`)
- During drain, `requantization_unit.sv` adds the rounding offset $2^{12-1} = 2048$, performs arithmetic right-shift by 12 (`>>> 12`), and saturates to 16 bits, yielding:
  $$12,288 \quad (\mathbf{16\text{'h}3000} \equiv 3.0\text{ in Q4.12})$$

The 8 guard bits provide headroom for up to $2^8 = 256$ worst-case full-scale additions without overflow.

---

## 16. Step 15 — Why Zero-Gating Is Important

Comparing the two situations:

### Without zero-gating

```text
Activation
    |
    v
Multiply
    |
    v
Accumulate
```

Even when $A = 0$, the datapath performs unnecessary switching.

### With SparseFlex

```text
Activation
    |
    v
Zero Detector
    |
    +------ A = 0 ------> GATE MAC (bypass_mac = 1)
    |
    +------ A != 0 -----> ENABLE MAC
```

Therefore, $A = 0$ disables the corresponding MAC operation, reducing unnecessary:

- weight SRAM reads (on all-zero 4-row groups)
- multiplication switching activity
- accumulator register toggling

---

## 17. Step 16 — Resource Scaling

Comparing the three hardware configurations:

| Configuration | Active PEs | Number of Passes | Active Logic | Active Logic Reduction |
|---|---:|---:|---:|---:|
| Full | 64 | 1 | 100% | 0% |
| Medium | 32 | 2 | 50% | **50%** |
| Low | 16 | 4 | 25% | **75%** |

Thus, compared with the 64-PE baseline:

$$
32\text{ PEs} \rightarrow 50\%\text{ active logic reduction}
$$

$$
16\text{ PEs} \rightarrow 75\%\text{ active logic reduction}
$$

---

## 18. Step 17 — Trade-off of Multi-Pass Execution

Reducing active PEs does not come for free: fewer active PEs require more channel passes:

$$
64\text{ PEs} \rightarrow 1\text{ pass} \qquad 32\text{ PEs} \rightarrow 2\text{ passes} \qquad 16\text{ PEs} \rightarrow 4\text{ passes}
$$

Because activations must be re-read across each channel pass, **activation SRAM reads scale with the number of passes**:

- **32-PE mode** (2 passes): **+100% increase** in activation SRAM reads.
- **16-PE mode** (4 passes): **+300% increase** in activation SRAM reads.

So SparseFlex explicitly exposes the fundamental hardware trade-off between:

$$
\boxed{\text{Active Compute Logic}} \quad \longleftrightarrow \quad \boxed{\text{Memory Traffic / Execution Cycles}}
$$

---

## 19. Step 18 — Complete SparseFlex Flow

```text
             INPUT ACTIVATIONS
                    |
                    v
          +-------------------+
          |  8-Bank SRAM      |
          | (Buffer A / B)    |
          +-------------------+
                    |
                    v
          +-------------------+
          | Zero Detection    |
          +-------------------+
                    |
             +------+------+
             |             |
          Zero           Non-zero
             |             |
             v             v
        MAC GATED      MAC ENABLED
             |             |
             +------+------+
                    |
                    v
          +-------------------+
          |     PE ARRAY      |
          |  16 / 32 / 64 PEs |
          +-------------------+
                    |
                    v
          Multi-Pass Tiling (P = 1, 2, or 4)
                    |
                    v
          +-------------------+
          | 40-bit Accumulator|
          +-------------------+
                    |
                    v
          +-------------------+
          |  Requantization   |
          | (Q16.24 -> Q4.12) |
          +-------------------+
                    |
                    v
             OUTPUT RESULT
```

---

## 20. Final Example Calculation Summary

For our example:

$$
A=
\begin{bmatrix}
1&0&2&0\\
0&3&0&1\\
2&0&1&0\\
0&1&0&2
\end{bmatrix}
$$

- **Total activation values:** $16$
- **Zero activation values:** $8$
- **Activation Sparsity:** $\frac{8}{16} = \mathbf{50\%}$
- **Dense MACs:** $16$ multiplications
- **Sparse useful MACs:** $8$ multiplications
- **MAC reduction:**

$$
\frac{16-8}{16}\times100 = \boxed{50\%}
$$

- **Output Vector:** $Y = [3, 4, 4, 5]^T$ (identical in dense and sparse execution)
- **Channel Passes by Mode:** $P = \frac{64}{64} = 1$, $P = \frac{64}{32} = 2$, $P = \frac{64}{16} = 4$

---

## 21. Final Presentation Statement

The main contribution of SparseFlex is not simply trying to make CNN execution faster at the cost of unpredictable timing. Instead, it provides **two orthogonal levels of deterministic hardware flexibility**:

1. **Computation-level sparsity gating:** Zero activations are detected synchronously; multipliers and accumulators are gated without introducing pipeline jitter.
2. **Architecture-level PE reconfiguration:** Active PEs scale cleanly across $64$, $32$, or $16$ units via hardware policy control, using multi-pass channel tiling to preserve all output channels.

Therefore, SparseFlex establishes a transparent, controllable trade-off between **MAC switching activity, active PE utilization, SRAM read traffic, and cycle latency**:

$$
\boxed{
\text{SparseFlex}
=
\text{Synchronous Zero-Gating}
+
\text{Configurable PE Array}
+
\text{Multi-Pass Channel Tiling}
}
$$

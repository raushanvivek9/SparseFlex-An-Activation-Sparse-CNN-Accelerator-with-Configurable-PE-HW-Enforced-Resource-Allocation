#!/usr/bin/env python3
"""
generate_fig01_diagram.py
Generates a publication-grade, professional microarchitectural schematic of the
Neural_Acc accelerator for IEEE/ACM paper submissions (DAC, ISCA, DATE, ASAP, TVLSI).
Outputs:
  - NEURAL_ACC_PAPER/plots/fig01_system_architecture.png (300 DPI High-Resolution)
  - NEURAL_ACC_PAPER/plots/fig01_system_architecture.svg (Scalable Vector Graphic)
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path

def create_architecture_diagram():
    # Output paths
    output_dir = os.path.join(os.path.dirname(__file__), "plots")
    os.makedirs(output_dir, exist_ok=True)
    png_path = os.path.join(output_dir, "fig01_system_architecture.png")
    svg_path = os.path.join(output_dir, "fig01_system_architecture.svg")

    # Canvas Setup: 20 x 12.5 inches for crisp 300 DPI publication quality
    fig = plt.figure(figsize=(20, 12.5), dpi=300)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    # Professional Academic Color Palette
    BG_COLOR = "#FFFFFF"
    PANEL_BG = "#F8FAFC"
    PANEL_BORDER = "#CBD5E1"
    
    # Subsystem Theme Colors
    HOST_BG, HOST_BORDER, HOST_TXT = "#F1F5F9", "#64748B", "#0F172A"
    CTRL_BG, CTRL_BORDER, CTRL_TXT = "#EEF2FF", "#6366F1", "#1E1B4B"
    MEM_BG, MEM_BORDER, MEM_TXT   = "#ECFDF5", "#10B981", "#064E3B"
    GATE_BG, GATE_BORDER, GATE_TXT = "#FDF2F8", "#EC4899", "#701A75"
    PE_BG, PE_BORDER, PE_TXT       = "#EFF6FF", "#3B82F6", "#1E3A8A"
    PE_ACTIVE_BG, PE_ACTIVE_BRD    = "#DBEAFE", "#2563EB"
    PE_GATED_BG, PE_GATED_BRD      = "#E2E8F0", "#94A3B8"
    DRAIN_BG, DRAIN_BRD, DRAIN_TXT = "#FFFBEB", "#F59E0B", "#78350F"
    BUS_COLOR = "#334155"
    BUS_HL = "#DC2626"
    BUS_GREEN = "#059669"
    BUS_PURPLE = "#9333EA"

    fig.patch.set_facecolor(BG_COLOR)

    # -------------------------------------------------------------------------
    # Helper Functions for Drawing Beautiful Boxes and Buses
    # -------------------------------------------------------------------------
    def draw_box(x, y, w, h, bg, border, title="", subtitle="", radius=1.0, lw=1.5, title_size=10, sub_size=8, title_col="#0F172A", sub_col="#475569", align="center"):
        rect = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle=f"round,pad=0,rounding_size={radius}",
            linewidth=lw, edgecolor=border, facecolor=bg, zorder=2
        )
        ax.add_patch(rect)
        if title:
            ty = y + h * 0.65 if subtitle else y + h * 0.5
            tx = x + w * 0.5 if align == "center" else x + 1.2
            ax.text(tx, ty, title, ha=align, va="center", fontsize=title_size, fontweight="bold", color=title_col, zorder=3)
        if subtitle:
            sy = y + h * 0.35 if title else y + h * 0.5
            sx = x + w * 0.5 if align == "center" else x + 1.2
            ax.text(sx, sy, subtitle, ha=align, va="center", fontsize=sub_size, color=sub_col, zorder=3)
        return rect

    def draw_subgraph(x, y, w, h, title, bg, border, header_col):
        rect = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0,rounding_size=1.5",
            linewidth=1.8, edgecolor=border, facecolor=bg, linestyle="--", zorder=1
        )
        ax.add_patch(rect)
        # Header Badge
        header_w = min(w * 0.7, len(title) * 1.1 + 4)
        h_badge = patches.FancyBboxPatch(
            (x + 2, y + h - 2.8), header_w, 2.6,
            boxstyle="round,pad=0,rounding_size=0.8",
            linewidth=1.2, edgecolor=border, facecolor=header_col, zorder=2
        )
        ax.add_patch(h_badge)
        ax.text(x + 2 + header_w * 0.5, y + h - 1.5, title, ha="center", va="center", fontsize=9.5, fontweight="bold", color="#FFFFFF", zorder=3)

    def draw_bus(x1, y1, x2, y2, color=BUS_COLOR, lw=2.0, label="", label_pos=(0.5, 0.5), label_side="top", arrow=True, dashed=False):
        style = "--" if dashed else "-"
        ax.plot([x1, x2], [y1, y2], color=color, linewidth=lw, linestyle=style, zorder=4)
        if arrow:
            dx = (x2 - x1)
            dy = (y2 - y1)
            dist = (dx**2 + dy**2)**0.5
            if dist > 0:
                ax.annotate("", xy=(x2, y2), xytext=(x2 - dx/dist*1.2, y2 - dy/dist*1.2),
                            arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=12), zorder=5)
        if label:
            lx = x1 + (x2 - x1) * label_pos[0]
            ly = y1 + (y2 - y1) * label_pos[1]
            offset_y = 0.8 if label_side == "top" else -0.8
            ax.text(lx, ly + offset_y, label, ha="center", va="center", fontsize=7.5, fontweight="bold",
                    color=color, bbox=dict(boxstyle="round,pad=0.2", facecolor="#FFFFFF", edgecolor=color, lw=0.6, alpha=0.95), zorder=6)

    def draw_orthogonal_bus(points, color=BUS_COLOR, lw=2.0, label="", label_idx=1, label_side="top", arrow=True, dashed=False):
        style = "--" if dashed else "-"
        for i in range(len(points)-1):
            x1, y1 = points[i]
            x2, y2 = points[i+1]
            ax.plot([x1, x2], [y1, y2], color=color, linewidth=lw, linestyle=style, zorder=4)
        if arrow:
            x1, y1 = points[-2]
            x2, y2 = points[-1]
            dx = (x2 - x1)
            dy = (y2 - y1)
            dist = (dx**2 + dy**2)**0.5
            if dist > 0:
                ax.annotate("", xy=(x2, y2), xytext=(x2 - dx/dist*1.2, y2 - dy/dist*1.2),
                            arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, mutation_scale=12), zorder=5)
        if label:
            x1, y1 = points[label_idx]
            x2, y2 = points[label_idx+1]
            lx = (x1 + x2) * 0.5
            ly = (y1 + y2) * 0.5
            offset_y = 0.8 if label_side == "top" else -0.8
            offset_x = 0.8 if label_side == "right" else (-0.8 if label_side == "left" else 0)
            ax.text(lx + offset_x, ly + offset_y, label, ha="center", va="center", fontsize=7.5, fontweight="bold",
                    color=color, bbox=dict(boxstyle="round,pad=0.2", facecolor="#FFFFFF", edgecolor=color, lw=0.6, alpha=0.95), zorder=6)

    # =========================================================================
    # 1. TOP HEADER BANNER
    # =========================================================================
    draw_box(2, 92.5, 96, 6.0, "#0F172A", "#1E293B",
             title="Neural_Acc: Activation-Sparse CNN Accelerator Top-Level Microarchitecture",
             subtitle="Synthesizable RTL Datapath with Reconfigurable 16/32/64 PE Array, Synchronous Zero-Gating & Hardware-Enforced Policy Interlocks",
             radius=1.2, lw=1.5, title_size=14, sub_size=9.5, title_col="#F8FAFC", sub_col="#94A3B8")

    # =========================================================================
    # 2. EXTERNAL INTERFACES & HOST DOMAIN (Left Column: X = 2..21)
    # =========================================================================
    draw_subgraph(2, 54, 19, 36.5, "1. External Interfaces & Host", HOST_BG, HOST_BORDER, "#475569")

    # Host Processor / SoC
    draw_box(3.5, 76, 16, 11, HOST_BG, HOST_BORDER,
             title="Host CPU / SoC",
             subtitle="• Runtime Constraints: L_max, P_max\n• Optimization Policy: pol_sel (A/B)\n• Layer Descriptors & Ingestion Trigger\n• Layer Done / Completion Handshake",
             radius=0.8, lw=1.2, title_size=9, sub_size=7.2, title_col=HOST_TXT, sub_col="#334155", align="left")

    # External DRAM / System Bus
    draw_box(3.5, 57, 16, 14, HOST_BG, HOST_BORDER,
             title="External DRAM / AXI4",
             subtitle="• Model Weights (Q4.12 Signed)\n• Input Activations (Q4.12 Words)\n• 64-bit / 32-bit Memory Controller\n• AXI4 Stream Master Read Port\n  [m_axi_araddr, m_axi_rdata]",
             radius=0.8, lw=1.2, title_size=9, sub_size=7.2, title_col=HOST_TXT, sub_col="#334155", align="left")

    # =========================================================================
    # 3. CONTROL PLANE & POLICY ARBITRATION (Top Middle: X = 23..63, Y = 62..89.5)
    # =========================================================================
    draw_subgraph(23, 62, 40, 28.5, "2. Hardware Control Plane & Policy Engine", CTRL_BG, CTRL_BORDER, "#4338CA")

    # Layer Command Sequencer (TSK-05)
    draw_box(24.5, 75, 17, 12, CTRL_BG, CTRL_BORDER,
             title="Layer Command Sequencer (TSK-05)",
             subtitle="• 16-Entry Inbound Command FIFO\n• Master Sequencer 6-State FSM:\n  IDLE -> CONFIG -> INGEST -> COMPUTE -> DRAIN\n• Hardware Barrier Synchronization\n• Completion & Interrupt Handshake",
             radius=0.8, lw=1.3, title_size=8.5, sub_size=7.0, title_col=CTRL_TXT, sub_col="#312E81", align="left")

    # Transparent Hardware Policy Controller (TSK-33 / TSK-35A)
    draw_box(43.5, 75, 18, 12, CTRL_BG, BUS_HL,
             title="Hardware Policy Controller (TSK-33/35A)",
             subtitle="• Single-Cycle Combinational Arbitration\n• Policy A: Min PEs under L_max (Energy)\n• Policy B: Max Slack under P_max (Speed)\n• FAIL-SAFE INTERLOCK: P_max < 16\n  -> invalid_pe_limit=1, exec_enable=0\n  -> Locks mode to 2'b11 (Safe Quiescence)",
             radius=0.8, lw=1.6, title_size=8.0, sub_size=6.8, title_col="#991B1B", sub_col="#7F1D1D", align="left")

    # Ping-Pong Buffer Controller (TSK-04)
    draw_box(24.5, 64, 17, 8.5, CTRL_BG, CTRL_BORDER,
             title="Ping-Pong Buffer Controller (TSK-04)",
             subtitle="• Logical Invariant: Producer != Consumer\n• Ingestion Buffer (Bank A) vs Compute (Bank B)\n• Atomic Role Swap on Layer Barrier",
             radius=0.8, lw=1.2, title_size=8.0, sub_size=6.8, title_col=CTRL_TXT, sub_col="#312E81", align="left")

    # K-Progress Tracker & Multi-Pass Tiler (TSK-07 / TSK-28)
    draw_box(43.5, 64, 18, 8.5, CTRL_BG, CTRL_BORDER,
             title="K-Progress Tracker & Tiler (TSK-07/28)",
             subtitle="• Reduction Depth: K = 3x3x64 = 576 terms\n• Chunk Progress: 0..8 (64 terms / chunk)\n• Multi-Pass Tiler: P = 1 (64PE) / 2 (32PE) / 4 (16PE)\n• Drives accum_clear (Chk 0) & drain_req (Chk 8)",
             radius=0.8, lw=1.2, title_size=8.0, sub_size=6.8, title_col=CTRL_TXT, sub_col="#312E81", align="left")

    # =========================================================================
    # 4. MEMORY SUBSYSTEM (Middle Left: X = 2..36, Y = 2..51)
    # =========================================================================
    draw_subgraph(2, 2, 34, 49.5, "3. Interleaved Multi-Bank SRAM Subsystem (41,472 Bytes)", MEM_BG, MEM_BORDER, "#047857")

    # DMA Controller (TSK-06)
    draw_box(3.5, 38, 14, 10.5, MEM_BG, MEM_BORDER,
             title="DMA Master Controller (TSK-06)",
             subtitle="• AXI4 Read Channel Master\n• Programmable Burst Length (1..256)\n• 32-bit Internal Ingestion FIFO\n• Automatic Tile Boundary Stride",
             radius=0.8, lw=1.2, title_size=8.2, sub_size=6.8, title_col=MEM_TXT, sub_col="#065F46", align="left")

    # DMA Write Adapter
    draw_box(19.5, 38, 15, 10.5, MEM_BG, MEM_BORDER,
             title="DMA-to-SRAM Write Adapter",
             subtitle="• 32-bit to Dual 16-bit Deserializer\n• SRAM Port A0 Write Router\n• Ping-Pong Base Address Offset\n• Write Handshake Protocol",
             radius=0.8, lw=1.2, title_size=8.2, sub_size=6.8, title_col=MEM_TXT, sub_col="#065F46", align="left")

    # 8-Bank Hybrid Dual-Port SRAM Array
    draw_box(3.5, 13, 31, 22.5, "#F0FDF4", "#059669",
             title="8-Bank Interleaved Dual-Port Hybrid SRAM (TSK-03: 41,472 Bytes Total)",
             subtitle="", radius=1.0, lw=1.5, title_size=8.8, sub_size=7.0, title_col="#064E3B", align="center")

    # Individual SRAM Banks (8 Banks)
    for bi in range(8):
        bx = 4.8 + bi * 3.65
        by = 17.5
        bw = 3.3
        bh = 14.5
        draw_box(bx, by, bw, bh, "#DCFCE7", "#10B981",
                 title=f"Bank {bi}",
                 subtitle="5,184 B\n(16b Q4.12)\n\nPort A (W)\nPort B (R)",
                 radius=0.5, lw=1.0, title_size=7.5, sub_size=6.2, title_col="#064E3B", sub_col="#047857", align="center")

    # Memory Telemetry Monitor (TSK-20)
    draw_box(3.5, 4.5, 31, 6.5, MEM_BG, "#059669",
             title="Memory Telemetry & Diagnostics Monitor (TSK-20)",
             subtitle="• Real-time Conflict Profiler • Read/Write Stall Counters • Out-of-Bounds Protection\n• Multi-Pass Memory Traffic Measurement: +100% (32-PE) & +300% (16-PE) Activation Reads",
             radius=0.8, lw=1.2, title_size=8.0, sub_size=6.8, title_col=MEM_TXT, sub_col="#065F46", align="center")

    # =========================================================================
    # 5. ZERO-GATING & OPERAND DISPATCH (Center Column: X = 38..59, Y = 2..59)
    # =========================================================================
    draw_subgraph(38, 2, 22, 57.5, "4. Synchronous Zero-Gating & Dispatch", GATE_BG, GATE_BORDER, "#BE185D")

    # Datapath Compute Feeder
    draw_box(39.5, 38, 19, 18, GATE_BG, GATE_BORDER,
             title="Datapath Compute Feeder (TSK-07)",
             subtitle="• Dedicated Port B 8-Bank Parallel Reader\n• Activation & Weight Unpack / Alignment\n• Spatial Coordinate Stride Sequencer\n• Broadcast Bus Drivers:\n  - 4 Rows: Shared Input Activation Words\n  - 16 Cols: Independent Weight Filter Words\n• Handshake: Synchronous Step Control",
             radius=0.8, lw=1.3, title_size=8.5, sub_size=7.0, title_col=GATE_TXT, sub_col="#831843", align="left")

    # Slot Control Unit & Zero Detector
    draw_box(39.5, 17, 19, 18, GATE_BG, "#BE185D",
             title="Slot Control Unit & Zero Detector (SCU)",
             subtitle="• Fine-Grained Dynamic Zero Comparator:\n  IsZero = (Activation_In == 16'h0000)\n• SYNCHRONOUS WEIGHT READ GATING:\n  SRAM_EN_W = ~IsZero\n  -> Eliminates Wordline & Sense-Amp Power\n• MAC CLOCK ENABLE MODULATION:\n  MAC_CE = ~IsZero\n  -> Gates Multiplier & Accumulator Switching\n• ZERO LATENCY IMPACT: 0.00% Latency Delta\n  (Cycle-Invariant Deterministic Pipeline)",
             radius=0.8, lw=1.5, title_size=8.5, sub_size=6.8, title_col="#831843", sub_col="#701A75", align="left")

    # Output Requantization & OFMAP Drain
    draw_box(39.5, 4.5, 19, 10, DRAIN_BG, DRAIN_BRD,
             title="OFMAP Drain & Requantization (TSK-11)",
             subtitle="• Reads 64 Parallel 40-bit Accumulators\n• Saturated Truncation (INT40 -> Q4.12 Signed)\n• Port A1 Writeback Router (Banks 0..7)\n• Generates layer_done_pulse upon Tile Drain",
             radius=0.8, lw=1.3, title_size=8.2, sub_size=6.8, title_col=DRAIN_TXT, sub_col="#92400E", align="left")

    # =========================================================================
    # 6. RECONFIGURABLE 64-PE PROCESSING ARRAY (Right: X = 62..98, Y = 2..89.5)
    # =========================================================================
    draw_subgraph(62, 2, 36, 88.5, "5. Configurable 64-PE Computing Array (4 Rows x 16 Columns)", PE_BG, PE_BORDER, "#1D4ED8")

    # Array Mode Indicator Box
    draw_box(63.5, 78.5, 33, 9.5, "#DBEAFE", "#2563EB",
             title="Array Allocation Modes (pe_array_40b)",
             subtitle="• 16-PE Mode (2'b00): Quadrant 0 Active (16 PEs) | Quadrants 1, 2, 3 Clock-Gated (4 Passes, 38,225 cyc)\n• 32-PE Mode (2'b01): Quadrants 0, 1 Active (32 PEs) | Quadrants 2, 3 Clock-Gated (2 Passes, 19,121 cyc)\n• 64-PE Mode (2'b10): All Quadrants Active (64 PEs) | Single-Pass Execution (9,569 cyc, Baseline)\n• Safe Inactive (2'b11): All 64 PEs Clock-Gated | P_max < 16 Interlock Asserted (0 Compute Cycles)",
             radius=0.8, lw=1.3, title_size=8.5, sub_size=6.8, title_col="#1E3A8A", sub_col="#1E40AF", align="left")

    # 4 Quadrants Display
    quad_info = [
        ("Quadrant 0 (Cols 0..3: 16 PEs)\nActive in: 16-PE, 32-PE, 64-PE Modes", 64.0, 56.5, 15.5, 20.0, PE_ACTIVE_BG, PE_ACTIVE_BRD, "#1E3A8A"),
        ("Quadrant 1 (Cols 4..7: 16 PEs)\nActive in: 32-PE, 64-PE Modes (Gated in 16-PE)", 80.5, 56.5, 15.5, 20.0, PE_ACTIVE_BG, PE_ACTIVE_BRD, "#1E3A8A"),
        ("Quadrant 2 (Cols 8..11: 16 PEs)\nActive ONLY in 64-PE Mode (Clock-Gated in 16/32-PE)", 64.0, 34.5, 15.5, 20.0, PE_GATED_BG, PE_GATED_BRD, "#475569"),
        ("Quadrant 3 (Cols 12..15: 16 PEs)\nActive ONLY in 64-PE Mode (Clock-Gated in 16/32-PE)", 80.5, 34.5, 15.5, 20.0, PE_GATED_BG, PE_GATED_BRD, "#475569")
    ]

    for q_title, qx, qy, qw, qh, qbg, qbrd, qcol in quad_info:
        draw_box(qx, qy, qw, qh, qbg, qbrd, title=q_title, subtitle="", radius=0.6, lw=1.2, title_size=7.2, sub_size=6.0, title_col=qcol, align="center")
        # Draw 4x4 PE grid cells inside each quadrant
        for r in range(4):
            for c in range(4):
                cell_x = qx + 0.8 + c * 3.4
                cell_y = qy + 1.2 + (3 - r) * 3.6
                cell_w = 3.0
                cell_h = 3.0
                is_active_quad = "Gated" not in q_title or "ONLY in 64-PE" not in q_title
                c_bg = "#EFF6FF" if "Gated" not in q_title else "#F1F5F9"
                c_brd = "#3B82F6" if "Gated" not in q_title else "#94A3B8"
                c_txt = "#1E3A8A" if "Gated" not in q_title else "#64748B"
                draw_box(cell_x, cell_y, cell_w, cell_h, c_bg, c_brd,
                         title=f"PE\nR{r}C{c}", subtitle="", radius=0.3, lw=0.8, title_size=6.2, title_col=c_txt, align="center")

    # Detailed Single-PE Microarchitecture Callout (Bottom of Datapath)
    draw_box(63.5, 4.5, 33, 28, "#FFFFFF", "#1E3A8A",
             title="Detailed Single Processing Element Datapath (mac_unit_40b)",
             subtitle="", radius=1.0, lw=1.6, title_size=9.0, title_col="#0F172A", align="center")

    # Inside Single PE Box: Subcomponents
    # Mult Unit
    draw_box(65.0, 16.5, 13.5, 13.5, "#EFF6FF", "#3B82F6",
             title="16b x 16b Signed Multiplier",
             subtitle="• Operands: Q4.12 Activation x Q4.12 Weight\n• Clock Enable Gated via Zero Detector\n• Dynamic Power Suppression: -48% to -85%\n• 32-bit Signed Product",
             radius=0.5, lw=1.0, title_size=7.8, sub_size=6.5, title_col="#1E3A8A", sub_col="#1E40AF", align="left")

    # 40b Accumulator Unit
    draw_box(81.0, 16.5, 14.0, 13.5, "#F0FDF4", "#10B981",
             title="40-bit Saturating Accumulator",
             subtitle="• 40-bit Register with 24 Guard Bits\n• Exact Numerical Fidelity: MAE = 0.000000\n• Max Intermediate Capacity: 16.7M MACs\n• accum_clear on Chunk 0\n• Sticky Saturation Detection",
             radius=0.5, lw=1.0, title_size=7.8, sub_size=6.5, title_col="#064E3B", sub_col="#047857", align="left")

    # Status / Gating logic in PE
    draw_box(65.0, 6.0, 30.0, 8.5, "#F8FAFC", "#64748B",
             title="PE Control & Clock-Gating Interface",
             subtitle="• col_enable[c] & enable: Master Quadrant Gating • mac_ce: Synchronous Activation Zero-Gate\n• accum_clear: Synchronous Reset to 0 • sat_clear: Sticky Flag Clear • Output: accum_out[r][c] (40-bit)",
             radius=0.5, lw=1.0, title_size=7.5, sub_size=6.5, title_col="#334155", sub_col="#475569", align="center")

    # Multiplier to Accumulator arrow inside callout
    draw_bus(78.5, 23.0, 81.0, 23.0, color="#2563EB", lw=2.0, label="32b Product", label_pos=(0.5, 0.5), label_side="top")

    # =========================================================================
    # 7. INTER-SUBSYSTEM BUSES & SIGNAL ROUTING
    # =========================================================================
    
    # 1. Host -> Sequencer (Layer Command Bus)
    draw_orthogonal_bus([(19.5, 83.0), (22.0, 83.0), (22.0, 83.0), (24.5, 83.0)],
                        color=BUS_COLOR, lw=2.0, label="cmd_valid, layer_id, L_max, P_max", label_idx=1, label_side="top")

    # 2. Sequencer -> Policy Controller
    draw_bus(41.5, 81.0, 43.5, 81.0, color=BUS_PURPLE, lw=2.0, label="req, L_max, P_max", label_pos=(0.5, 0.5), label_side="top")

    # 3. Policy Controller -> Sequencer (Resolved Mode & Safety)
    draw_bus(43.5, 77.5, 41.5, 77.5, color=BUS_HL, lw=2.0, label="mode[1:0], exec_en, invalid", label_pos=(0.5, 0.5), label_side="bottom")

    # 4. Policy Controller -> PE Array (Mode Select / Column Clock Gating)
    draw_orthogonal_bus([(52.5, 87.0), (52.5, 90.0), (79.0, 90.0), (79.0, 88.0)],
                        color=BUS_HL, lw=2.2, label="col_enable[15:0], cfg_mode[1:0], enable", label_idx=1, label_side="top")

    # 5. Sequencer -> Ping-Pong & K-Tracker
    draw_bus(33.0, 75.0, 33.0, 72.5, color=BUS_PURPLE, lw=1.8, label="buf_req", label_pos=(0.5, 0.5), label_side="right")
    draw_orthogonal_bus([(33.0, 75.0), (33.0, 73.5), (52.5, 73.5), (52.5, 72.5)],
                        color=BUS_PURPLE, lw=1.8, label="compute_start, k_total", label_idx=1, label_side="top")

    # 6. Host -> DMA Controller
    draw_orthogonal_bus([(11.5, 76.0), (11.5, 69.0), (10.5, 69.0), (10.5, 48.5)],
                        color=BUS_COLOR, lw=2.0, label="dma_start, src_addr, len", label_idx=1, label_side="left")

    # 7. External DRAM <-> DMA (AXI4 Master)
    draw_orthogonal_bus([(19.5, 64.0), (21.5, 64.0), (21.5, 53.0), (17.5, 53.0), (17.5, 48.5)],
                        color=BUS_GREEN, lw=2.2, label="AXI4 Master Read Bus (m_axi_ar*, m_axi_r*)", label_idx=1, label_side="right")

    # 8. DMA -> DMA Write Adapter
    draw_bus(17.5, 43.0, 19.5, 43.0, color=BUS_COLOR, lw=2.0, label="32b Flits", label_pos=(0.5, 0.5), label_side="top")

    # 9. DMA Write Adapter -> SRAM Array Port A0
    draw_orthogonal_bus([(27.0, 38.0), (27.0, 36.5)],
                        color=BUS_GREEN, lw=2.2, label="Port A0 Write: wr_req, addr, din [31:0]", label_idx=0, label_side="right")

    # 10. K-Progress Tracker -> Compute Feeder
    draw_orthogonal_bus([(52.5, 64.0), (52.5, 60.5), (49.0, 60.5), (49.0, 56.0)],
                        color=BUS_PURPLE, lw=2.0, label="chunk_idx [3:0], pass_idx [1:0], step", label_idx=1, label_side="top")

    # 11. SRAM Array Port B -> Compute Feeder (Parallel Read Bus)
    draw_orthogonal_bus([(34.5, 25.0), (36.5, 25.0), (36.5, 44.0), (39.5, 44.0)],
                        color=BUS_GREEN, lw=2.5, label="Port B 8-Bank Read Bus: rd_dout [0..7][31:0]", label_idx=1, label_side="left")

    # 12. Compute Feeder <-> Slot Control Unit (Zero Gating)
    draw_bus(46.0, 38.0, 46.0, 35.0, color=GATE_BORDER, lw=2.2, label="Act_In", label_pos=(0.5, 0.5), label_side="left")
    draw_bus(52.0, 35.0, 52.0, 38.0, color=BUS_HL, lw=2.2, label="wt_sram_ren (Gated)", label_pos=(0.5, 0.5), label_side="right")

    # 13. Slot Control Unit -> PE Array (Dynamic MAC Clock Enable Gate)
    draw_orthogonal_bus([(58.5, 26.0), (60.5, 26.0), (60.5, 11.5), (65.0, 11.5)],
                        color=BUS_HL, lw=2.2, label="mac_ce (Gated on Zero)", label_idx=1, label_side="top")

    # 14. Compute Feeder -> PE Array (Broadcast Data Buses)
    draw_orthogonal_bus([(58.5, 48.0), (60.5, 48.0), (60.5, 52.0), (64.0, 52.0)],
                        color="#2563EB", lw=2.5, label="act_data_row[0..3] (Row Broadcast)", label_idx=1, label_side="top")
    draw_orthogonal_bus([(58.5, 44.0), (61.5, 44.0), (61.5, 48.0), (64.0, 48.0)],
                        color="#059669", lw=2.5, label="weight_data[0..15] (Column Filters)", label_idx=1, label_side="bottom")

    # 15. K-Progress Tracker -> PE Array (accum_clear)
    draw_orthogonal_bus([(58.5, 68.0), (60.5, 68.0), (60.5, 66.0), (64.0, 66.0)],
                        color=BUS_PURPLE, lw=1.8, label="accum_clear (Chunk 0)", label_idx=0, label_side="top")

    # 16. K-Progress Tracker -> OFMAP Drain (drain_req)
    draw_orthogonal_bus([(43.5, 68.0), (37.0, 68.0), (37.0, 11.0), (39.5, 11.0)],
                        color=BUS_PURPLE, lw=1.8, label="drain_req (Chunk 8)", label_idx=1, label_side="left")

    # 17. PE Array Accumulator Outputs -> OFMAP Drain
    draw_orthogonal_bus([(65.0, 5.0), (60.0, 5.0), (60.0, 7.5), (58.5, 7.5)],
                        color=DRAIN_BRD, lw=2.2, label="64x accum_out[39:0]", label_idx=1, label_side="top")

    # 18. OFMAP Drain -> SRAM Array Port A1 (Writeback)
    draw_orthogonal_bus([(39.5, 8.0), (36.0, 8.0), (36.0, 15.0), (34.5, 15.0)],
                        color=DRAIN_BRD, lw=2.2, label="Port A1 Writeback: wr_req, addr, din", label_idx=1, label_side="bottom")

    # 19. OFMAP Drain -> Sequencer -> Host (Done Pulse)
    draw_orthogonal_bus([(49.0, 14.5), (49.0, 16.0), (38.0, 16.0), (38.0, 76.0), (41.5, 76.0)],
                        color=DRAIN_BRD, lw=1.8, label="layer_done_pulse", label_idx=2, label_side="left")
    draw_orthogonal_bus([(24.5, 87.0), (21.5, 87.0), (21.5, 87.0), (19.5, 87.0)],
                        color=HOST_BORDER, lw=2.0, label="layer_done_id / Interrupt", label_idx=1, label_side="top")

    # =========================================================================
    # 8. LEGEND & ANNOTATIONS (Bottom Left / Bottom Banner)
    # =========================================================================
    draw_box(2, 0.4, 96, 1.4, "#F8FAFC", "#E2E8F0",
             title="Bus Legend:   [Black/Gray] Standard Control & Flit Bus   |   [Green] SRAM Port A/B Memory Access Buses   |   [Red] Synchronous Zero-Gating & Safety Interlocks   |   [Purple] K-Reduction & Sequencer Control   |   [Blue] PE Broadcast Operands   |   [Amber] Output Drain & Requantization",
             subtitle="", radius=0.4, lw=1.0, title_size=7.5, title_col="#334155", align="center")

    # Save outputs
    plt.savefig(png_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.savefig(svg_path, format="svg", facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()
    print(f"SUCCESS: High-resolution architecture diagram saved to:\n  PNG: {png_path}\n  SVG: {svg_path}")

if __name__ == "__main__":
    create_architecture_diagram()


#!/usr/bin/env python3
"""
SparseFlex: M.Tech Defense Presentation (.pptx) Generator
Creates a 15-slide 16:9 widescreen PowerPoint presentation combining:
- Mandatory M.Tech evaluation criteria (Problem, Inputs, Outputs, Approach, Literature, Dataset/Metrics, Effort, Rigor)
- End-to-End 7-phase hardware pipeline & Policy Engine (L_max, P_max)
- Complete Working Example (4x4 Matrix A, Weight W, 50% sparsity, Multi-Pass P=1/2/4, Ping-Pong SRAM, Q4.12 & 40b, Trade-off)
- Verified TSK-33/TSK-37 experimental results and regression proof
"""

import os
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
OUT_PPTX = os.path.join(REPO_ROOT, "SparseFlex_MTech_Presentation.pptx")

# Colors — IIT Tirupati Maroon + Clean Slate Theme
MAROON       = RGBColor(0x80, 0x00, 0x00)
MAROON_DARK  = RGBColor(0x4A, 0x04, 0x04)
MAROON_LIGHT = RGBColor(0xFB, 0xF3, 0xF3)
NAVY         = RGBColor(0x0F, 0x17, 0x2A)
SLATE_DARK   = RGBColor(0x1E, 0x29, 0x3B)
SLATE_MUTED  = RGBColor(0x47, 0x55, 0x69)
BORDER_GRAY  = RGBColor(0xCB, 0xD5, 0xE1)
BG_LIGHT     = RGBColor(0xF8, 0xFA, 0xFC)
WHITE        = RGBColor(0xFF, 0xFF, 0xFF)
GREEN        = RGBColor(0x15, 0x80, 0x3D)
GREEN_LIGHT  = RGBColor(0xEC, 0xFD, 0xF5)
BLUE         = RGBColor(0x1D, 0x4E, 0xD8)
BLUE_LIGHT   = RGBColor(0xEF, 0xF6, 0xFF)
AMBER        = RGBColor(0xB4, 0x53, 0x09)
AMBER_LIGHT  = RGBColor(0xFF, 0xFB, 0xEB)
RED_SOFT     = RGBColor(0xFE, 0xE2, 0xE2)
RED_TEXT     = RGBColor(0xB9, 0x1C, 0x1C)
TEAL         = RGBColor(0x0F, 0x76, 0x6E)
GOLD         = RGBColor(0xF5, 0x9E, 0x0B)

FONT_MAIN = "Segoe UI"
FONT_MONO = "Consolas"

TOTAL_SLIDES = 15


def set_slide_bg(slide, color):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_rect(slide, x, y, w, h, fill=None, line=None, line_pt=1.0, rounded=False):
    shape_type = MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE
    shp = slide.shapes.add_shape(shape_type, Inches(x), Inches(y), Inches(w), Inches(h))
    if rounded and len(shp.adjustments) > 0:
        shp.adjustments[0] = 0.06
    if fill is not None:
        shp.fill.solid()
        shp.fill.fore_color.rgb = fill
    else:
        shp.fill.background()
    if line is not None:
        shp.line.color.rgb = line
        shp.line.width = Pt(line_pt)
    else:
        shp.line.fill.background()
    return shp


def add_textbox(slide, x, y, w, h, text="", font_size=12, bold=False, color=NAVY,
                align=PP_ALIGN.LEFT, valign=MSO_ANCHOR.TOP, font_name=FONT_MAIN,
                margin_l=0.04, margin_r=0.04, margin_t=0.02, margin_b=0.02):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = valign
    tf.margin_left = Inches(margin_l)
    tf.margin_right = Inches(margin_r)
    tf.margin_top = Inches(margin_t)
    tf.margin_bottom = Inches(margin_b)
    if text:
        p = tf.paragraphs[0]
        p.alignment = align
        r = p.add_run()
        r.text = text
        r.font.name = font_name
        r.font.size = Pt(font_size)
        r.font.bold = bold
        r.font.color.rgb = color
    return tb


def add_rich_paragraphs(tf, items, default_size=11.5, default_color=SLATE_DARK, space_after=4):
    """items: list of either str or list of (text, bold, color, font_name, size) tuples."""
    tf.word_wrap = True
    for idx, item in enumerate(items):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.space_after = Pt(space_after)
        p.line_spacing = 1.15
        if isinstance(item, str):
            r = p.add_run()
            r.text = item
            r.font.name = FONT_MAIN
            r.font.size = Pt(default_size)
            r.font.color.rgb = default_color
        else:
            for seg in item:
                txt = seg[0]
                is_bold = seg[1] if len(seg) > 1 else False
                col = seg[2] if len(seg) > 2 else default_color
                fname = seg[3] if len(seg) > 3 else FONT_MAIN
                fsize = seg[4] if len(seg) > 4 else default_size
                r = p.add_run()
                r.text = txt
                r.font.name = fname
                r.font.size = Pt(fsize)
                r.font.bold = is_bold
                r.font.color.rgb = col


def add_image_fit(slide, img_path, x, y, max_w, max_h, center=True):
    """Add image preserving exact aspect ratio within (max_w, max_h)."""
    with Image.open(img_path) as im:
        iw, ih = im.size
    aspect = iw / ih
    box_aspect = max_w / max_h
    if aspect > box_aspect:
        w = max_w
        h = max_w / aspect
    else:
        h = max_h
        w = max_h * aspect
    px = x + (max_w - w) / 2.0 if center else x
    py = y + (max_h - h) / 2.0 if center else y
    return slide.shapes.add_picture(img_path, Inches(px), Inches(py), Inches(w), Inches(h))


def add_header_footer(slide, title, tag, slide_num, notes_text=""):
    set_slide_bg(slide, BG_LIGHT)
    # Top maroon bar
    add_rect(slide, 0, 0, 13.333, 0.08, fill=MAROON)
    # Title
    add_textbox(slide, 0.5, 0.18, 9.75, 0.48, title, font_size=19, bold=True, color=NAVY, valign=MSO_ANCHOR.MIDDLE)
    # Section tag pill on top right
    pill = add_rect(slide, 10.35, 0.22, 2.48, 0.34, fill=MAROON_LIGHT, line=MAROON, line_pt=1.0, rounded=True)
    tf = pill.text_frame
    tf.word_wrap = False
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = tag
    r.font.name = FONT_MAIN
    r.font.size = Pt(9.5)
    r.font.bold = True
    r.font.color.rgb = MAROON
    # Thin horizontal rule
    add_rect(slide, 0.5, 0.72, 12.333, 0.018, fill=BORDER_GRAY)
    # Footer rule & labels
    add_rect(slide, 0.5, 7.05, 12.333, 0.015, fill=BORDER_GRAY)
    add_textbox(slide, 0.5, 7.10, 8.5, 0.30,
                "SparseFlex  |  M.Tech Evaluation · Dept. of CSE, IIT Tirupati",
                font_size=9.5, color=SLATE_MUTED)
    add_textbox(slide, 11.3, 7.10, 1.533, 0.30,
                f"Slide {slide_num} / {TOTAL_SLIDES}",
                font_size=9.5, bold=True, color=MAROON, align=PP_ALIGN.RIGHT)
    if notes_text:
        slide.notes_slide.notes_text_frame.text = notes_text


def add_card(slide, x, y, w, h, title="", header_fill=MAROON, body_fill=WHITE, border=BORDER_GRAY):
    card = add_rect(slide, x, y, w, h, fill=body_fill, line=border, line_pt=1.0, rounded=True)
    if title:
        add_rect(slide, x, y, w, 0.36, fill=header_fill, line=header_fill, line_pt=0.5)
        add_textbox(slide, x + 0.10, y + 0.03, w - 0.20, 0.30, title,
                    font_size=12, bold=True, color=WHITE, valign=MSO_ANCHOR.MIDDLE)
    return card


def style_table_cell(cell, text, font_size=10.5, bold=False, color=NAVY, fill=None,
                     align=PP_ALIGN.CENTER, font_name=FONT_MAIN):
    if fill is not None:
        cell.fill.solid()
        cell.fill.fore_color.rgb = fill
    cell.vertical_anchor = MSO_ANCHOR.MIDDLE
    cell.margin_left = Inches(0.06)
    cell.margin_right = Inches(0.06)
    cell.margin_top = Inches(0.03)
    cell.margin_bottom = Inches(0.03)
    tf = cell.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    r = p.add_run()
    r.text = text
    r.font.name = font_name
    r.font.size = Pt(font_size)
    r.font.bold = bold
    r.font.color.rgb = color


def draw_matrix_grid(slide, x, y, cell_w, cell_h, matrix, highlight_zeros=True, header_label="", sub_label=""):
    if header_label:
        add_textbox(slide, x, y - 0.34, cell_w * len(matrix[0]), 0.30, header_label,
                    font_size=12, bold=True, color=NAVY, align=PP_ALIGN.CENTER)
    rows = len(matrix)
    cols = len(matrix[0])
    tbl_shape = slide.shapes.add_table(rows, cols, Inches(x), Inches(y),
                                       Inches(cell_w * cols), Inches(cell_h * rows))
    tbl = tbl_shape.table
    for c in range(cols):
        tbl.columns[c].width = Inches(cell_w)
    for r in range(rows):
        tbl.rows[r].height = Inches(cell_h)
        for c in range(cols):
            val = matrix[r][c]
            is_zero = (val == 0)
            if highlight_zeros and is_zero:
                bg = RED_SOFT
                fg = RED_TEXT
                is_b = True
            elif highlight_zeros:
                bg = BLUE_LIGHT
                fg = BLUE
                is_b = True
            else:
                bg = WHITE if (r % 2 == 0) else BG_LIGHT
                fg = NAVY
                is_b = True
            style_table_cell(tbl.cell(r, c), str(val), font_size=14, bold=is_b,
                             color=fg, fill=bg, font_name=FONT_MONO)
    if sub_label:
        add_textbox(slide, x, y + cell_h * rows + 0.06, cell_w * cols, 0.30, sub_label,
                    font_size=10.5, bold=True, color=SLATE_MUTED, align=PP_ALIGN.CENTER)
    return tbl_shape


def build_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank)
    set_slide_bg(s1, NAVY)
    add_rect(s1, 0, 0, 0.25, 7.5, fill=MAROON)
    add_rect(s1, 0.25, 0, 13.083, 0.10, fill=MAROON)

    # Top tag pill
    pill1 = add_rect(s1, 0.75, 0.70, 5.9, 0.40, fill=MAROON, rounded=True)
    p = pill1.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = "M.TECH PROJECT EVALUATION  |  DEPT. OF CSE, IIT TIRUPATI"
    r.font.name = FONT_MAIN; r.font.size = Pt(11); r.font.bold = True; r.font.color.rgb = WHITE

    add_textbox(s1, 0.75, 1.40, 8.9, 1.45,
                "SparseFlex: An Activation-Sparse CNN Accelerator",
                font_size=38, bold=True, color=WHITE)
    add_textbox(s1, 0.75, 2.90, 8.9, 0.90,
                "Reconfigurable 16 / 32 / 64 Processing Elements with Synchronous Zero-Gating\n"
                "& Hardware-Enforced Resource Allocation",
                font_size=18, bold=False, color=RGBColor(0xE2, 0xE8, 0xF0))

    # Key result callout box
    add_rect(s1, 0.75, 4.10, 8.85, 1.05, fill=MAROON_DARK, line=GOLD, line_pt=1.5, rounded=True)
    add_textbox(s1, 0.95, 4.22, 8.45, 0.80,
                "CORE ACHIEVEMENT: SparseFlex decouples switching-power reduction from timing jitter — "
                "achieving up to 84.92% weight-read & MAC switching savings with 0.00% cycle variation (9,569 cycles).",
                font_size=13.5, bold=True, color=RGBColor(0xFE, 0xF3, 0xC7), valign=MSO_ANCHOR.MIDDLE)

    # Presenter & Verification KPIs
    add_textbox(s1, 0.75, 5.55, 8.85, 0.90,
                "Presenter: Raushan Kumar   |   Indian Institute of Technology Tirupati\n"
                "RTL Verification: 20 Testbench Suites · 12,202 / 12,202 Checks Passing · MAE = 0.000000",
                font_size=13, bold=False, color=RGBColor(0xCB, 0xD5, 0xE1))

    # Right QR Card
    qr_card = add_rect(s1, 10.10, 1.75, 2.55, 3.35, fill=WHITE, line=BORDER_GRAY, line_pt=1.0, rounded=True)
    add_image_fit(s1, os.path.join(REPO_ROOT, "github_repo_qr.png"), 10.30, 1.92, 2.15, 2.15)
    add_textbox(s1, 10.20, 4.18, 2.35, 0.80,
                "Scan for GitHub Repo\nSystemVerilog RTL &\nVerification Scripts",
                font_size=11, bold=True, color=MAROON, align=PP_ALIGN.CENTER)

    add_rect(s1, 0.75, 6.85, 11.9, 0.02, fill=SLATE_MUTED)
    add_textbox(s1, 0.75, 6.95, 8.5, 0.35,
                "SparseFlex Hardware Accelerator Defense  |  2026",
                font_size=10, color=RGBColor(0x94, 0xA3, 0xB8))
    add_textbox(s1, 11.2, 6.95, 1.5, 0.35, "Slide 1 / 15", font_size=10, bold=True, color=WHITE, align=PP_ALIGN.RIGHT)

    s1.notes_slide.notes_text_frame.text = (
        "Good morning respected committee members and supervisor. Today I present SparseFlex, an activation-sparse "
        "CNN accelerator featuring reconfigurable 16, 32, and 64 processing elements with synchronous zero-gating and "
        "single-cycle hardware policy interlocks."
    )

    # =========================================================================
    # SLIDE 2: PROBLEM STATEMENT & SIGNIFICANCE (Mandatory A)
    # =========================================================================
    s2 = prs.slides.add_slide(blank)
    add_header_footer(s2, "Motivation & Problem Statement: The Real-Time Edge AI Bottleneck", "PROBLEM STATEMENT", 2,
        "Modern edge CNNs exhibit 48% to 85% zero activations post-ReLU. Asynchronous zero-skippers (SCNN, NullHop) "
        "cause load imbalance and unpredictable latency jitter, breaking safety-critical real-time deadlines. "
        "Adaptive accelerators also overlook on-chip SRAM read inflation when scaling down PEs.")

    cards2 = [
        ("1. The Energy & Thermal Wall", MAROON,
         [("Battery-powered edge SoCs operate under tight thermal limits (", False, SLATE_DARK),
          ("< 5W", True, MAROON), ("), while CNNs execute dense MACs and heavy SRAM traffic.", False, SLATE_DARK)],
         "Evaluating 0 x W consumes clock/multiplier/memory power for zero output."),
        ("2. High Natural Activation Sparsity", TEAL,
         [("Post-ReLU CNN feature maps contain ", False, SLATE_DARK),
          ("48.11% to 84.92% zeros", True, TEAL), (" across standard CIFAR-10/100 ResNet-18 & VGG-16-BN layers.", False, SLATE_DARK)],
         "Ignoring sparsity wastes over half of all hardware MAC operations."),
        ("3. Research Gap in Prior Accelerators", BLUE,
         [("Prior sparse accelerators (SCNN, NullHop) rely on ", False, SLATE_DARK),
          ("asynchronous queues", True, BLUE), (", causing severe spatial load imbalance & non-deterministic timing jitter.", False, SLATE_DARK)],
         "Safety-critical automotive/robotics tasks demand 0.00% latency jitter.")
    ]
    cy = 1.00
    for c_title, c_col, main_segs, foot_txt in cards2:
        add_card(s2, 0.50, cy, 5.75, 1.82, c_title, header_fill=c_col)
        tb = add_textbox(s2, 0.65, cy + 0.44, 5.45, 0.85)
        add_rich_paragraphs(tb.text_frame, [main_segs], default_size=12)
        add_rect(s2, 0.65, cy + 1.32, 5.45, 0.38, fill=BG_LIGHT, rounded=True)
        add_textbox(s2, 0.72, cy + 1.35, 5.30, 0.32, foot_txt, font_size=10.5, bold=True, color=c_col, valign=MSO_ANCHOR.MIDDLE)
        cy += 1.98

    # Right chart card
    add_card(s2, 6.45, 1.00, 6.38, 5.78, "Observed CNN Sparsity & Compute-Cycle Reduction", header_fill=SLATE_DARK)
    add_image_fit(s2, os.path.join(REPO_ROOT, "poster_sparsity_chart.png"), 6.60, 1.50, 6.08, 4.15)
    add_rect(s2, 6.65, 5.80, 5.98, 0.82, fill=MAROON_LIGHT, line=MAROON, line_pt=1.0, rounded=True)
    add_textbox(s2, 6.80, 5.88, 5.68, 0.66,
                "Research Opportunity: Eliminate 48%–85% redundant MAC switching AND scale active PEs dynamically "
                "while keeping total execution cycles strictly deterministic (0.00% jitter).",
                font_size=11.5, bold=True, color=MAROON, valign=MSO_ANCHOR.MIDDLE)

    # =========================================================================
    # SLIDE 3: ARCHITECTURE & INPUTS -> OUTPUTS OVERVIEW (Mandatory B & C)
    # =========================================================================
    s3 = prs.slides.add_slide(blank)
    add_header_footer(s3, "System Architecture: Inputs, Hardware Core & Outputs", "SYSTEM OVERVIEW", 3,
        "SparseFlex ingests signed 16-bit Q4.12 activations and weights alongside host latency and PE caps, "
        "computes inside 40-bit saturating MACs with zero-gating and ping-pong SRAM, and drains requantized Q4.12 OFMAPs.")

    add_rect(s3, 0.50, 0.88, 12.333, 4.35, fill=WHITE, line=BORDER_GRAY, line_pt=1.0, rounded=True)
    add_image_fit(s3, os.path.join(REPO_ROOT, "SparseFlex_Architecture_Block_Diagram.jpg"), 0.65, 0.94, 12.03, 4.22)

    io_cards = [
        ("INPUTS (What Enters the Chip)", MAROON, 0.50, [
            [("Data: ", True, MAROON), ("Activations (X) & Weights (W) in signed ", False, SLATE_DARK), ("Q4.12", True, NAVY), (" (16-bit)", False, SLATE_DARK)],
            [("Range: ", True, MAROON), ("[-8.0, +7.999755], LSB = 2^-12 (0.000244)", False, SLATE_DARK)],
            [("Control: ", True, MAROON), ("L_max (cycles), P_max (0..64), pol_sel, cmd", False, SLATE_DARK)]
        ]),
        ("COMPUTE ENGINE (SparseFlex Core)", SLATE_DARK, 4.70, [
            [("Feeder: ", True, NAVY), ("Zero comparator gates switching (", False, SLATE_DARK), ("0000h", True, TEAL, FONT_MONO), (")", False, SLATE_DARK)],
            [("Array: ", True, NAVY), ("4x16 grid (64 PEs); modes 16 / 32 / 64 PEs", False, SLATE_DARK)],
            [("Memory: ", True, NAVY), ("41,472B 8-bank Ping-Pong SRAM (Buffer A/B)", False, SLATE_DARK)]
        ]),
        ("OUTPUTS (What Leaves the Chip)", TEAL, 8.90, [
            [("OFMAP: ", True, TEAL), ("Requantized 16-bit ", False, SLATE_DARK), ("Q4.12", True, NAVY), (" packed in 32-bit words", False, SLATE_DARK)],
            [("Precision: ", True, TEAL), ("40-bit Q16.24 accumulators -> MAE = ", False, SLATE_DARK), ("0.000000", True, GREEN)],
            [("Status: ", True, TEAL), ("cfg_mode, execution_enable, cycle counters", False, SLATE_DARK)]
        ])
    ]
    for title_c, hcol, x_pos, lines_c in io_cards:
        add_card(s3, x_pos, 5.36, 3.93, 1.54, title_c, header_fill=hcol)
        tb = add_textbox(s3, x_pos + 0.08, 5.76, 3.77, 1.08)
        add_rich_paragraphs(tb.text_frame, lines_c, default_size=10.5, space_after=3)

    # =========================================================================
    # SLIDE 4: END-TO-END 7-PHASE EXECUTION PIPELINE (What & How)
    # =========================================================================
    s4 = prs.slides.add_slide(blank)
    add_header_footer(s4, "End-to-End Execution Pipeline: What Happens in Each Phase & How", "7-PHASE FLOW", 4,
        "Walking phase by phase from host command ingestion to completion telemetry: Phase 1 validates parameters, "
        "Phase 2 resolves PEs in 1 cycle, Phase 3 swaps ping-pong banks, Phase 4 performs synchronous zero-gating, "
        "Phase 5 accumulates in 40-bit Q16.24, Phase 6 rounds and packs Q4.12, Phase 7 raises layer_done_pulse.")

    phases = [
        ("P1: Ingest", MAROON), ("P2: Policy", TEAL), ("P3: Buffer", BLUE),
        ("P4: Zero-Gate", MAROON), ("P5: Compute", SLATE_DARK), ("P6: Drain", AMBER), ("P7: Done", GREEN)
    ]
    px = 0.50
    for idx_p, (pname, pcol) in enumerate(phases):
        box = add_rect(s4, px, 0.90, 1.62, 0.44, fill=pcol, rounded=True)
        add_textbox(s4, px + 0.02, 0.92, 1.58, 0.40, pname, font_size=11, bold=True, color=WHITE,
                    align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
        if idx_p < 6:
            add_textbox(s4, px + 1.62, 0.92, 0.17, 0.40, "→", font_size=12, bold=True, color=SLATE_MUTED,
                        align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE, margin_l=0.0, margin_r=0.0)
        px += 1.79

    tbl_shape4 = s4.shapes.add_table(8, 5, Inches(0.50), Inches(1.48), Inches(12.333), Inches(5.40))
    t4 = tbl_shape4.table
    col_w4 = [1.45, 2.25, 3.05, 4.25, 1.333]
    for ci, cw in enumerate(col_w4):
        t4.columns[ci].width = Inches(cw)

    headers4 = ["Phase / State", "Hardware Module", "WHAT It Does (Goal)", "HOW It Does It (RTL Signals & Logic)", "Timing"]
    for ci, htxt in enumerate(headers4):
        style_table_cell(t4.cell(0, ci), htxt, font_size=10.5, bold=True, color=WHITE, fill=NAVY)

    rows4 = [
        ("Phase 1\nST_VALIDATE", "layer_command_\nsequencer.sv", "Ingests descriptor; checks valid K > 0 & buffer IDs.",
         "64-bit packet checked on ready/valid; raises error_code on K=0 or mode 2'b11.", "2 cycles"),
        ("Phase 2\nCombinatorial", "tsk33_transparent_\npolicy_controller.sv", "Selects 16/32/64 PE mode; enforces safety interlock.",
         "Evaluates T(M)<=L_max and M<=P_max in 1 cycle; locks exec_enable=0 if P_max<16.", "1 cycle"),
        ("Phase 3\nST_CONFIGURE", "dma_controller & ping_\npong_buffer_controller", "Bursts DRAM tensors; swaps Buffer A / B roles safely.",
         "AXI4 master writes Port A; consumer_start toggles active bank without read-write collision.", "Overlapped"),
        ("Phase 4\nST_SPARSE_WAIT", "datapath_compute_\nfeeder & mac_unit_40b", "Eliminates zero-valued weight reads & MAC switching.",
         "Per-PE bypass_mac freezes MAC on act==0; feeder skips wt reads if all_acts_zero.", "Per step"),
        ("Phase 5\nST_WAIT_COMP", "pe_array_40b.sv\n(4x16 PEs)", "Runs multi-pass MACs into 40-bit overflow-safe sums.",
         "Quadrants clock-gated via col_active; P = 64/N_active passes into 40b Q16.24 regs.", "9.5k–38.2k\ncycles"),
        ("Phase 6\nST_DRAIN", "ofmap_drain_ctrl &\nrequantization_unit.sv", "Rounds, saturates & packs 40b sums into 16b Q4.12.",
         "Adds round_offset (2048), shifts >>>12, clamps [-32768,32767], packs 32b to Port A.", "128 words"),
        ("Phase 7\nST_COMPLETE", "layer_command_\nsequencer & Telemetry", "Notifies Host CPU & records execution telemetry.",
         "Asserts 1-cycle layer_done_pulse; latches cycles, skipped ops & SRAM bank conflicts.", "1 cycle")
    ]
    t4.rows[0].height = Inches(0.42)
    for ri, rdata in enumerate(rows4, start=1):
        t4.rows[ri].height = Inches(0.71)
        bg = WHITE if (ri % 2 == 1) else BG_LIGHT
        style_table_cell(t4.cell(ri, 0), rdata[0], font_size=10, bold=True, color=MAROON, fill=bg)
        style_table_cell(t4.cell(ri, 1), rdata[1], font_size=9.5, bold=False, color=BLUE, fill=bg, font_name=FONT_MONO)
        style_table_cell(t4.cell(ri, 2), rdata[2], font_size=10, bold=True, color=NAVY, fill=bg, align=PP_ALIGN.LEFT)
        style_table_cell(t4.cell(ri, 3), rdata[3], font_size=10, bold=False, color=SLATE_DARK, fill=bg, align=PP_ALIGN.LEFT)
        style_table_cell(t4.cell(ri, 4), rdata[4], font_size=10, bold=True, color=TEAL, fill=bg)

    # =========================================================================
    # SLIDE 5: HARDWARE POLICY ENGINE (L_max, P_max, Interlock)
    # =========================================================================
    s5 = prs.slides.add_slide(blank)
    add_header_footer(s5, "Hardware Policy Engine: L_max, P_max & Mode Selection", "POLICY ENGINE", 5,
        "L_max comes from host RTOS frame deadlines (cycles @ 100 MHz); P_max comes from PMIC/thermal caps. "
        "Policy A picks minimum PEs under L_max; Policy B picks maximum throughput under P_max; P_max < 16 locks off execution.")

    add_card(s5, 0.50, 0.95, 5.95, 2.25, "How L_max & P_max Constraints Originate", header_fill=MAROON)
    tb5 = add_textbox(s5, 0.65, 1.38, 5.65, 1.75)
    add_rich_paragraphs(tb5.text_frame, [
        [("1. Latency Budget (L_max): ", True, MAROON), ("Set by Host RTOS from camera frame SLA at 100 MHz (e.g., 40,000 cyc relaxed vs 15,000 cyc urgent).", False, SLATE_DARK)],
        [("2. PE Cap (P_max): ", True, MAROON), ("Set by SoC PMIC / thermal sensor (Tj < 70C: 64 PEs | 70-85C: 32 PEs | >85C: 16 PEs | Fault <16).", False, SLATE_DARK)],
        [("3. Policies (1-Cycle): ", True, MAROON), ("Policy A (pol_sel=0) minimizes PEs under L_max; Policy B (pol_sel=1) maximizes speed under P_max.", False, SLATE_DARK)]
    ], default_size=11, space_after=5)

    # Walkthrough table bottom-left
    tbl_s5 = s5.shapes.add_table(5, 4, Inches(0.50), Inches(3.38), Inches(5.95), Inches(3.45))
    t5 = tbl_s5.table
    for ci, cw in enumerate([1.45, 1.35, 1.25, 1.90]):
        t5.columns[ci].width = Inches(cw)
    t5.rows[0].height = Inches(0.45)
    for ci, htxt in enumerate(["Scenario", "Inputs (L, P)", "Selected", "Hardware Outcome"]):
        style_table_cell(t5.cell(0, ci), htxt, font_size=10, bold=True, color=WHITE, fill=NAVY)
    s5_rows = [
        ("1. Energy Save", "L=40k, P=64\nPolicy A", "16 PEs\n(2'b00)", "T=38,225<=40k;\n75% logic saved"),
        ("2. Urgent Frame", "L=15k, P=64\nPolicy A", "64 PEs\n(2'b10)", "T=9,569<=15k;\nPeak throughput"),
        ("3. Hot SoC Cap", "L=25k, P=32\nPolicy B", "32 PEs\n(2'b01)", "T=19,121<=25k;\n+5,879 cyc slack"),
        ("4. Safety Lock", "Any L, P=8\nAny Policy", "LOCKED\n(2'b11)", "invalid_pe_limit=1;\nexec_enable=0")
    ]
    for ri, rdata in enumerate(s5_rows, start=1):
        t5.rows[ri].height = Inches(0.75)
        bg = RED_SOFT if ri == 4 else (WHITE if ri % 2 == 1 else BG_LIGHT)
        col_r = RED_TEXT if ri == 4 else NAVY
        for ci, val in enumerate(rdata):
            style_table_cell(t5.cell(ri, ci), val, font_size=10, bold=(ci in (0, 2)), color=col_r, fill=bg)

    # Right Heatmap chart
    add_card(s5, 6.62, 0.95, 6.21, 5.88, "201-Point Verified Constraint Space Heatmap (Policy A)", header_fill=SLATE_DARK)
    add_image_fit(s5, os.path.join(REPO_ROOT, "NEURAL_ACC_PAPER", "plots", "fig13_policy_space_heatmap.png"), 6.72, 1.42, 6.01, 4.65)
    add_textbox(s5, 6.80, 6.20, 5.85, 0.50,
                "Verified across 201 boundary test points in tb_tsk37_policy_audit.sv (201/201 PASS).",
                font_size=10.5, bold=True, color=GREEN, align=PP_ALIGN.CENTER)

    # =========================================================================
    # SLIDE 6: WORKING EXAMPLE 1/3 — MATRIX INPUTS & DENSE BASELINE
    # =========================================================================
    s6 = prs.slides.add_slide(blank)
    add_header_footer(s6, "Complete Working Example (1/3): Matrix Inputs & Dense Baseline", "WORKING EXAMPLE", 6,
        "Taking a concrete 4x4 activation matrix A with 8 zeros (50% sparsity) and a 4x4 weight matrix W. "
        "Normal dense execution computes all 16 MACs to produce Y = [3, 4, 4, 5]^T.")

    A_mat = [[1, 0, 2, 0], [0, 3, 0, 1], [2, 0, 1, 0], [0, 1, 0, 2]]
    W_mat = [[1, 2, 1, 1], [2, 1, 2, 1], [1, 1, 2, 2], [2, 1, 1, 2]]

    add_card(s6, 0.50, 0.95, 4.10, 4.65, "Step 1: Activation Matrix A (4x4)", header_fill=MAROON)
    draw_matrix_grid(s6, 0.78, 1.60, 0.88, 0.68, A_mat, highlight_zeros=True,
                     sub_label="Red cells = 0  (Triggers Zero-Gating)")
    add_rect(s6, 0.68, 4.68, 3.74, 0.78, fill=MAROON_LIGHT, line=MAROON, line_pt=1.0, rounded=True)
    add_textbox(s6, 0.78, 4.74, 3.54, 0.66,
                "Total Elements = 4 x 4 = 16  |  Zeros = 8\n"
                "Activation Sparsity = 8 / 16 = 50%",
                font_size=12.5, bold=True, color=MAROON, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    add_card(s6, 4.82, 0.95, 3.70, 4.65, "Step 2: Weight Matrix W (4x4)", header_fill=SLATE_DARK)
    draw_matrix_grid(s6, 5.15, 1.60, 0.76, 0.68, W_mat, highlight_zeros=False)
    add_rect(s6, 5.00, 4.68, 3.34, 0.78, fill=BLUE_LIGHT, line=BLUE, line_pt=1.0, rounded=True)
    add_textbox(s6, 5.08, 4.74, 3.18, 0.66,
                "Row-Wise Dot Product Operation:\n"
                "Y[i] = Sum_{j=0..3} A[i][j] * W[i][j]",
                font_size=11.5, bold=True, color=BLUE, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    add_card(s6, 8.74, 0.95, 4.09, 4.65, "Step 3: Normal Dense Computation", header_fill=TEAL)
    tb6 = add_textbox(s6, 8.92, 1.48, 3.75, 2.75)
    add_rich_paragraphs(tb6.text_frame, [
        [("Row 0: ", True, MAROON), ("(1x1) + (0x2) + (2x1) + (0x1) = ", False, SLATE_DARK), ("3", True, NAVY)],
        [("Row 1: ", True, MAROON), ("(0x2) + (3x1) + (0x2) + (1x1) = ", False, SLATE_DARK), ("4", True, NAVY)],
        [("Row 2: ", True, MAROON), ("(2x1) + (0x1) + (1x2) + (0x2) = ", False, SLATE_DARK), ("4", True, NAVY)],
        [("Row 3: ", True, MAROON), ("(0x2) + (1x1) + (0x1) + (2x2) = ", False, SLATE_DARK), ("5", True, NAVY)],
    ], default_size=12, space_after=12)
    add_rect(s6, 8.94, 4.30, 3.70, 1.15, fill=GREEN_LIGHT, line=GREEN, line_pt=1.2, rounded=True)
    add_textbox(s6, 9.00, 4.38, 3.58, 0.98,
                "Dense Output Y = [ 3,  4,  4,  5 ]^T\n"
                "Dense Total Multiplications = 16 MACs",
                font_size=12, bold=True, color=GREEN, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    # Bottom takeaway strip
    add_rect(s6, 0.50, 5.82, 12.333, 1.00, fill=WHITE, line=MAROON, line_pt=1.5, rounded=True)
    add_textbox(s6, 0.70, 5.90, 11.933, 0.84,
                "Observation: Half of all dense MAC terms (8 out of 16) compute 0 x W = 0, adding zero numerical contribution "
                "while wasting dynamic multiplier switching and accumulator register power.",
                font_size=13, bold=True, color=NAVY, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    # =========================================================================
    # SLIDE 7: WORKING EXAMPLE 2/3 — SYNCHRONOUS ZERO-GATING
    # =========================================================================
    s7 = prs.slides.add_slide(blank)
    add_header_footer(s7, "Working Example (2/3): Synchronous Zero-Gating (50% MAC Cut)", "ZERO-GATING", 7,
        "In our 50%-sparse matrix example, zero-gating skips 8 of 16 multiplications cleanly. "
        "At RTL level, mac_unit_40b asserts bypass_mac for each zero element while feeder maintains deterministic cycle timing.")

    # Left comparison table for Row 0 and overall matrix
    add_card(s7, 0.50, 0.95, 6.20, 4.55, "Step 4 & 5: Row-by-Row Zero-Gating Walkthrough", header_fill=MAROON)
    tbl_s7 = s7.shapes.add_table(5, 4, Inches(0.70), Inches(1.48), Inches(5.80), Inches(2.55))
    t7 = tbl_s7.table
    for ci, cw in enumerate([1.25, 1.15, 1.45, 1.95]):
        t7.columns[ci].width = Inches(cw)
    t7.rows[0].height = Inches(0.45)
    for ci, htxt in enumerate(["Row 0 Act", "Weight", "RTL bypass_mac", "HW Action"]):
        style_table_cell(t7.cell(0, ci), htxt, font_size=10.5, bold=True, color=WHITE, fill=NAVY)
    s7_rows = [
        ("A[0,0] = 1", "W[0,0] = 1", "0 (Active)", "Compute: 1 x 1 = 1"),
        ("A[0,1] = 0", "W[0,1] = 2", "1 (Zero Gate)", "SKIP MAC (Hold Acc)"),
        ("A[0,2] = 2", "W[0,2] = 1", "0 (Active)", "Compute: 2 x 1 = 2"),
        ("A[0,3] = 0", "W[0,3] = 1", "1 (Zero Gate)", "SKIP MAC (Hold Acc)")
    ]
    for ri, rdata in enumerate(s7_rows, start=1):
        t7.rows[ri].height = Inches(0.52)
        is_skip = "SKIP" in rdata[3]
        bg = RED_SOFT if is_skip else GREEN_LIGHT
        fg = RED_TEXT if is_skip else GREEN
        for ci, val in enumerate(rdata):
            style_table_cell(t7.cell(ri, ci), val, font_size=10.5, bold=(ci >= 2 or is_skip),
                             color=fg if ci >= 2 else NAVY, fill=bg)

    add_rect(s7, 0.70, 4.22, 5.80, 1.10, fill=BLUE_LIGHT, line=BLUE, line_pt=1.2, rounded=True)
    add_textbox(s7, 0.85, 4.30, 5.50, 0.94,
                "Full Matrix Result:  Dense = 16 MACs   |   Skipped = 8 MACs   |   Useful = 8 MACs\n"
                "MAC Reduction = (16 - 8) / 16 x 100%  =  50% Savings (Exact Output Y Unchanged!)",
                font_size=12, bold=True, color=BLUE, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    # Right Hardware Mechanism card + Why Zero-Gating Matters
    add_card(s7, 6.95, 0.95, 5.88, 4.55, "Step 6 & 15: Synchronous Zero-Gating Mechanism in RTL", header_fill=SLATE_DARK)
    tb7 = add_textbox(s7, 7.15, 1.48, 5.48, 3.85)
    add_rich_paragraphs(tb7.text_frame, [
        [("1. Per-PE Zero Bypass (", True, MAROON), ("mac_unit_40b.sv", True, BLUE, FONT_MONO), ("):", True, MAROON)],
        [("   * bypass_mac = (!act_mask) || (act_data == 0)", False, NAVY, FONT_MONO, 10.5)],
        [("   * Forces multiplier product to 0 & freezes 40-bit accumulator register clock-enable (no wasteful toggling).", False, SLATE_DARK)],
        [("2. All-Zero Row-Group Weight Skip (", True, TEAL), ("datapath_compute_feeder.sv", True, BLUE, FONT_MONO), ("):", True, TEAL)],
        [("   * Evaluates all_acts_zero across 4 parallel PE rows in ST_SPARSE_WAIT_A; suppresses weight SRAM reads when whole chunk is zero.", False, SLATE_DARK)],
        [("3. Strict Timing Determinism:", True, GREEN)],
        [("   * Unlike async zero-skippers, pipeline slot counters step uniformly — eliminating timing jitter.", False, SLATE_DARK)]
    ], default_size=11.5, space_after=6)

    # Bottom contrast bar
    add_rect(s7, 0.50, 5.72, 12.333, 1.10, fill=MAROON_LIGHT, line=MAROON, line_pt=1.5, rounded=True)
    add_textbox(s7, 0.70, 5.80, 11.933, 0.94,
                "Key Takeaway: Without Zero-Gating -> wasteful switching on A = 0  |  "
                "With SparseFlex -> Multiplier & Accumulator activity disabled on A = 0 while preserving Y = [3, 4, 4, 5]^T with 0.00% jitter.",
                font_size=12.5, bold=True, color=MAROON, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    # =========================================================================
    # SLIDE 8: WORKING EXAMPLE 3/3 — 64/32/16 PE SCALING & MULTI-PASS TILING
    # =========================================================================
    s8 = prs.slides.add_slide(blank)
    add_header_footer(s8, "Working Example (3/3): PE Scaling & Multi-Pass Channel Tiling", "TILING & TRADE-OFF", 8,
        "SparseFlex supports 64, 32, and 16 active PEs using clock-gated columns. Because physically 64 channels exist, "
        "scaling down requires P = 64 / N_active passes (1, 2, or 4), trading active logic (saving 50%/75%) for activation SRAM reads (+100%/+300%).")

    modes8 = [
        ("Full Array: 64 PEs (cfg_mode = 2'b10)", SLATE_DARK, 0.50,
         "col_active = 16'hFFFF  (All 16 cols x 4 rows ON)",
         "Passes: P = 64 / 64 = 1 Pass",
         "Channels 0 - 63 computed simultaneously\n\n* Active PE Logic: 100% (0% reduced)\n* Latency: 9,569 cycles (Fastest)\n* Act SRAM Reads: 9,216 (1x baseline)"),
        ("Medium: 32 PEs (cfg_mode = 2'b01)", BLUE, 4.70,
         "col_active = 16'h00FF  (Cols 0..7 ON; 8..15 Gated)",
         "Passes: P = 64 / 32 = 2 Passes",
         "Pass 1 -> Ch 0-31   |   Pass 2 -> Ch 32-63\nY = Y_pass1 U Y_pass2 (128 packed words)\n* Active PE Logic Saved: 50%\n* Act SRAM Reads: +100% (18,432 reads)"),
        ("Low-Power: 16 PEs (cfg_mode = 2'b00)", MAROON, 8.90,
         "col_active = 16'h000F  (Cols 0..3 ON; 4..15 Gated)",
         "Passes: P = 64 / 16 = 4 Passes",
         "Pass 1 -> Ch 0-15  |  Pass 2 -> Ch 16-31\nPass 3 -> Ch 32-47 | Pass 4 -> Ch 48-63\n* Active PE Logic Saved: 75%\n* Act SRAM Reads: +300% (36,864 reads)")
    ]
    for m_title, m_col, x_pos, mask_txt, pass_txt, body_txt in modes8:
        add_card(s8, x_pos, 0.95, 3.93, 4.25, m_title, header_fill=m_col)
        add_textbox(s8, x_pos + 0.10, 1.40, 3.73, 0.34, mask_txt, font_size=9, bold=True, color=m_col, font_name=FONT_MONO, valign=MSO_ANCHOR.MIDDLE)
        # Quadrant visual strip (4 quadrants Q0..Q3)
        q_cnt = 4 if "64" in m_title else (2 if "32" in m_title else 1)
        for qi in range(4):
            q_on = (qi < q_cnt)
            qf = m_col if q_on else BORDER_GRAY
            qt = WHITE if q_on else SLATE_MUTED
            qb = add_rect(s8, x_pos + 0.14 + qi * 0.92, 1.82, 0.84, 0.56, fill=qf, rounded=True)
            add_textbox(s8, x_pos + 0.14 + qi * 0.92, 1.84, 0.84, 0.52, f"Q{qi}\n{'ON' if q_on else 'OFF'}",
                        font_size=10, bold=True, color=qt, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
        add_rect(s8, x_pos + 0.12, 2.52, 3.69, 0.42, fill=AMBER_LIGHT, line=AMBER, line_pt=1.0, rounded=True)
        add_textbox(s8, x_pos + 0.16, 2.55, 3.61, 0.36, pass_txt, font_size=12, bold=True, color=AMBER,
                    align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
        add_textbox(s8, x_pos + 0.14, 3.04, 3.65, 2.05, body_txt, font_size=11, color=SLATE_DARK)

    # Bottom trade-off box (Step 17)
    add_rect(s8, 0.50, 5.42, 12.333, 1.42, fill=MAROON_LIGHT, line=MAROON, line_pt=1.5, rounded=True)
    add_textbox(s8, 0.72, 5.50, 11.90, 1.26,
                "Fundamental Trade-Off Exposed (channel_tile_controller.sv):\n"
                "Throttling active PEs cuts active compute logic by 50% (32-PE) or 75% (16-PE), "
                "but forces P = 64/N_active passes — inflating activation SRAM reads by +100% and +300% respectively.",
                font_size=12.5, bold=True, color=MAROON, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    # =========================================================================
    # SLIDE 9: Q4.12 ARITHMETIC, 40-BIT ACCUMULATOR & PING-PONG SRAM
    # =========================================================================
    s9 = prs.slides.add_slide(blank)
    add_header_footer(s9, "Datapath Precision (Q4.12 / 40b MAC) & Ping-Pong SRAM", "DATAPATH & SRAM", 9,
        "Inputs use 16-bit Q4.12 (1.5 -> 6144). Multiplications form 32-bit Q8.24 products summed into 40-bit Q16.24 "
        "accumulators with 8 guard bits above the product. Dual-port ping-pong SRAM overlaps DMA writes and PE reads.")

    # Top Left: Fixed-Point & Accumulation Flow (Steps 13 & 14)
    add_card(s9, 0.50, 0.95, 7.15, 4.35, "Q4.12 -> Q8.24 -> 40-bit Q16.24 -> Requantization Datapath", header_fill=MAROON)
    # 4 stacked stage strips
    stages9 = [
        ("1. Input Q4.12 (16-bit)", BLUE_LIGHT, BLUE,
         "1 Sign [15] | 3 Int [14:12] | 12 Frac [11:0] -> Range [-8.0, +7.999755]\n"
         "Example: 1.5 * 2^12 = 6144 (16'h1800)  |  Row 0 input 1.0 -> 4096 (16'h1000)"),
        ("2. Multiplier Q8.24 (32-bit)", GREEN_LIGHT, GREEN,
         "Signed 16b x 16b -> 32-bit Product  (Frac bits = 12 + 12 = 24)\n"
         "Example: (1.0 * 1.0) + (2.0 * 1.0) = 3.0 -> Sum in Q8.24 = 50,331,648"),
        ("3. 40-Bit Accumulator Q16.24 (mac_unit_40b.sv)", MAROON_LIGHT, MAROON,
         "8 Guard Bits [39:32] above 32-bit product -> 2^8 = 256 full additions headroom\n"
         "Row 0 Accumulated Register = 40'h00_0300_0000  (Zero overflow guaranteed!)"),
        ("4. Drain Requantization -> 16b Q4.12 (requantization_unit.sv)", AMBER_LIGHT, AMBER,
         "Add round_offset 2048 -> Shift >>>12 -> clamp [-32768, 32767]\n"
         "Row 0 Out = 12,288 (16'h3000) == 3.000  |  Pack 2x16b -> 32b Port A write")
    ]
    sy = 1.42
    for st_title, st_bg, st_col, st_txt in stages9:
        add_rect(s9, 0.68, sy, 6.79, 0.88, fill=st_bg, line=st_col, line_pt=1.0, rounded=True)
        add_textbox(s9, 0.80, sy + 0.04, 6.55, 0.26, st_title, font_size=10.5, bold=True, color=st_col)
        add_textbox(s9, 0.80, sy + 0.30, 6.55, 0.52, st_txt, font_size=9.3, color=NAVY, font_name=FONT_MONO)
        sy += 0.96

    # Top Right: Ping-Pong SRAM Overlap (Step 12)
    add_card(s9, 7.85, 0.95, 4.98, 4.35, "41,472B 8-Bank Ping-Pong SRAM (Step 12)", header_fill=TEAL)
    add_textbox(s9, 8.02, 1.40, 4.64, 0.68,
                "8 interleaved dual-port banks (5,184 bytes/bank)\n"
                "partitioned into logical Buffer A and Buffer B:",
                font_size=11, bold=True, color=NAVY)
    pp_rows = [
        ("Cycle / Layer 1", "Buffer A -> PE Reads (Port B)", "Buffer B <- DMA Writes (Port A)", BLUE_LIGHT, MAROON_LIGHT),
        ("Cycle / Layer 2", "Buffer B -> PE Reads (Port B)", "Buffer A <- DMA Writes (Port A)", MAROON_LIGHT, BLUE_LIGHT),
        ("Cycle / Layer 3", "Buffer A -> PE Reads (Port B)", "Buffer B <- DMA Writes (Port A)", BLUE_LIGHT, MAROON_LIGHT),
    ]
    py9 = 2.18
    for lbl, r_txt, w_txt, c_l, c_r in pp_rows:
        add_textbox(s9, 8.02, py9, 4.64, 0.26, lbl, font_size=10, bold=True, color=SLATE_MUTED)
        add_rect(s9, 8.02, py9 + 0.25, 2.26, 0.52, fill=c_l, line=BLUE, line_pt=0.8, rounded=True)
        add_textbox(s9, 8.05, py9 + 0.27, 2.20, 0.48, r_txt, font_size=9.5, bold=True, color=NAVY, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
        add_rect(s9, 10.40, py9 + 0.25, 2.26, 0.52, fill=c_r, line=MAROON, line_pt=0.8, rounded=True)
        add_textbox(s9, 10.43, py9 + 0.27, 2.20, 0.48, w_txt, font_size=9.5, bold=True, color=MAROON, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
        py9 += 0.90
    add_textbox(s9, 8.02, 4.88, 4.64, 0.35, "Zero read-after-write contention | 100% Port B streaming.",
                font_size=10.5, bold=True, color=TEAL, align=PP_ALIGN.CENTER)

    # Bottom MAE=0 banner
    add_rect(s9, 0.50, 5.52, 12.333, 1.30, fill=GREEN_LIGHT, line=GREEN, line_pt=1.5, rounded=True)
    add_textbox(s9, 0.70, 5.62, 11.933, 1.10,
                "Verified Across 4 Real CNN Layers (ResNet-18 & VGG-16-BN, 1,024 Outputs, 589,824 MACs in TSK-37):\n"
                "Bit-Exact Numerical Equivalence vs. 64-Bit Python Golden Model:  MAE = 0.000000  |  RMSE = 0.000000  |  0 Saturation Errors",
                font_size=13, bold=True, color=GREEN, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    # =========================================================================
    # SLIDE 10: QUANTITATIVE RESULTS (1) — DETERMINISM & SPARSITY TELEMETRY
    # =========================================================================
    s10 = prs.slides.add_slide(blank)
    add_header_footer(s10, "Experimental Results (1): Sparsity Savings & 0.00% Jitter", "RESULTS: DETERMINISM", 10,
        "Measured across WL1 to WL4 from TSK33_MEASUREMENT_RESULTS.csv: total execution cycles remain 100% invariant "
        "(9,569 / 19,121 / 38,225) between dense and sparse runs, while compute cycles and weight SRAM reads drop 48.11% to 84.92%.")

    add_card(s10, 0.50, 0.95, 5.75, 5.88, "Cycle Determinism Across All PE Modes (fig06)", header_fill=SLATE_DARK)
    add_image_fit(s10, os.path.join(REPO_ROOT, "NEURAL_ACC_PAPER", "plots", "fig06_total_cycles_pe_modes.png"), 0.62, 1.42, 5.51, 4.30)
    add_rect(s10, 0.68, 5.86, 5.39, 0.82, fill=GREEN_LIGHT, line=GREEN, line_pt=1.0, rounded=True)
    add_textbox(s10, 0.78, 5.92, 5.19, 0.70,
                "0.00% Latency Jitter Proven: Dense == Sparse Cycles\n"
                "64-PE: 9,569 cyc  |  32-PE: 19,121 cyc  |  16-PE: 38,225 cyc",
                font_size=11.5, bold=True, color=GREEN, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    add_card(s10, 6.45, 0.95, 6.38, 5.88, "Measured RTL Telemetry (64-PE Mode, TSK33 CSV)", header_fill=MAROON)
    tbl_s10 = s10.shapes.add_table(5, 5, Inches(6.62), Inches(1.48), Inches(6.04), Inches(2.90))
    t10 = tbl_s10.table
    for ci, cw in enumerate([1.65, 1.05, 1.15, 1.15, 1.04]):
        t10.columns[ci].width = Inches(cw)
    t10.rows[0].height = Inches(0.48)
    for ci, htxt in enumerate(["Workload\n(Model)", "Total Cyc\n(Dense/Sp)", "Compute Cyc\n(9,216->Sp)", "Wt Reads\n(147,456->Sp)", "Switching\nSaved"]):
        style_table_cell(t10.cell(0, ci), htxt, font_size=9.5, bold=True, color=WHITE, fill=NAVY)
    s10_rows = [
        ("WL1: ResNet-18\nCIFAR-10 conv1", "9,569 /\n9,569", "2,867", "45,872", "-68.89%"),
        ("WL2: ResNet-18\nCIFAR-100 conv1", "9,569 /\n9,569", "3,081", "49,296", "-66.57%"),
        ("WL3: VGG-16-BN\nCIFAR-10 feat.3", "9,569 /\n9,569", "4,782", "76,512", "-48.11%"),
        ("WL4: ResNet-18\nCIFAR-10 conv2", "9,569 /\n9,569", "1,390", "22,240", "-84.92%")
    ]
    for ri, rdata in enumerate(s10_rows, start=1):
        t10.rows[ri].height = Inches(0.60)
        bg = WHITE if ri % 2 == 1 else BG_LIGHT
        for ci, val in enumerate(rdata):
            c_txt = GREEN if ci == 4 else NAVY
            style_table_cell(t10.cell(ri, ci), val, font_size=10, bold=(ci in (0, 4)),
                             color=c_txt, fill=bg, align=PP_ALIGN.LEFT if ci == 0 else PP_ALIGN.CENTER)

    add_rect(s10, 6.62, 4.60, 6.04, 2.02, fill=MAROON_LIGHT, line=MAROON, line_pt=1.0, rounded=True)
    tb10 = add_textbox(s10, 6.76, 4.68, 5.76, 1.86)
    add_rich_paragraphs(tb10.text_frame, [
        [("Key Experimental Proof:", True, MAROON)],
        [("* Weight SRAM reads drop from ", False, SLATE_DARK), ("147,456", True, NAVY), (" to ", False, SLATE_DARK), ("22,240", True, GREEN), (" (-84.92% in WL4).", False, SLATE_DARK)],
        [("* Active MAC compute cycles drop in exact 1:1 ratio with layer sparsity.", False, SLATE_DARK)],
        [("* Zero output mismatches (0/1,024) verified across all 28 configurations.", False, SLATE_DARK)]
    ], default_size=11.5, space_after=5)

    # =========================================================================
    # SLIDE 11: QUANTITATIVE RESULTS (2) — MULTI-PASS MEMORY AMPLIFICATION
    # =========================================================================
    s11 = prs.slides.add_slide(blank)
    add_header_footer(s11, "Experimental Results (2): Multi-Pass Memory Amplification Trade-Off", "RESULTS: MEMORY TAX", 11,
        "Scaling PEs down saves 50% (32-PE) or 75% (16-PE) active compute logic, but forces 2 or 4 passes, multiplying "
        "activation SRAM reads by +100% (18,432) and +300% (36,864). Naive linear energy savings assumptions do not hold.")

    add_card(s11, 0.50, 0.95, 6.65, 5.88, "Active Logic Reduction vs. On-Chip SRAM Read Amplification", header_fill=MAROON)
    add_image_fit(s11, os.path.join(REPO_ROOT, "poster_results_chart.png"), 0.62, 1.42, 6.41, 4.45)
    add_textbox(s11, 0.72, 5.95, 6.20, 0.75,
                "WL1 Chunk-Grouped Traffic: 12,339 (64-PE) -> 21,555 (+74.7%) -> 39,987 (+224.1%).\n"
                "Word-level Act SRAM Reads scale strictly 1x -> 2x (+100%) -> 4x (+300%).",
                font_size=10.5, bold=True, color=SLATE_DARK, align=PP_ALIGN.CENTER)

    add_card(s11, 7.35, 0.95, 5.48, 5.88, "Measured Activation SRAM Tax & Takeaway", header_fill=SLATE_DARK)
    tbl_s11 = s11.shapes.add_table(4, 4, Inches(7.52), Inches(1.48), Inches(5.14), Inches(2.15))
    t11 = tbl_s11.table
    for ci, cw in enumerate([1.05, 1.25, 1.32, 1.52]):
        t11.columns[ci].width = Inches(cw)
    t11.rows[0].height = Inches(0.45)
    for ci, htxt in enumerate(["Mode", "Logic Saved", "Act Reads", "Traffic Tax"]):
        style_table_cell(t11.cell(0, ci), htxt, font_size=10, bold=True, color=WHITE, fill=NAVY)
    for ri, rdata in enumerate([
        ("64-PE\n(P=1)", "0.0%", "9,216", "Baseline"),
        ("32-PE\n(P=2)", "50.0%", "18,432", "+100.0%\nAct Reads"),
        ("16-PE\n(P=4)", "75.0%", "36,864", "+300.0%\nAct Reads")
    ], start=1):
        t11.rows[ri].height = Inches(0.56)
        bg = WHITE if ri % 2 == 1 else BG_LIGHT
        for ci, val in enumerate(rdata):
            style_table_cell(t11.cell(ri, ci), val, font_size=10, bold=(ci in (0, 1, 3)),
                             color=RED_TEXT if (ri > 1 and ci == 3) else (GREEN if (ri > 1 and ci == 1) else NAVY), fill=bg)

    add_rect(s11, 7.52, 3.85, 5.14, 2.75, fill=AMBER_LIGHT, line=AMBER, line_pt=1.2, rounded=True)
    tb11 = add_textbox(s11, 7.66, 3.95, 4.86, 2.55)
    add_rich_paragraphs(tb11.text_frame, [
        [("Architectural Discovery (What I Am Most Proud Of):", True, AMBER)],
        [("1. Prior claims of \"proportional energy savings\" from PE throttling ignore off-array SRAM re-fetching.", False, SLATE_DARK)],
        [("2. In 16-PE mode, computing 4 sequential channel passes re-reads the entire activation map 4 times.", False, SLATE_DARK)],
        [("3. SparseFlex's honest hardware telemetry enables intelligent co-optimization of peak power vs. memory bandwidth.", False, SLATE_DARK)]
    ], default_size=11, space_after=6)

    # =========================================================================
    # SLIDE 12: LITERATURE COMPARISON MATRIX (Mandatory E)
    # =========================================================================
    s12 = prs.slides.add_slide(blank)
    add_header_footer(s12, "Comparative Positioning vs. Existing CNN Accelerators", "RELATED WORK", 12,
        "Audited across 18 foundational papers (ISCA, ASPLOS, JSSC, TCAD). SparseFlex matches Eyeriss determinism "
        "while avoiding asynchronous jitter of SCNN and NullHop, and uniquely adds single-cycle policy arbitration and fail-safe interlocks.")

    tbl_s12 = s12.shapes.add_table(9, 7, Inches(0.50), Inches(0.95), Inches(12.333), Inches(4.75))
    t12 = tbl_s12.table
    for ci, cw in enumerate([2.55, 1.50, 1.50, 1.50, 1.50, 1.65, 2.133]):
        t12.columns[ci].width = Inches(cw)
    t12.rows[0].height = Inches(0.52)
    h12 = ["Architecture Feature", "DianNao\n(ASPLOS'14)", "Eyeriss\n(JSSC'17)", "SCNN\n(ISCA'17)",
           "NullHop\n(TNNLS'19)", "Eyeriss v2\n(JETCAS'19)", "SparseFlex\n(Ours)"]
    for ci, htxt in enumerate(h12):
        style_table_cell(t12.cell(0, ci), htxt, font_size=10.5, bold=True, color=WHITE,
                         fill=MAROON if ci == 6 else NAVY)
    rows12 = [
        ("Sparsity Exploited", "None (Dense)", "Activations", "Wt & Act", "Activations", "Wt & Act", "Activations"),
        ("Zero-Handling Engine", "Full MAC", "Clock Gate", "Async Crossbar", "Sparsity Map", "Dyn. Router", "Sync Zero-Gate"),
        ("Timing Determinism", "Yes (Fixed)", "Yes (Fixed)", "No (Jitter)", "No (Jitter)", "Mixed", "Yes (0.00% Jitter)"),
        ("Configurable Array", "Fixed 64", "Fixed 168", "Fixed", "Fixed 128", "Flex NoC", "16 / 32 / 64 PEs"),
        ("Active Logic Saved", "0%", "0%", "0%", "0%", "Undefined", "50% / 75%"),
        ("Memory Penalty Audited", "No", "No", "No", "No", "No", "Yes (+100%/+300%)"),
        ("Resource Policy Engine", "Static", "SW Driver", "HW Queue", "Async Logic", "SW Runtime", "1-Cycle HW LUT"),
        ("Fail-Safe Interlock", "None", "None", "None", "None", "SW Check", "HW Lock (P_max<16)")
    ]
    for ri, rdata in enumerate(rows12, start=1):
        t12.rows[ri].height = Inches(0.525)
        bg_row = WHITE if ri % 2 == 1 else BG_LIGHT
        for ci, val in enumerate(rdata):
            bg = MAROON_LIGHT if ci == 6 else bg_row
            if "No (Jitter)" in val:
                fc = RED_TEXT
            elif ci == 6:
                fc = MAROON
            elif ci == 0:
                fc = NAVY
            else:
                fc = SLATE_DARK
            style_table_cell(t12.cell(ri, ci), val, font_size=10, bold=(ci in (0, 6) or "No (" in val),
                             color=fc, fill=bg, align=PP_ALIGN.LEFT if ci == 0 else PP_ALIGN.CENTER)

    add_rect(s12, 0.50, 5.88, 12.333, 0.96, fill=WHITE, line=MAROON, line_pt=1.5, rounded=True)
    add_textbox(s12, 0.70, 5.95, 11.933, 0.82,
                "Positioning Summary (18 Papers Surveyed): SparseFlex adopts fixed-point systolic reuse like DianNao & Eyeriss, "
                "eliminates async jitter of SCNN & NullHop, and introduces single-cycle policy arbitration + empirical memory-tax accounting.",
                font_size=12, bold=True, color=NAVY, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    # =========================================================================
    # SLIDE 13: DATASETS, METHODOLOGY & EFFORT DISTRIBUTION (Mandatory F & G)
    # =========================================================================
    s13 = prs.slides.add_slide(blank)
    add_header_footer(s13, "Datasets, Methodology, Engineering Effort & Challenges Overcome", "METHOD & EFFORT", 13,
        "Standard CIFAR-10 & CIFAR-100 workloads from ResNet-18 and VGG-16-BN verified via Icarus Verilog v12.0 "
        "against a 64-bit golden reference. 35% effort went to core RTL, 20% to toolchains/tests, 15% to headroom/verification each.")

    # Left: Datasets & Methods
    add_card(s13, 0.50, 0.95, 5.65, 5.88, "Datasets, Evaluation Methods & Metrics", header_fill=NAVY)
    tb13_l = add_textbox(s13, 0.68, 1.42, 5.29, 5.25)
    add_rich_paragraphs(tb13_l.text_frame, [
        [("Standard Datasets & CNN Layers (4 Workloads):", True, MAROON)],
        [("  * WL1: ResNet-18 layer1.0.conv1 (CIFAR-10) — 68.89% sparsity", False, SLATE_DARK)],
        [("  * WL2: ResNet-18 layer1.0.conv1 (CIFAR-100) — 66.57% sparsity", False, SLATE_DARK)],
        [("  * WL3: VGG-16-BN features.3 (CIFAR-10) — 48.11% sparsity", False, SLATE_DARK)],
        [("  * WL4: ResNet-18 layer2.1.conv2 (CIFAR-10) — 84.92% sparsity", False, SLATE_DARK)],
        [("Verification & Audit Methodology:", True, TEAL)],
        [("  * Icarus Verilog v12.0 cycle-accurate SystemVerilog simulation.", False, SLATE_DARK)],
        [("  * Independent 64-bit Python integer reference (reproduce_numerical).", False, SLATE_DARK)],
        [("  * 201-point constraint sweep across L_max and P_max boundaries.", False, SLATE_DARK)],
        [("Honest Boundary Reporting:", True, AMBER)],
        [("  * Vivado power/FPGA mapping scripts authored; silicon energy NOT_RUN due to host Vivado license absence (xlicdiag audit).", False, SLATE_DARK)]
    ], default_size=11, space_after=5)

    # Right: Effort distribution visual bars + Critical struggles solved
    add_card(s13, 6.35, 0.95, 6.48, 5.88, "Realistic Time Allocation & Toughest Bugs Solved", header_fill=MAROON)
    effort_bars = [
        ("RTL Architecture & Pipeline", 0.35, "35%", MAROON),
        ("EDA Toolchains & Harnesses", 0.20, "20%", BLUE),
        ("Fixed-Point Guard-Bit Math", 0.15, "15%", TEAL),
        ("Domain Learning & Survey", 0.15, "15%", SLATE_DARK),
        ("Regression & Evidence Audits", 0.15, "15%", GREEN)
    ]
    ey = 1.48
    for e_lbl, e_pct, e_txt, e_col in effort_bars:
        add_textbox(s13, 6.55, ey, 2.55, 0.32, e_lbl, font_size=10.5, bold=True, color=NAVY, valign=MSO_ANCHOR.MIDDLE)
        add_rect(s13, 9.15, ey + 0.04, 2.80 * (e_pct / 0.38), 0.24, fill=e_col, rounded=True)
        add_textbox(s13, 9.20 + 2.80 * (e_pct / 0.38), ey, 0.65, 0.32, e_txt, font_size=11, bold=True, color=e_col, valign=MSO_ANCHOR.MIDDLE)
        ey += 0.44

    add_rect(s13, 6.55, 3.85, 6.08, 2.78, fill=BG_LIGHT, line=BORDER_GRAY, line_pt=1.0, rounded=True)
    tb13_r = add_textbox(s13, 6.70, 3.94, 5.78, 2.60)
    add_rich_paragraphs(tb13_r.text_frame, [
        [("Three Critical Engineering Struggles Overcome:", True, MAROON)],
        [("1. K=576 Accumulator Overflow -> ", True, NAVY), ("Sized 40-bit Q16.24 registers with 8 guard bits above 32b products, dropping MAE to 0.000000.", False, SLATE_DARK)],
        [("2. FSM Drain / Buffer Races -> ", True, NAVY), ("Enforced atomic barrier handshakes between k_progress_tracker, ping-pong buffer, and OFMAP drain.", False, SLATE_DARK)],
        [("3. Dense vs Sparse Timing Reconciliation -> ", True, NAVY), ("Audited 1,124 raw cycle trace rows in TSK-20 until monitor counters matched 100.0%.", False, SLATE_DARK)]
    ], default_size=11, space_after=6)

    # =========================================================================
    # SLIDE 14: PROOF OF RIGOR, VERIFICATION & LIVE DEMO (Mandatory H)
    # =========================================================================
    s14 = prs.slides.add_slide(blank)
    add_header_footer(s14, "Proof of Genuine Engineering Effort, Verification Rigor & Live Demo", "PROOF & DEMO", 14,
        "20 modular SystemVerilog suites executing 12,202 passing assertions (0 failures), plus live demonstration runner "
        "`python run_demo.py --all` running Icarus Verilog simulations in real time.")

    kpis = [
        ("20 / 20", "RTL Test Suites Passing\n(Exit Code 0)", MAROON),
        ("12,202 / 12,202", "Functional Assertions\n(0 Failures)", GREEN),
        ("201 / 201", "Policy Boundary Sweep\n& Safety Interlocks", BLUE),
        ("0.000000", "MAE & RMSE Error\nAcross 589,824 MACs", TEAL)
    ]
    kx = 0.50
    for k_big, k_sub, k_col in kpis:
        add_rect(s14, kx, 0.95, 2.93, 1.35, fill=WHITE, line=k_col, line_pt=1.8, rounded=True)
        add_rect(s14, kx, 0.95, 2.93, 0.08, fill=k_col)
        add_textbox(s14, kx + 0.08, 1.10, 2.77, 0.52, k_big, font_size=24, bold=True, color=k_col, align=PP_ALIGN.CENTER)
        add_textbox(s14, kx + 0.08, 1.68, 2.77, 0.52, k_sub, font_size=10.5, bold=True, color=SLATE_MUTED, align=PP_ALIGN.CENTER)
        kx += 3.133

    add_card(s14, 0.50, 2.52, 6.20, 4.30, "Why This Is Authentic Deep Engineering (Not Toy Code)", header_fill=SLATE_DARK)
    tb14_l = add_textbox(s14, 0.68, 2.98, 5.84, 3.70)
    add_rich_paragraphs(tb14_l.text_frame, [
        [("1. Multi-Module Synthesizable RTL: ", True, MAROON), ("20+ integrated SystemVerilog modules spanning AXI4 DMA, 8-bank hybrid SRAM, 64-PE array, drain & requantization.", False, SLATE_DARK)],
        [("2. Protected Baseline Governance: ", True, MAROON), ("5 core baseline RTL files held strictly at 0 diffs with SHA-256 verification.", False, SLATE_DARK)],
        [("3. Cycle-Exact Trace Auditing: ", True, MAROON), ("Reconciled 1,124 memory trace entries & SHA-256 checksums across all 4 workloads.", False, SLATE_DARK)],
        [("4. Real Pretrained CNN Weights: ", True, MAROON), ("Validated WL1–WL4 hex images against 64-bit Python integer golden models.", False, SLATE_DARK)]
    ], default_size=11.5, space_after=8)

    add_card(s14, 6.95, 2.52, 5.88, 4.30, "Live Verification Demo Runner (run_demo.py)", header_fill=MAROON)
    add_rect(s14, 7.15, 3.05, 5.48, 2.55, fill=NAVY, rounded=True)
    add_textbox(s14, 7.30, 3.16, 5.18, 2.34,
                "# Execute 100% Live Simulations (Zero Hardcoding):\n"
                "python run_demo.py --regression  # 20 SV Suites (12,202 checks)\n"
                "python run_demo.py --telemetry   # WL1-WL4 Live Trade-off Audit\n"
                "python run_demo.py --numerical   # MAE=0.0 Across 589,824 MACs\n"
                "python run_demo.py --policy      # 201-Point Interlock Audit\n"
                "python run_demo.py --sparse      # 10 Live Zero-Gate Scenarios\n"
                "python run_demo.py --all         # Full Sequential Defense Demo",
                font_size=10.5, bold=False, color=RGBColor(0x86, 0xEF, 0xAC), font_name=FONT_MONO, valign=MSO_ANCHOR.MIDDLE)
    add_textbox(s14, 7.15, 5.75, 5.48, 0.90,
                "Compiles IEEE 1800-2012 SystemVerilog via Icarus Verilog v12.0 & verifies all outputs live during defense.",
                font_size=11, bold=True, color=MAROON, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    # =========================================================================
    # SLIDE 15: CONCLUSION & FUTURE ROADMAP
    # =========================================================================
    s15 = prs.slides.add_slide(blank)
    set_slide_bg(s15, NAVY)
    add_rect(s15, 0, 0, 13.333, 0.10, fill=MAROON)

    add_textbox(s15, 0.75, 0.45, 9.0, 0.65, "Conclusion, Contributions & Future Work",
                font_size=30, bold=True, color=WHITE)

    # Core Formula Box
    add_rect(s15, 0.75, 1.30, 8.80, 0.85, fill=MAROON, line=GOLD, line_pt=1.5, rounded=True)
    add_textbox(s15, 0.88, 1.36, 8.54, 0.72,
                "SparseFlex = Zero-Gating + Configurable PEs (16/32/64) + Multi-Pass Tiling",
                font_size=14.5, bold=True, color=WHITE, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    # 2 Summary cards
    add_card(s15, 0.75, 2.45, 4.25, 3.85, "Key Contributions", header_fill=TEAL, body_fill=SLATE_DARK, border=SLATE_MUTED)
    tb15_l = add_textbox(s15, 0.92, 2.95, 3.90, 3.20)
    add_rich_paragraphs(tb15_l.text_frame, [
        [("1. Deterministic Sparsity: ", True, GOLD), ("Up to 84.92% switching & weight-read elimination with 0.00% latency jitter.", False, WHITE)],
        [("2. Memory Tax Proof: ", True, GOLD), ("Quantified +100% / +300% activation SRAM read scaling under multi-pass PE throttling.", False, WHITE)],
        [("3. Hardware Safety: ", True, GOLD), ("Single-cycle policy engine + fail-safe interlock if P_max < 16.", False, WHITE)],
        [("4. Verified RTL: ", True, GOLD), ("12,202/12,202 checks passed; MAE = 0.000000.", False, WHITE)]
    ], default_size=11.5, space_after=8)

    add_card(s15, 5.25, 2.45, 4.30, 3.85, "Future Roadmap & Venues", header_fill=BLUE, body_fill=SLATE_DARK, border=SLATE_MUTED)
    tb15_r = add_textbox(s15, 5.42, 2.95, 3.96, 3.20)
    add_rich_paragraphs(tb15_r.text_frame, [
        [("Target Publications:", True, RGBColor(0x93, 0xC5, 0xFD))],
        [("  * IEEE TCAD / IEEE ISCAS / ACM DAC.", False, WHITE)],
        [("Next Engineering Steps:", True, RGBColor(0x93, 0xC5, 0xFD))],
        [("  * TSMC 28nm standard-cell ASIC synthesis for sign-off power & silicon area.", False, WHITE)],
        [("  * DMA scatter-gather controller for full multi-layer ImageNet automation.", False, WHITE)],
        [("  * Dual weight-activation sparsity via CSC indexing.", False, WHITE)]
    ], default_size=11.5, space_after=6)

    # Right Thank You + QR Card
    add_rect(s15, 9.90, 1.30, 2.85, 5.00, fill=WHITE, rounded=True)
    add_image_fit(s15, os.path.join(REPO_ROOT, "github_repo_qr.png"), 10.15, 1.55, 2.35, 2.35)
    add_textbox(s15, 10.05, 4.10, 2.55, 1.95,
                "Thank You!\nQuestions & Discussion\n\nRaushan Kumar\nDept. of CSE, IIT Tirupati",
                font_size=13, bold=True, color=NAVY, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    add_rect(s15, 0.75, 6.78, 12.0, 0.02, fill=SLATE_MUTED)
    add_textbox(s15, 0.75, 6.88, 9.0, 0.35, "SparseFlex: Activation-Sparse CNN Accelerator  |  IIT Tirupati M.Tech Defense",
                font_size=10, color=RGBColor(0x94, 0xA3, 0xB8))
    add_textbox(s15, 11.2, 6.88, 1.55, 0.35, "Slide 15 / 15", font_size=10, bold=True, color=WHITE, align=PP_ALIGN.RIGHT)

    s15.notes_slide.notes_text_frame.text = (
        "Thank you respected committee members. In conclusion, SparseFlex combines synchronous zero-gating, "
        "configurable 16/32/64 PE scaling, and multi-pass channel tiling — achieving up to 84.92% switching elimination "
        "with zero cycle jitter and MAE = 0.000000. I welcome your questions."
    )

    prs.save(OUT_PPTX)
    print(f"[SUCCESS] Generated 15-slide PowerPoint deck: {OUT_PPTX}")


if __name__ == "__main__":
    build_deck()

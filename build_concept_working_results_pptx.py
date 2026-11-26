#!/usr/bin/env python3
"""
SparseFlex: Concept, Working & Verified Results Presentation (.pptx)
Builds a cohesive 14-slide 16:9 widescreen PowerPoint structured in 3 Acts:
  - Act 1: CONCEPT (Slides 2-4)
  - Act 2: WORKING (Slides 5-9)
  - Act 3: RESULTS — Sparsity + Beyond Sparsity (Slides 10-14)
"""

import os
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
OUT_PPTX = os.path.join(REPO_ROOT, "SparseFlex_Concept_Working_Results.pptx")

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
TEAL_LIGHT   = RGBColor(0xF0, 0xFD, 0xFA)
GOLD         = RGBColor(0xF5, 0x9E, 0x0B)

FONT_MAIN = "Segoe UI"
FONT_MONO = "Consolas"
TOTAL_SLIDES = 14


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


def add_header_footer(slide, title, act_name, act_color, slide_num, notes_text=""):
    """Clean top header with active Act indicator pills (Concept / Working / Results)."""
    set_slide_bg(slide, BG_LIGHT)
    add_rect(slide, 0, 0, 13.333, 0.08, fill=act_color)
    add_textbox(slide, 0.50, 0.16, 8.35, 0.50, title, font_size=18.5, bold=True,
                color=NAVY, valign=MSO_ANCHOR.MIDDLE)

    # 3 Act breadcrumb pills on top right: CONCEPT | WORKING | RESULTS
    acts = [("1. CONCEPT", MAROON), ("2. WORKING", BLUE), ("3. RESULTS", GREEN)]
    ax = 8.95
    for label, col in acts:
        is_active = (label.split(". ")[1] == act_name)
        bg = col if is_active else WHITE
        fg = WHITE if is_active else SLATE_MUTED
        bd = col if is_active else BORDER_GRAY
        p_shp = add_rect(slide, ax, 0.22, 1.24, 0.34, fill=bg, line=bd, line_pt=1.0, rounded=True)
        add_textbox(slide, ax, 0.22, 1.24, 0.34, label, font_size=8.8, bold=True, color=fg,
                    align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE, margin_l=0.0, margin_r=0.0)
        ax += 1.32

    add_rect(slide, 0.50, 0.72, 12.333, 0.018, fill=BORDER_GRAY)
    add_rect(slide, 0.50, 7.05, 12.333, 0.015, fill=BORDER_GRAY)
    add_textbox(slide, 0.50, 7.10, 8.80, 0.30,
                "SparseFlex  |  Concept, Working & Verified Results  |  Dept. of CSE, IIT Tirupati",
                font_size=9.5, color=SLATE_MUTED)
    add_textbox(slide, 11.30, 7.10, 1.533, 0.30,
                f"Slide {slide_num} / {TOTAL_SLIDES}",
                font_size=9.5, bold=True, color=act_color, align=PP_ALIGN.RIGHT)
    if notes_text:
        slide.notes_slide.notes_text_frame.text = notes_text


def add_card(slide, x, y, w, h, title="", header_fill=MAROON, body_fill=WHITE, border=BORDER_GRAY):
    card = add_rect(slide, x, y, w, h, fill=body_fill, line=border, line_pt=1.0, rounded=True)
    if title:
        add_rect(slide, x, y, w, 0.36, fill=header_fill, line=header_fill, line_pt=0.5)
        add_textbox(slide, x + 0.10, y + 0.03, w - 0.20, 0.30, title,
                    font_size=11.5, bold=True, color=WHITE, valign=MSO_ANCHOR.MIDDLE)
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


def draw_matrix_grid(slide, x, y, cell_w, cell_h, matrix, highlight_zeros=True, sub_label=""):
    rows, cols = len(matrix), len(matrix[0])
    tbl_shape = slide.shapes.add_table(rows, cols, Inches(x), Inches(y),
                                       Inches(cell_w * cols), Inches(cell_h * rows))
    tbl = tbl_shape.table
    for c in range(cols):
        tbl.columns[c].width = Inches(cell_w)
    for r in range(rows):
        tbl.rows[r].height = Inches(cell_h)
        for c in range(cols):
            val = matrix[r][c]
            if highlight_zeros and val == 0:
                bg, fg = RED_SOFT, RED_TEXT
            elif highlight_zeros:
                bg, fg = BLUE_LIGHT, BLUE
            else:
                bg, fg = (WHITE if r % 2 == 0 else BG_LIGHT), NAVY
            style_table_cell(tbl.cell(r, c), str(val), font_size=14, bold=True, color=fg, fill=bg, font_name=FONT_MONO)
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
    # SLIDE 1: TITLE & 3-ACT ROADMAP (CONCEPT -> WORKING -> RESULTS)
    # =========================================================================
    s1 = prs.slides.add_slide(blank)
    set_slide_bg(s1, NAVY)
    add_rect(s1, 0, 0, 0.24, 7.5, fill=MAROON)
    add_rect(s1, 0.24, 0, 13.093, 0.10, fill=MAROON)

    pill1 = add_rect(s1, 0.70, 0.55, 6.20, 0.38, fill=MAROON, rounded=True)
    add_textbox(s1, 0.70, 0.55, 6.20, 0.38, "M.TECH PRESENTATION  |  CONCEPT, WORKING & VERIFIED RESULTS",
                font_size=10.5, bold=True, color=WHITE, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    add_textbox(s1, 0.70, 1.15, 9.10, 1.25,
                "SparseFlex: An Activation-Sparse\nCNN Hardware Accelerator",
                font_size=36, bold=True, color=WHITE)
    add_textbox(s1, 0.70, 2.55, 9.10, 0.65,
                "Reconfigurable 16 / 32 / 64 Processing Elements · Synchronous Zero-Gating · Hardware Policy Interlocks",
                font_size=15, color=RGBColor(0xCB, 0xD5, 0xE1))

    # 3-Act Visual Roadmap Cards right on Title Slide
    acts_s1 = [
        ("1. CONCEPT (Slides 2–4)", MAROON,
         "Why SparseFlex?\n* Zero-gating without jitter\n* Configurable 16/32/64 PEs\n* Single-cycle L_max/P_max policy\n* Fail-safe lock (P_max < 16)"),
        ("2. WORKING (Slides 5–9)", BLUE,
         "How It Executes\n* 7-phase RTL state pipeline\n* Worked 4x4 matrix example\n* Multi-pass tiling (P=1, 2, 4)\n* Q4.12 / 40b / Ping-Pong SRAM"),
        ("3. RESULTS (Slides 10–14)", GREEN,
         "Sparsity + Beyond Sparsity\n* -84.92% wt reads (0% jitter)\n* 75% logic cut & 3.995x speedup\n* 0 bank conflicts / 0 stalls\n* MAE = 0.000000 | 12,202 checks")
    ]
    ax1 = 0.70
    for a_title, a_col, a_txt in acts_s1:
        add_rect(s1, ax1, 3.45, 2.92, 2.55, fill=SLATE_DARK, line=a_col, line_pt=1.5, rounded=True)
        add_rect(s1, ax1, 3.45, 2.92, 0.40, fill=a_col)
        add_textbox(s1, ax1 + 0.08, 3.47, 2.76, 0.36, a_title, font_size=11.5, bold=True, color=WHITE, valign=MSO_ANCHOR.MIDDLE)
        add_textbox(s1, ax1 + 0.12, 3.94, 2.68, 1.98, a_txt, font_size=11, color=RGBColor(0xE2, 0xE8, 0xF0))
        ax1 += 3.06

    # Right QR Card
    add_rect(s1, 10.15, 1.15, 2.55, 4.85, fill=WHITE, line=BORDER_GRAY, line_pt=1.0, rounded=True)
    add_image_fit(s1, os.path.join(REPO_ROOT, "github_repo_qr.png"), 10.35, 1.38, 2.15, 2.15)
    add_textbox(s1, 10.22, 3.72, 2.41, 2.10,
                "Scan for Source RTL\n& Live Testbenches\n\nRaushan Kumar\nDept. of CSE\nIIT Tirupati",
                font_size=12, bold=True, color=NAVY, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    add_rect(s1, 0.70, 6.75, 12.0, 0.02, fill=SLATE_MUTED)
    add_textbox(s1, 0.70, 6.85, 8.8, 0.35,
                "SparseFlex Defense Deck: Concept, Working & Results  |  2026",
                font_size=10, color=RGBColor(0x94, 0xA3, 0xB8))
    add_textbox(s1, 11.2, 6.85, 1.5, 0.35, "Slide 1 / 14", font_size=10, bold=True, color=WHITE, align=PP_ALIGN.RIGHT)
    s1.notes_slide.notes_text_frame.text = (
        "This presentation walks through SparseFlex in three clear parts: First the Concept, second the internal Working "
        "using a concrete matrix walkthrough, and third all verified Results—covering both sparsity savings and non-sparsity wins."
    )

    # =========================================================================
    # ACT 1 - SLIDE 2: CONCEPT (PROBLEM & CORE DUAL IDEA)
    # =========================================================================
    s2 = prs.slides.add_slide(blank)
    add_header_footer(s2, "Core Concept: Two Axes of Deterministic Hardware Flexibility", "CONCEPT", MAROON, 2,
        "SparseFlex solves two edge AI challenges: eliminating dynamic power wasted on post-ReLU zero activations without introducing timing jitter, "
        "and dynamically reconfiguring active PEs under real-time latency and thermal caps.")

    cards2 = [
        ("The Problem: Wasted Power + Unpredictable Jitter", MAROON,
         "Post-ReLU CNNs contain 48%–85% zero activations. Naive accelerators compute 0 x W anyway; prior sparse engines (SCNN, NullHop) skip asymmetrically via FIFOs, causing severe timing jitter unsuitable for hard real-time edge deadlines."),
        ("Concept Pillar 1: Synchronous Zero-Gating", TEAL,
         "Inspects incoming activations inline inside the datapath (mac_unit_40b) and feeder. Suppresses weight SRAM reads and freezes multiplier clock enables on zeros while stepping pipeline counters deterministically (0.00% jitter)."),
        ("Concept Pillar 2: Dynamic 16 / 32 / 64 PE Scaling", BLUE,
         "Partitions a 4x16 grid (64 PEs) into clock-gated quadrants. A single-cycle policy controller picks 16, 32, or 64 PEs from runtime limits (L_max, P_max), using multi-pass tiling so every output channel is preserved.")
    ]
    cy = 0.96
    for c_t, c_col, c_b in cards2:
        add_card(s2, 0.50, cy, 6.15, 1.88, c_t, header_fill=c_col)
        add_textbox(s2, 0.66, cy + 0.44, 5.83, 1.36, c_b, font_size=11.5, color=SLATE_DARK, valign=MSO_ANCHOR.MIDDLE)
        cy += 2.00

    add_card(s2, 6.85, 0.96, 5.98, 5.88, "Activation Sparsity Across Canonical CNNs", header_fill=SLATE_DARK)
    add_image_fit(s2, os.path.join(REPO_ROOT, "poster_sparsity_chart.png"), 6.98, 1.44, 5.72, 4.15)
    add_rect(s2, 7.05, 5.74, 5.58, 0.94, fill=MAROON_LIGHT, line=MAROON, line_pt=1.0, rounded=True)
    add_textbox(s2, 7.18, 5.82, 5.32, 0.78,
                "Core Equation:\nSparseFlex = Synchronous Zero-Gating + Configurable PEs + Multi-Pass Tiling",
                font_size=12, bold=True, color=MAROON, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    # =========================================================================
    # ACT 1 - SLIDE 3: CONCEPT — ARCHITECTURE & INTERFACES
    # =========================================================================
    s3 = prs.slides.add_slide(blank)
    add_header_footer(s3, "System Architecture: Dataflow, Control Plane & Memory", "CONCEPT", MAROON, 3,
        "Top-level architecture of SparseFlex (neural_acc_integrated_top.sv): Host CPU sends layer commands and constraints, "
        "Policy Controller arbitrates PE count in 1 cycle, DMA fills 41 KB 8-bank SRAM, Zero-Gate Feeder drives the 64-PE array, and Drain writes back.")

    add_rect(s3, 0.50, 0.88, 12.333, 4.38, fill=WHITE, line=BORDER_GRAY, line_pt=1.0, rounded=True)
    add_image_fit(s3, os.path.join(REPO_ROOT, "SparseFlex_Architecture_Block_Diagram.jpg"), 0.65, 0.94, 12.03, 4.25)

    io3 = [
        ("INPUTS (Host + DRAM)", MAROON, 0.50,
         "* Signed Q4.12 Activations X & Weights W (16-bit)\n* Range: [-8.0, +7.999755], LSB = 2^-12\n* Constraints: L_max (cycles), P_max (PE cap), pol_sel"),
        ("ARCHITECTURAL CORE", SLATE_DARK, 4.70,
         "* 64 PEs arranged as 4 rows x 16 cols (Q0..Q3)\n* Dual-port 41,472B 8-bank Ping-Pong SRAM\n* Combinatorial Policy Controller + 6-state FSM"),
        ("OUTPUTS (OFMAP + Status)", TEAL, 8.90,
         "* Requantized 16-bit Q4.12 OFMAPs (packed 32-bit)\n* Bit-exact 40b Q16.24 accumulation (MAE = 0.0)\n* Telemetry: cycles, skipped ops, bank conflicts")
    ]
    for t_c, h_c, x_p, txt_c in io3:
        add_card(s3, x_p, 5.40, 3.93, 1.48, t_c, header_fill=h_c)
        add_textbox(s3, x_p + 0.10, 5.80, 3.73, 1.00, txt_c, font_size=10.5, color=SLATE_DARK, valign=MSO_ANCHOR.MIDDLE)

    # =========================================================================
    # ACT 1 - SLIDE 4: CONCEPT — HARDWARE POLICY ENGINE & INTERLOCK
    # =========================================================================
    s4 = prs.slides.add_slide(blank)
    add_header_footer(s4, "Policy Concept: Solving L_max & P_max Constraints in 1 Cycle", "CONCEPT", MAROON, 4,
        "tsk33_transparent_policy_controller.sv arbitrates between Policy A (minimize active PEs within latency budget) "
        "and Policy B (maximize speed within PE cap), enforcing an unconditional safety interlock when P_max < 16.")

    add_card(s4, 0.50, 0.95, 5.95, 2.30, "Two Optimization Objectives + Hardware Safety Lock", header_fill=MAROON)
    tb4 = add_textbox(s4, 0.65, 1.38, 5.65, 1.80)
    add_rich_paragraphs(tb4.text_frame, [
        [("Policy A (pol_sel=0 · Energy Priority): ", True, MAROON), ("Pick min M in {16, 32, 64} with T(M) <= L_max and M <= P_max.", False, SLATE_DARK)],
        [("Policy B (pol_sel=1 · Speed Priority): ", True, TEAL), ("Pick max M with M <= P_max for lowest cycle latency (9,569 cyc @ 64-PE).", False, SLATE_DARK)],
        [("Safety Lock (P_max < 16): ", True, RED_TEXT), ("Unconditionally sets invalid_pe_limit=1, execution_enable=0, mode=2'b11 (0 cycles executed).", False, SLATE_DARK)]
    ], default_size=11, space_after=6)

    tbl_s4 = s4.shapes.add_table(5, 4, Inches(0.50), Inches(3.42), Inches(5.95), Inches(3.42))
    t4 = tbl_s4.table
    for ci, cw in enumerate([1.45, 1.35, 1.25, 1.90]):
        t4.columns[ci].width = Inches(cw)
    t4.rows[0].height = Inches(0.45)
    for ci, htxt in enumerate(["Scenario", "Constraints", "Mode Picked", "Hardware Outcome"]):
        style_table_cell(t4.cell(0, ci), htxt, font_size=10, bold=True, color=WHITE, fill=NAVY)
    for ri, rdata in enumerate([
        ("1. Battery Save", "L=40k, P=64\nPolicy A", "16 PEs\n(2'b00)", "38,225<=40k;\n75% logic saved"),
        ("2. Urgent SLA", "L=15k, P=64\nPolicy A", "64 PEs\n(2'b10)", "9,569<=15k;\nPeak throughput"),
        ("3. Thermal Cap", "L=25k, P=32\nPolicy B", "32 PEs\n(2'b01)", "19,121<=25k;\n+5,879 cyc slack"),
        ("4. Unsafe Cap", "Any L, P=8\nAny Policy", "LOCKED\n(2'b11)", "invalid_pe_limit=1;\n0 compute cycles")
    ], start=1):
        t4.rows[ri].height = Inches(0.74)
        bg = RED_SOFT if ri == 4 else (WHITE if ri % 2 == 1 else BG_LIGHT)
        col_r = RED_TEXT if ri == 4 else NAVY
        for ci, val in enumerate(rdata):
            style_table_cell(t4.cell(ri, ci), val, font_size=10, bold=(ci in (0, 2)), color=col_r, fill=bg)

    add_card(s4, 6.62, 0.95, 6.21, 5.88, "2D Operational Constraint Space (201 Boundary Tests)", header_fill=SLATE_DARK)
    add_image_fit(s4, os.path.join(REPO_ROOT, "NEURAL_ACC_PAPER", "plots", "fig13_policy_space_heatmap.png"), 6.72, 1.40, 6.01, 4.70)
    add_textbox(s4, 6.80, 6.22, 5.85, 0.48,
                "Single-cycle arbitration verified 201 / 201 points in tb_tsk37_policy_audit.sv.",
                font_size=10.5, bold=True, color=GREEN, align=PP_ALIGN.CENTER)

    # =========================================================================
    # ACT 2 - SLIDE 5: WORKING — 7-PHASE HARDWARE EXECUTION PIPELINE
    # =========================================================================
    s5 = prs.slides.add_slide(blank)
    add_header_footer(s5, "How It Works: End-to-End 7-Phase Hardware Pipeline", "WORKING", BLUE, 5,
        "Walking phase-by-phase through layer execution: Phase 1 validates parameters, Phase 2 picks active PEs in 1 cycle, "
        "Phase 3 swaps ping-pong SRAM banks, Phase 4 performs zero-gating, Phase 5 accumulates in 40 bits, Phase 6 rounds/packs, Phase 7 signals completion.")

    phases5 = [
        ("P1: Ingest", MAROON), ("P2: Policy", TEAL), ("P3: Buffer", BLUE),
        ("P4: Zero-Gate", MAROON), ("P5: Compute", SLATE_DARK), ("P6: Drain", AMBER), ("P7: Done", GREEN)
    ]
    px = 0.50
    for idx_p, (pname, pcol) in enumerate(phases5):
        add_rect(s5, px, 0.90, 1.62, 0.44, fill=pcol, rounded=True)
        add_textbox(s5, px + 0.02, 0.92, 1.58, 0.40, pname, font_size=11, bold=True, color=WHITE,
                    align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
        if idx_p < 6:
            add_textbox(s5, px + 1.62, 0.92, 0.17, 0.40, "→", font_size=12, bold=True, color=SLATE_MUTED,
                        align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE, margin_l=0.0, margin_r=0.0)
        px += 1.79

    tbl_s5 = s5.shapes.add_table(8, 5, Inches(0.50), Inches(1.48), Inches(12.333), Inches(5.40))
    t5 = tbl_s5.table
    for ci, cw in enumerate([1.45, 2.25, 3.05, 4.25, 1.333]):
        t5.columns[ci].width = Inches(cw)
    t5.rows[0].height = Inches(0.42)
    for ci, htxt in enumerate(["Phase / State", "Hardware Module", "WHAT It Does (Goal)", "HOW It Does It (RTL Signals & Logic)", "Duration"]):
        style_table_cell(t5.cell(0, ci), htxt, font_size=10.5, bold=True, color=WHITE, fill=NAVY)
    rows5 = [
        ("Phase 1\nST_VALIDATE", "layer_command_\nsequencer.sv", "Ingests descriptor; verifies K > 0 & buffer IDs.",
         "64-bit command checked on ready/valid; flags error_code on K=0 or mode 2'b11.", "2 cycles"),
        ("Phase 2\nCombinatorial", "tsk33_transparent_\npolicy_controller.sv", "Resolves 16/32/64 PEs; enforces safety lock.",
         "Checks T(M)<=L_max and M<=P_max in 1 cycle; locks exec_enable=0 if P_max<16.", "1 cycle"),
        ("Phase 3\nST_CONFIGURE", "dma_controller & ping_\npong_buffer_controller", "Bursts DRAM tensors; swaps Buffer A / B roles.",
         "AXI4 writes Port A while Port B feeds compute; atomic bank swap prevents races.", "Overlapped"),
        ("Phase 4\nST_SPARSE_WAIT", "datapath_compute_\nfeeder & mac_unit_40b", "Suppresses weight reads & MAC zero switching.",
         "Per-PE bypass_mac freezes MAC on act==0; feeder skips wt reads if all_acts_zero.", "Per step"),
        ("Phase 5\nST_WAIT_COMP", "pe_array_40b.sv\n(4x16 PEs)", "Executes multi-pass MACs into 40-bit sums.",
         "Quadrants clock-gated via col_active; P = 64/N_active passes into 40b Q16.24.", "9.5k–38.2k\ncycles"),
        ("Phase 6\nST_DRAIN", "ofmap_drain_ctrl &\nrequantization_unit.sv", "Rounds, saturates & packs 40b into Q4.12.",
         "Adds round_offset (2048), shifts >>>12, clamps [-32768,32767], packs 32b words.", "128 words"),
        ("Phase 7\nST_COMPLETE", "layer_command_\nsequencer & Telemetry", "Notifies Host CPU & records hardware stats.",
         "Asserts layer_done_pulse; latches cycles, skipped ops & SRAM bank conflicts.", "1 cycle")
    ]
    for ri, rdata in enumerate(rows5, start=1):
        t5.rows[ri].height = Inches(0.71)
        bg = WHITE if ri % 2 == 1 else BG_LIGHT
        style_table_cell(t5.cell(ri, 0), rdata[0], font_size=10, bold=True, color=MAROON, fill=bg)
        style_table_cell(t5.cell(ri, 1), rdata[1], font_size=9.5, bold=False, color=BLUE, fill=bg, font_name=FONT_MONO)
        style_table_cell(t5.cell(ri, 2), rdata[2], font_size=10, bold=True, color=NAVY, fill=bg, align=PP_ALIGN.LEFT)
        style_table_cell(t5.cell(ri, 3), rdata[3], font_size=10, bold=False, color=SLATE_DARK, fill=bg, align=PP_ALIGN.LEFT)
        style_table_cell(t5.cell(ri, 4), rdata[4], font_size=10, bold=True, color=TEAL, fill=bg)

    # =========================================================================
    # ACT 2 - SLIDE 6: WORKING EXAMPLE 1/3 — MATRIX INPUTS & DENSE BASELINE
    # =========================================================================
    s6 = prs.slides.add_slide(blank)
    add_header_footer(s6, "Worked Example (1/3): Matrix Inputs & Dense Computation", "WORKING", BLUE, 6,
        "Concrete 4x4 activation matrix A (8 zeros = 50% sparsity) and weight matrix W. "
        "Without sparsity filtering, dense execution computes all 16 MACs to obtain Y = [3, 4, 4, 5]^T.")

    A_mat = [[1, 0, 2, 0], [0, 3, 0, 1], [2, 0, 1, 0], [0, 1, 0, 2]]
    W_mat = [[1, 2, 1, 1], [2, 1, 2, 1], [1, 1, 2, 2], [2, 1, 1, 2]]

    add_card(s6, 0.50, 0.95, 4.10, 4.65, "Step 1: Activation Matrix A (4x4)", header_fill=MAROON)
    draw_matrix_grid(s6, 0.78, 1.60, 0.88, 0.68, A_mat, highlight_zeros=True,
                     sub_label="Red cells = 0  (Triggers Zero-Gating)")
    add_rect(s6, 0.68, 4.68, 3.74, 0.78, fill=MAROON_LIGHT, line=MAROON, line_pt=1.0, rounded=True)
    add_textbox(s6, 0.78, 4.74, 3.54, 0.66,
                "Total Elements = 4 x 4 = 16  |  Zeros = 8\nActivation Sparsity = 8 / 16 = 50%",
                font_size=12.5, bold=True, color=MAROON, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    add_card(s6, 4.82, 0.95, 3.70, 4.65, "Step 2: Weight Matrix W (4x4)", header_fill=SLATE_DARK)
    draw_matrix_grid(s6, 5.15, 1.60, 0.76, 0.68, W_mat, highlight_zeros=False)
    add_rect(s6, 5.00, 4.68, 3.34, 0.78, fill=BLUE_LIGHT, line=BLUE, line_pt=1.0, rounded=True)
    add_textbox(s6, 5.08, 4.74, 3.18, 0.66,
                "Row-Wise Dot Product Operation:\nY[i] = Sum_{j=0..3} A[i][j] * W[i][j]",
                font_size=11.5, bold=True, color=BLUE, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    add_card(s6, 8.74, 0.95, 4.09, 4.65, "Step 3: Normal Dense Computation", header_fill=TEAL)
    tb6 = add_textbox(s6, 8.92, 1.48, 3.75, 2.70)
    add_rich_paragraphs(tb6.text_frame, [
        [("Row 0: ", True, MAROON), ("(1x1) + (0x2) + (2x1) + (0x1) = ", False, SLATE_DARK), ("3", True, NAVY)],
        [("Row 1: ", True, MAROON), ("(0x2) + (3x1) + (0x2) + (1x1) = ", False, SLATE_DARK), ("4", True, NAVY)],
        [("Row 2: ", True, MAROON), ("(2x1) + (0x1) + (1x2) + (0x2) = ", False, SLATE_DARK), ("4", True, NAVY)],
        [("Row 3: ", True, MAROON), ("(0x2) + (1x1) + (0x1) + (2x2) = ", False, SLATE_DARK), ("5", True, NAVY)],
    ], default_size=12, space_after=12)
    add_rect(s6, 8.94, 4.30, 3.70, 1.15, fill=GREEN_LIGHT, line=GREEN, line_pt=1.2, rounded=True)
    add_textbox(s6, 9.00, 4.38, 3.58, 0.98,
                "Dense Output Y = [ 3,  4,  4,  5 ]^T\nDense Total Multiplications = 16 MACs",
                font_size=12, bold=True, color=GREEN, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    add_rect(s6, 0.50, 5.82, 12.333, 1.00, fill=WHITE, line=MAROON, line_pt=1.5, rounded=True)
    add_textbox(s6, 0.70, 5.90, 11.933, 0.84,
                "Half of all dense terms (8 of 16) compute 0 x W = 0 — adding zero value while wasting dynamic switching power.",
                font_size=13, bold=True, color=NAVY, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    # =========================================================================
    # ACT 2 - SLIDE 7: WORKING EXAMPLE 2/3 — SYNCHRONOUS ZERO-GATING
    # =========================================================================
    s7 = prs.slides.add_slide(blank)
    add_header_footer(s7, "Worked Example (2/3): Synchronous Zero-Gating (50% MAC Cut)", "WORKING", BLUE, 7,
        "Zero-gating skips all 8 zero multiplications inside the 4x4 matrix example (50% MAC reduction) while maintaining "
        "exact timing determinism (0.00% jitter) via mac_unit_40b.sv bypass_mac and datapath_compute_feeder.sv all_acts_zero.")

    add_card(s7, 0.50, 0.95, 6.20, 4.55, "Step 4 & 5: Row-by-Row Zero-Gating Walkthrough", header_fill=MAROON)
    tbl_s7 = s7.shapes.add_table(5, 4, Inches(0.70), Inches(1.48), Inches(5.80), Inches(2.55))
    t7 = tbl_s7.table
    for ci, cw in enumerate([1.25, 1.15, 1.45, 1.95]):
        t7.columns[ci].width = Inches(cw)
    t7.rows[0].height = Inches(0.45)
    for ci, htxt in enumerate(["Row 0 Act", "Weight", "RTL bypass_mac", "HW Action"]):
        style_table_cell(t7.cell(0, ci), htxt, font_size=10.5, bold=True, color=WHITE, fill=NAVY)
    for ri, rdata in enumerate([
        ("A[0,0] = 1", "W[0,0] = 1", "0 (Active)", "Compute: 1 x 1 = 1"),
        ("A[0,1] = 0", "W[0,1] = 2", "1 (Zero Gate)", "SKIP MAC (Hold Acc)"),
        ("A[0,2] = 2", "W[0,2] = 1", "0 (Active)", "Compute: 2 x 1 = 2"),
        ("A[0,3] = 0", "W[0,3] = 1", "1 (Zero Gate)", "SKIP MAC (Hold Acc)")
    ], start=1):
        t7.rows[ri].height = Inches(0.52)
        is_skip = "SKIP" in rdata[3]
        bg = RED_SOFT if is_skip else GREEN_LIGHT
        fg = RED_TEXT if is_skip else GREEN
        for ci, val in enumerate(rdata):
            style_table_cell(t7.cell(ri, ci), val, font_size=10.5, bold=(ci >= 2 or is_skip),
                             color=fg if ci >= 2 else NAVY, fill=bg)

    add_rect(s7, 0.70, 4.22, 5.80, 1.10, fill=BLUE_LIGHT, line=BLUE, line_pt=1.2, rounded=True)
    add_textbox(s7, 0.80, 4.30, 5.60, 0.94,
                "Full Matrix: Dense = 16  |  Skipped = 8  |  Useful = 8 MACs\n"
                "MAC Reduction = (16 - 8)/16 = 50%  (Output Y = [3,4,4,5]^T Unchanged)",
                font_size=11, bold=True, color=BLUE, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    add_card(s7, 6.95, 0.95, 5.88, 4.55, "RTL Zero-Gating Mechanism (Two Granularities)", header_fill=SLATE_DARK)
    tb7 = add_textbox(s7, 7.15, 1.48, 5.48, 3.85)
    add_rich_paragraphs(tb7.text_frame, [
        [("1. Per-PE Zero Bypass (", True, MAROON), ("mac_unit_40b.sv", True, BLUE, FONT_MONO), ("):", True, MAROON)],
        [("   bypass_mac = (!act_mask) || (act_data == 0)", False, NAVY, FONT_MONO, 10.5)],
        [("   * Forces multiplier product to 0 & freezes 40-bit accumulator register update cleanly.", False, SLATE_DARK)],
        [("2. Row-Group Weight Skip (", True, TEAL), ("datapath_compute_feeder.sv", True, BLUE, FONT_MONO), ("):", True, TEAL)],
        [("   * Checks all_acts_zero across 4 parallel PE rows in ST_SPARSE_WAIT_A to skip weight SRAM reads.", False, SLATE_DARK)],
        [("3. Strict Timing Determinism:", True, GREEN)],
        [("   * Pipeline slot counters advance uniformly — 0.00% timing jitter on outputs.", False, SLATE_DARK)]
    ], default_size=11.5, space_after=6)

    add_rect(s7, 0.50, 5.72, 12.333, 1.10, fill=MAROON_LIGHT, line=MAROON, line_pt=1.5, rounded=True)
    add_textbox(s7, 0.70, 5.80, 11.933, 0.94,
                "Synchronous Zero-Gating eliminates multiplier, accumulator, and SRAM switching on zeros while guaranteeing fixed execution latency.",
                font_size=12.5, bold=True, color=MAROON, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    # =========================================================================
    # ACT 2 - SLIDE 8: WORKING EXAMPLE 3/3 — 64/32/16 PE SCALING & MULTI-PASS TILING
    # =========================================================================
    s8 = prs.slides.add_slide(blank)
    add_header_footer(s8, "Worked Example (3/3): PE Scaling & Multi-Pass Channel Tiling", "WORKING", BLUE, 8,
        "How 64, 32, and 16 active PEs execute across Q0..Q3 quadrants using P = 64/N_active passes in channel_tile_controller.sv, "
        "preserving all 128 output words while exposing the memory vs logic trade-off.")

    modes8 = [
        ("Full Array: 64 PEs (2'b10)", SLATE_DARK, 0.50,
         "col_active = 16'hFFFF  (All 16 cols ON)",
         "Passes: P = 64 / 64 = 1 Pass",
         "All 64 channels computed in parallel\n\n* Active PE Logic: 100%\n* Latency: 9,569 cycles (1x Base)\n* Act SRAM Reads: 9,216 (1x Base)"),
        ("Medium Scale: 32 PEs (2'b01)", BLUE, 4.70,
         "col_active = 16'h00FF  (Cols 0..7 ON)",
         "Passes: P = 64 / 32 = 2 Passes",
         "Pass 1: Ch 0-31   |   Pass 2: Ch 32-63\nY = Y_pass1 U Y_pass2 (128 words)\n* Active PE Logic Saved: 50.0%\n* Act SRAM Reads: +100% (18,432)"),
        ("Low Power: 16 PEs (2'b00)", MAROON, 8.90,
         "col_active = 16'h000F  (Cols 0..3 ON)",
         "Passes: P = 64 / 16 = 4 Passes",
         "Pass 1: Ch 0-15  |  Pass 2: Ch 16-31\nPass 3: Ch 32-47 |  Pass 4: Ch 48-63\n* Active PE Logic Saved: 75.0%\n* Act SRAM Reads: +300% (36,864)")
    ]
    for m_title, m_col, x_pos, mask_txt, pass_txt, body_txt in modes8:
        add_card(s8, x_pos, 0.95, 3.93, 4.25, m_title, header_fill=m_col)
        add_textbox(s8, x_pos + 0.10, 1.40, 3.73, 0.34, mask_txt, font_size=9.5, bold=True, color=m_col, font_name=FONT_MONO, valign=MSO_ANCHOR.MIDDLE)
        q_cnt = 4 if "64" in m_title else (2 if "32" in m_title else 1)
        for qi in range(4):
            q_on = (qi < q_cnt)
            qf = m_col if q_on else BORDER_GRAY
            qt = WHITE if q_on else SLATE_MUTED
            add_rect(s8, x_pos + 0.14 + qi * 0.92, 1.82, 0.84, 0.56, fill=qf, rounded=True)
            add_textbox(s8, x_pos + 0.14 + qi * 0.92, 1.84, 0.84, 0.52, f"Q{qi}\n{'ON' if q_on else 'OFF'}",
                        font_size=10, bold=True, color=qt, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
        add_rect(s8, x_pos + 0.12, 2.52, 3.69, 0.42, fill=AMBER_LIGHT, line=AMBER, line_pt=1.0, rounded=True)
        add_textbox(s8, x_pos + 0.16, 2.55, 3.61, 0.36, pass_txt, font_size=12, bold=True, color=AMBER,
                    align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
        add_textbox(s8, x_pos + 0.14, 3.04, 3.65, 2.05, body_txt, font_size=11, color=SLATE_DARK)

    add_rect(s8, 0.50, 5.42, 12.333, 1.42, fill=MAROON_LIGHT, line=MAROON, line_pt=1.5, rounded=True)
    add_textbox(s8, 0.72, 5.50, 11.90, 1.26,
                "Multi-Pass Tiling Insight (channel_tile_controller.sv): Arbitrary channel counts & tail tiles (e.g., 18 ch = 36 words) "
                "execute without truncation, but re-reading activations P times scales Act SRAM traffic by +100% (32-PE) and +300% (16-PE).",
                font_size=12.5, bold=True, color=MAROON, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    # =========================================================================
    # ACT 2 - SLIDE 9: WORKING — Q4.12, 40-BIT ACCUMULATOR & PING-PONG SRAM
    # =========================================================================
    s9 = prs.slides.add_slide(blank)
    add_header_footer(s9, "Inside the Datapath: Q4.12 Precision, 40b MAC & Ping-Pong SRAM", "WORKING", BLUE, 9,
        "Data precision and memory overlap: Q4.12 inputs multiply to 32-bit Q8.24, accumulate into 40-bit Q16.24 (8 guard bits), "
        "and round via Round-Half-Up (+2048, >>>12) back to packed Q4.12 words while dual-port ping-pong SRAM prevents stalls.")

    add_card(s9, 0.50, 0.95, 7.15, 4.35, "Q4.12 -> Q8.24 -> 40-Bit Q16.24 -> Requantization Math", header_fill=MAROON)
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

    add_card(s9, 7.85, 0.95, 4.98, 4.35, "41,472B 8-Bank Ping-Pong SRAM Overlap", header_fill=TEAL)
    add_textbox(s9, 8.02, 1.40, 4.64, 0.68,
                "8 interleaved dual-port banks (5,184 B/bank)\npartitioned into logical Buffer A & Buffer B:",
                font_size=11, bold=True, color=NAVY)
    py9 = 2.18
    for lbl, r_txt, w_txt, c_l, c_r in [
        ("Cycle / Layer 1", "Buffer A -> PE Reads (Port B)", "Buffer B <- DMA Writes (Port A)", BLUE_LIGHT, MAROON_LIGHT),
        ("Cycle / Layer 2", "Buffer B -> PE Reads (Port B)", "Buffer A <- DMA Writes (Port A)", MAROON_LIGHT, BLUE_LIGHT),
        ("Cycle / Layer 3", "Buffer A -> PE Reads (Port B)", "Buffer B <- DMA Writes (Port A)", BLUE_LIGHT, MAROON_LIGHT),
    ]:
        add_textbox(s9, 8.02, py9, 4.64, 0.26, lbl, font_size=10, bold=True, color=SLATE_MUTED)
        add_rect(s9, 8.02, py9 + 0.25, 2.26, 0.52, fill=c_l, line=BLUE, line_pt=0.8, rounded=True)
        add_textbox(s9, 8.05, py9 + 0.27, 2.20, 0.48, r_txt, font_size=9.5, bold=True, color=NAVY, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
        add_rect(s9, 10.40, py9 + 0.25, 2.26, 0.52, fill=c_r, line=MAROON, line_pt=0.8, rounded=True)
        add_textbox(s9, 10.43, py9 + 0.27, 2.20, 0.48, w_txt, font_size=9.5, bold=True, color=MAROON, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)
        py9 += 0.90
    add_textbox(s9, 8.02, 4.88, 4.64, 0.35, "Zero read-after-write hazards | Continuous compute.", font_size=10.5, bold=True, color=TEAL, align=PP_ALIGN.CENTER)

    add_rect(s9, 0.50, 5.52, 12.333, 1.30, fill=GREEN_LIGHT, line=GREEN, line_pt=1.5, rounded=True)
    add_textbox(s9, 0.70, 5.62, 11.933, 1.10,
                "All 32 Shift Boundaries (S in 0..31) & Extreme Limits (+/- 2^39) Verified Bit-Exact in TSK-21 & TSK-37:\n"
                "Round-Half-Up Hardware == 64-Bit Python Golden Reference  |  MAE = 0.000000  |  RMSE = 0.000000",
                font_size=12.5, bold=True, color=GREEN, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    # =========================================================================
    # ACT 3 - SLIDE 10: RESULTS — SPARSITY SAVINGS & 0.00% JITTER
    # =========================================================================
    s10 = prs.slides.add_slide(blank)
    add_header_footer(s10, "Result (1): Sparsity Cuts Switching -84.92% with 0.00% Jitter", "RESULTS", GREEN, 10,
        "Measured across WL1 to WL4 (ResNet-18, VGG-16-BN) in TSK33_MEASUREMENT_RESULTS.csv: weight SRAM reads drop "
        "from 147,456 to 22,240 (-84.92%), active compute cycles drop 9,216 -> 1,390, while total execution cycles stay fixed at 9,569.")

    add_card(s10, 0.50, 0.95, 6.20, 5.88, "Weight Read Reduction (TSK33_MEASUREMENT_RESULTS.csv)", header_fill=GREEN)
    add_image_fit(s10, os.path.join(REPO_ROOT, "presentation_charts", "chart_sparsity_weights.png"), 0.62, 1.40, 5.96, 4.35)
    add_rect(s10, 0.68, 5.86, 5.84, 0.82, fill=GREEN_LIGHT, line=GREEN, line_pt=1.0, rounded=True)
    add_textbox(s10, 0.78, 5.92, 5.64, 0.70,
                "Strict Determinism Verified: Dense == Sparse Total Cycles (0.00% Jitter)\n"
                "64-PE: 9,569 cyc  |  32-PE: 19,121 cyc  |  16-PE: 38,225 cyc",
                font_size=11, bold=True, color=GREEN, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    add_card(s10, 6.90, 0.95, 5.93, 5.88, "Exact 64-PE Mode Measurements Across 4 Workloads", header_fill=NAVY)
    tbl_s10 = s10.shapes.add_table(5, 5, Inches(7.05), Inches(1.48), Inches(5.63), Inches(2.90))
    t10 = tbl_s10.table
    for ci, cw in enumerate([1.50, 0.98, 1.05, 1.12, 0.98]):
        t10.columns[ci].width = Inches(cw)
    t10.rows[0].height = Inches(0.48)
    for ci, htxt in enumerate(["Workload", "Total Cyc", "Comp Cyc", "Wt Reads", "Saved"]):
        style_table_cell(t10.cell(0, ci), htxt, font_size=9.8, bold=True, color=WHITE, fill=NAVY)
    for ri, rdata in enumerate([
        ("WL1 (ResNet18)\nCIFAR-10", "9,569\n(0% Delta)", "2,867", "45,872", "-68.89%"),
        ("WL2 (ResNet18)\nCIFAR-100", "9,569\n(0% Delta)", "3,081", "49,296", "-66.57%"),
        ("WL3 (VGG-16)\nCIFAR-10", "9,569\n(0% Delta)", "4,782", "76,512", "-48.11%"),
        ("WL4 (ResNet18)\nDeep conv2", "9,569\n(0% Delta)", "1,390", "22,240", "-84.92%")
    ], start=1):
        t10.rows[ri].height = Inches(0.60)
        bg = WHITE if ri % 2 == 1 else BG_LIGHT
        for ci, val in enumerate(rdata):
            style_table_cell(t10.cell(ri, ci), val, font_size=9.8, bold=(ci in (0, 4)),
                             color=GREEN if ci == 4 else NAVY, fill=bg,
                             align=PP_ALIGN.LEFT if ci == 0 else PP_ALIGN.CENTER)

    add_rect(s10, 7.05, 4.58, 5.63, 2.08, fill=MAROON_LIGHT, line=MAROON, line_pt=1.0, rounded=True)
    tb10 = add_textbox(s10, 7.18, 4.66, 5.37, 1.92)
    add_rich_paragraphs(tb10.text_frame, [
        [("What Sparsity Gives Us:", True, MAROON)],
        [("* Up to ", False, SLATE_DARK), ("84.92% reduction", True, GREEN), (" in active compute cycles (9,216 -> 1,390) and weight SRAM reads (147,456 -> 22,240).", False, SLATE_DARK)],
        [("* Identical ", False, SLATE_DARK), ("0.00% latency variation", True, NAVY), (" across every workload and PE mode.", False, SLATE_DARK)],
        [("* Zero integer output mismatches (0/1,024 outputs).", False, SLATE_DARK)]
    ], default_size=11, space_after=5)

    # =========================================================================
    # ACT 3 - SLIDE 11: RESULTS BEYOND SPARSITY (1/2) — SCALING, SPEEDUP & TRADE-OFF
    # =========================================================================
    s11 = prs.slides.add_slide(blank)
    add_header_footer(s11, "Result (2) Beyond Sparsity: PE Scaling, 4x Speedup & Memory Tax", "RESULTS", GREEN, 11,
        "Non-sparsity result 1: Dynamic scaling cuts active PE logic by 50%–75% or speeds up execution by 3.995x (38,225 -> 9,569 cycles). "
        "We also quantify the multi-pass activation read inflation (+100%/+300%) and WL4 total SRAM traffic (+87.18%).")

    add_card(s11, 0.50, 0.95, 6.45, 5.88, "Measured PE Scaling vs. Memory Inflation (TSK33 CSV)", header_fill=MAROON)
    add_image_fit(s11, os.path.join(REPO_ROOT, "presentation_charts", "chart_scaling_tradeoff.png"), 0.62, 1.40, 6.21, 4.40)
    add_textbox(s11, 0.72, 5.92, 6.00, 0.78,
                "Exact WL4 Sparse SRAM Totals: 31,712 (64-PE) -> 40,928 (+29.06%) -> 59,360 (+87.18%).\n"
                "WL1 Totals: 55,344 (64-PE) -> 64,560 (+16.65%) -> 82,992 (+49.96%).",
                font_size=10, bold=True, color=SLATE_DARK, align=PP_ALIGN.CENTER)

    add_card(s11, 7.15, 0.95, 5.68, 5.88, "Non-Sparsity Scaling Gains & Honest Trade-Off", header_fill=BLUE)
    tbl_s11 = s11.shapes.add_table(4, 5, Inches(7.30), Inches(1.48), Inches(5.38), Inches(2.20))
    t11 = tbl_s11.table
    for ci, cw in enumerate([0.92, 1.05, 1.15, 1.08, 1.18]):
        t11.columns[ci].width = Inches(cw)
    t11.rows[0].height = Inches(0.45)
    for ci, htxt in enumerate(["Mode", "Logic Cut", "Cycles (@100M)", "Speedup", "Act Tax"]):
        style_table_cell(t11.cell(0, ci), htxt, font_size=9.5, bold=True, color=WHITE, fill=NAVY)
    for ri, rdata in enumerate([
        ("64-PE", "0.0%", "9,569\n(95.69 us)", "3.995x\nvs 16-PE", "1.0x Base\n(9,216)"),
        ("32-PE", "50.0%", "19,121\n(191.2 us)", "1.999x\nvs 16-PE", "+100.0%\n(18,432)"),
        ("16-PE", "75.0%", "38,225\n(382.3 us)", "1.000x\nBaseline", "+300.0%\n(36,864)")
    ], start=1):
        t11.rows[ri].height = Inches(0.58)
        bg = WHITE if ri % 2 == 1 else BG_LIGHT
        for ci, val in enumerate(rdata):
            c_t = GREEN if ((ci == 1 and ri > 1) or (ci == 3 and ri == 1)) else (RED_TEXT if (ci == 4 and ri > 1) else NAVY)
            style_table_cell(t11.cell(ri, ci), val, font_size=9.5, bold=(ci in (0, 1, 3, 4)), color=c_t, fill=bg)

    add_rect(s11, 7.30, 3.90, 5.38, 2.74, fill=BLUE_LIGHT, line=BLUE, line_pt=1.2, rounded=True)
    tb11 = add_textbox(s11, 7.45, 4.00, 5.08, 2.54)
    add_rich_paragraphs(tb11.text_frame, [
        [("Positive Gains Independent of Sparsity:", True, BLUE)],
        [("1. Peak Logic/Power Reduction: ", True, NAVY), ("Down-scaling cuts active PEs 50%–75% even on 100% dense inputs.", False, SLATE_DARK)],
        [("2. Near-Ideal 4x Throughput Scaling: ", True, NAVY), ("Scaling up to 64 PEs cuts runtime 382.25 us -> 95.69 us (3.995x).", False, SLATE_DARK)],
        [("3. Refuting Naive Linear Scaling: ", True, NAVY), ("First empirical quantification showing +300% act SRAM re-reads under 4-pass throttling.", False, SLATE_DARK)]
    ], default_size=11, space_after=6)

    # =========================================================================
    # ACT 3 - SLIDE 12: RESULTS BEYOND SPARSITY (2/2) — POLICY ENGINE & SAFETY LOCK
    # =========================================================================
    s12 = prs.slides.add_slide(blank)
    add_header_footer(s12, "Result (3) Beyond Sparsity: Policy Control & Hardware Safety", "RESULTS", GREEN, 12,
        "Non-sparsity result 2: Over 560 constraint tests in TSK-35B and 201 boundary checks in TSK-37, Policy A minimizes "
        "PEs cleanly, Policy B delivers 100% min latency under P_max, and all 240 invalid P_max < 16 requests are blocked.")

    add_card(s12, 0.50, 0.95, 6.35, 5.88, "560 Constraint Evaluations: Policy A vs. Policy B", header_fill=TEAL)
    add_image_fit(s12, os.path.join(REPO_ROOT, "presentation_charts", "chart_policy_distribution.png"), 0.62, 1.42, 6.11, 4.35)
    add_rect(s12, 0.68, 5.88, 5.99, 0.80, fill=TEAL_LIGHT, line=TEAL, line_pt=1.0, rounded=True)
    add_textbox(s12, 0.78, 5.94, 5.79, 0.68,
                "Policy A saves PEs (47.5% at 16-PE, 32.5% at 32-PE) when deadlines allow;\n"
                "Policy B hits min allowed latency in 100% of valid cases | 240/240 Unsafe Blocked.",
                font_size=10.5, bold=True, color=TEAL, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    add_card(s12, 7.05, 0.95, 5.78, 5.88, "Verified Policy & Fail-Safe Metrics (TSK-35B / TSK-37)", header_fill=NAVY)
    tb12 = add_textbox(s12, 7.25, 1.48, 5.38, 5.15)
    add_rich_paragraphs(tb12.text_frame, [
        [("1. Policy A (Min-Resource Objective):", True, MAROON)],
        [("   * Selected 16-PE (75% logic saved) in 76/160 valid tests (47.50%).", False, SLATE_DARK)],
        [("   * Selected 32-PE (50% logic saved) in 52/160 valid tests (32.50%).", False, SLATE_DARK)],
        [("   * Escalated to 64-PE only on tight deadlines (32/160 = 20.00%).", False, SLATE_DARK)],
        [("2. Policy B (Min-Latency Objective):", True, TEAL)],
        [("   * Achieved lowest possible cycle time under P_max across 100% of valid tests (80 at 64-PE, 40 at 32-PE, 40 at 16-PE).", False, SLATE_DARK)],
        [("3. Hardware Fail-Safe Interlock Verification:", True, RED_TEXT)],
        [("   * All 240 unsafe calls (P_max = 0, 8, 15 in TSK-35B) + 201 boundary checks in TSK-37 triggered invalid_pe_limit=1 & execution_enable=0.", False, SLATE_DARK)],
        [("   * 0 unauthorized compute cycles & 0 SRAM corruptions.", True, GREEN)]
    ], default_size=11, space_after=6)

    # =========================================================================
    # ACT 3 - SLIDE 13: RESULTS BEYOND SPARSITY (3/3) — ZERO CONFLICTS, ACCURACY & RIGOR
    # =========================================================================
    s13 = prs.slides.add_slide(blank)
    add_header_footer(s13, "Result (4) Beyond Sparsity: Zero Stalls, Bit-Exact Math & Suites", "RESULTS", GREEN, 13,
        "Non-sparsity results 3 & 4: TSK-20 confirms 0 bank conflicts and 0 stalls across 1,124 cycles; TSK-21/37 proves MAE = 0.000000 "
        "with 100% channel & tail-tile preservation; 20/20 suites pass 12,202 baseline assertions.")

    kpis13 = [
        ("0 / 1,124", "SRAM Bank Conflicts\n& 0.0000 Stall Ratio", MAROON),
        ("5.00 W/cyc", "Peak Sustained\nSRAM Bandwidth", BLUE),
        ("0.000000", "MAE & RMSE\n(589,824 MACs)", GREEN),
        ("20 / 20", "Suites · 12,202+ Checks\n(0 Failures)", TEAL)
    ]
    kx = 0.50
    for kb, ks, kc in kpis13:
        add_rect(s13, kx, 0.95, 2.93, 1.32, fill=WHITE, line=kc, line_pt=1.8, rounded=True)
        add_rect(s13, kx, 0.95, 2.93, 0.08, fill=kc)
        add_textbox(s13, kx + 0.08, 1.08, 2.77, 0.50, kb, font_size=24, bold=True, color=kc, align=PP_ALIGN.CENTER)
        add_textbox(s13, kx + 0.08, 1.62, 2.77, 0.56, ks, font_size=10.5, bold=True, color=SLATE_MUTED, align=PP_ALIGN.CENTER)
        kx += 3.133

    add_card(s13, 0.50, 2.48, 6.20, 4.35, "Memory Arbitration & Numerical Integrity Results", header_fill=NAVY)
    tb13_l = add_textbox(s13, 0.68, 2.96, 5.84, 3.74)
    add_rich_paragraphs(tb13_l.text_frame, [
        [("Zero Stalls & Bank Conflicts (TSK20_MEMORY_REPLAY_RESULTS.csv):", True, MAROON)],
        [("  * 8/8 dense & sparse workloads hit Rd_Stall=0, Wr_Stall=0, Bank_Conflict_Cycles=0 across 1,124 reconciled cycles.", False, SLATE_DARK)],
        [("Channel Preservation & Tail Tiles (TSK-21 / TSK-23):", True, BLUE)],
        [("  * 16-PE == 32-PE == 64-PE identical checksums; 64/64 channels preserved; arbitrary non-multiples (18 ch = 36 words) pass 32/32 SRAM readback.", False, SLATE_DARK)],
        [("Full Regression & Baseline Governance:", True, GREEN)],
        [("  * 5/5 protected baseline RTL files cleanly untouched (0 diffs); >13,200 total unified assertions pass with Exit Code 0.", False, SLATE_DARK)]
    ], default_size=11, space_after=7)

    add_card(s13, 6.95, 2.48, 5.88, 4.35, "Live Simulation Runner & Honest Boundaries", header_fill=MAROON)
    add_rect(s13, 7.15, 3.00, 5.48, 2.30, fill=NAVY, rounded=True)
    add_textbox(s13, 7.28, 3.08, 5.22, 2.14,
                "python run_demo.py --regression  # 20 Suites (12,202 checks)\n"
                "python run_demo.py --telemetry   # Live WL1-WL4 Trade-off\n"
                "python run_demo.py --numerical   # MAE=0.0 Across 589,824 MACs\n"
                "python run_demo.py --policy      # 201-Point Interlock Audit\n"
                "python run_demo.py --sparse      # 10 Live Zero-Gate Cases\n"
                "python run_demo.py --all         # Complete Live Defense Demo",
                font_size=10, color=RGBColor(0x86, 0xEF, 0xAC), font_name=FONT_MONO, valign=MSO_ANCHOR.MIDDLE)
    add_rect(s13, 7.15, 5.45, 5.48, 1.22, fill=AMBER_LIGHT, line=AMBER, line_pt=1.0, rounded=True)
    add_textbox(s13, 7.28, 5.52, 5.22, 1.08,
                "Toolchain Boundary Honesty: Physical synthesis / silicon mW numbers are marked NOT_RUN due to host Vivado license absence "
                "(288 KB VCD w/ 21,888 transitions & SDC/Tcl flows ready).",
                font_size=10.5, bold=True, color=AMBER, valign=MSO_ANCHOR.MIDDLE)

    # =========================================================================
    # ACT 3 - SLIDE 14: UNIFIED SUMMARY & CONCLUSION
    # =========================================================================
    s14 = prs.slides.add_slide(blank)
    set_slide_bg(s14, NAVY)
    add_rect(s14, 0, 0, 13.333, 0.10, fill=GREEN)

    add_textbox(s14, 0.70, 0.40, 11.90, 0.56, "Conclusion: Concept, Working & Positive Results",
                font_size=26, bold=True, color=WHITE, valign=MSO_ANCHOR.MIDDLE)

    add_rect(s14, 0.70, 1.15, 9.00, 0.78, fill=MAROON, line=GOLD, line_pt=1.5, rounded=True)
    add_textbox(s14, 0.85, 1.21, 8.70, 0.66,
                "SparseFlex = Synchronous Zero-Gating + Configurable PEs (16/32/64) + Multi-Pass Tiling",
                font_size=14.5, bold=True, color=WHITE, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    boxes14 = [
        ("Sparsity & Working Concept Wins", GREEN, 0.70,
         "* Synchronous Zero-Gating cuts weight SRAM reads & active MAC switching by 48.11% to 84.92% (147,456 -> 22,240 reads).\n\n"
         "* Strict Timing Determinism: Exact 0.00% latency variation (9,569 / 19,121 / 38,225 cycles fixed) for safety-critical RTOS deadlines.\n\n"
         "* Worked 4x4 Matrix Verified: Complete Q4.12 -> 40-bit Q16.24 -> Q4.12 pipeline trace with zero timing bubbles."),
        ("Non-Sparsity Architectural Wins", BLUE, 5.28,
         "* Dynamic PE Scaling: Cuts active PE logic by 50% (32-PE) or 75% (16-PE), OR scales speed 3.995x (38,225 -> 9,569 cyc).\n\n"
         "* 1-Cycle Safe Policy Engine: 201/201 boundary checks pass; 240/240 unsafe P_max < 16 requests blocked with 0 compute cycles.\n\n"
         "* Zero Stalls / Conflicts & Bit-Exact Math: 0 bank conflicts across 1,124 cycles | MAE = 0.000000 | +100%/+300% act trade-off quantified.")
    ]
    for b_t, b_c, bx, b_txt in boxes14:
        add_card(s14, bx, 2.15, 4.42, 4.10, b_t, header_fill=b_c, body_fill=SLATE_DARK, border=b_c)
        add_textbox(s14, bx + 0.16, 2.68, 4.10, 3.42, b_txt, font_size=11.5, color=WHITE)

    add_rect(s14, 9.95, 1.18, 2.75, 5.02, fill=WHITE, rounded=True)
    add_image_fit(s14, os.path.join(REPO_ROOT, "github_repo_qr.png"), 10.18, 1.42, 2.28, 2.28)
    add_textbox(s14, 10.05, 3.90, 2.55, 2.10,
                "Thank You!\nQuestions & Discussion\n\nRaushan Kumar\nDept. of CSE, IIT Tirupati",
                font_size=13, bold=True, color=NAVY, align=PP_ALIGN.CENTER, valign=MSO_ANCHOR.MIDDLE)

    add_rect(s14, 0.70, 6.75, 12.0, 0.02, fill=SLATE_MUTED)
    add_textbox(s14, 0.70, 6.85, 8.8, 0.35, "SparseFlex: Concept, Working & Results  |  IIT Tirupati M.Tech Defense",
                font_size=10, color=RGBColor(0x94, 0xA3, 0xB8))
    add_textbox(s14, 11.2, 6.85, 1.5, 0.35, "Slide 14 / 14", font_size=10, bold=True, color=WHITE, align=PP_ALIGN.RIGHT)
    s14.notes_slide.notes_text_frame.text = (
        "In summary, SparseFlex validates both deterministic sparsity exploitation (-84.92% switching, 0% jitter) and strong "
        "non-sparsity architectural wins (50-75% logic scaling, 3.995x speedup, 1-cycle safe policy control, zero SRAM stalls, MAE=0). Thank you!"
    )

    prs.save(OUT_PPTX)
    print(f"[SUCCESS] Generated Concept-Working-Results deck: {OUT_PPTX}")


if __name__ == "__main__":
    build_deck()

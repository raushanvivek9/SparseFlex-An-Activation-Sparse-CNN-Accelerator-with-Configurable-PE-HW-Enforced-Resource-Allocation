#!/usr/bin/env python3
"""Generate crisp 300-DPI presentation charts directly from verified SparseFlex CSV telemetry."""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(REPO_ROOT, "presentation_charts")
os.makedirs(OUT_DIR, exist_ok=True)

TSK33_CSV = os.path.join(REPO_ROOT, "TSK33_ADAPTIVE_RESOURCE_POLICY", "TSK33_MEASUREMENT_RESULTS.csv")
TSK20_CSV = os.path.join(REPO_ROOT, "phase2_step1_microarchitecture_and_rtl", "TSK20_MEMORY_REPLAY_RESULTS.csv")

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.edgecolor": "#CBD5E1",
    "axes.linewidth": 0.9,
})


def make_sparsity_chart():
    df = pd.read_csv(TSK33_CSV)
    sub = df[(df["PE_Mode"] == "64-PE") & (df["Adaptive_Enabled"] == 0)]
    wls = ["WL1", "WL2", "WL3", "WL4"]
    labels = ["WL1\nResNet-18 C10\n(68.89% Sp.)", "WL2\nResNet-18 C100\n(66.57% Sp.)",
              "WL3\nVGG-16 C10\n(48.11% Sp.)", "WL4\nResNet-18 Deep\n(84.92% Sp.)"]
    dense_wt, sparse_wt, reds = [], [], []
    for wl in wls:
        d = int(sub[(sub["Workload_ID"] == wl) & (sub["Execution_Type"] == "Dense")]["Weight_SRAM_Reads"].iloc[0])
        s = int(sub[(sub["Workload_ID"] == wl) & (sub["Execution_Type"] == "Sparse")]["Weight_SRAM_Reads"].iloc[0])
        r = float(sub[(sub["Workload_ID"] == wl) & (sub["Execution_Type"] == "Sparse")]["Weight_SRAM_Reduction_Pct"].iloc[0])
        dense_wt.append(d / 1000.0)
        sparse_wt.append(s / 1000.0)
        reds.append(r)

    x = np.arange(len(wls))
    w = 0.36
    fig, ax = plt.subplots(figsize=(6.8, 4.3), dpi=300)
    b1 = ax.bar(x - w/2, dense_wt, w, label="Dense Weight SRAM Reads", color="#1E293B", edgecolor="#0F172A")
    b2 = ax.bar(x + w/2, sparse_wt, w, label="Sparse Zero-Gated Reads", color="#15803D", edgecolor="#14532D")

    for i in range(len(wls)):
        ax.text(x[i] - w/2, dense_wt[i] + 3.0, f"{dense_wt[i]*1000:,.0f}", ha="center", va="bottom",
                fontsize=8.5, fontweight="bold", color="#1E293B")
        ax.text(x[i] + w/2, sparse_wt[i] + 3.0, f"{sparse_wt[i]*1000:,.0f}\n(-{reds[i]:.2f}%)",
                ha="center", va="bottom", fontsize=8.5, fontweight="bold", color="#15803D")

    ax.set_ylabel("Weight SRAM Reads (Thousands of Words)", fontsize=10, fontweight="bold", color="#0F172A")
    ax.set_title("Weight Read Elimination via Zero-Gating (64-PE Mode)\nTotal Cycles Invariant at 9,569 Cycles (0.00% Jitter)",
                 fontsize=11, fontweight="bold", color="#800000", pad=10)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=9, fontweight="bold", color="#1E293B")
    ax.set_ylim(0, 198)
    ax.grid(axis="y", linestyle="--", alpha=0.5, color="#CBD5E1")
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(frameon=True, facecolor="white", edgecolor="#CBD5E1", fontsize=9, ncol=2, loc="upper center")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "chart_sparsity_weights.png"))
    plt.close(fig)


def make_scaling_tradeoff_chart():
    df = pd.read_csv(TSK33_CSV)
    # Show non-sparsity PE scaling: 64-PE vs 32-PE vs 16-PE (WL1 & WL4 Sparse)
    modes = ["64-PE\n(1 Pass)", "32-PE\n(2 Passes)", "16-PE\n(4 Passes)"]
    logic_saved = [0.0, 50.0, 75.0]
    act_increase = [0.0, 100.0, 300.0]

    # Exact WL1 sparse total accesses increase from CSV: 55344, 64560 (+16.65%), 82992 (+49.96%)
    # Exact WL4 sparse total accesses increase from CSV: 31712, 40928 (+29.06%), 59360 (+87.18%)
    wl4_tot_inc = []
    wl1_tot_inc = []
    for m_str in ["64-PE", "32-PE", "16-PE"]:
        v1 = int(df[(df["Workload_ID"] == "WL1") & (df["PE_Mode"] == m_str) & (df["Execution_Type"] == "Sparse") & (df["Adaptive_Enabled"] == 0)]["Total_SRAM_Accesses"].iloc[0])
        v4 = int(df[(df["Workload_ID"] == "WL4") & (df["PE_Mode"] == m_str) & (df["Execution_Type"] == "Sparse") & (df["Adaptive_Enabled"] == 0)]["Total_SRAM_Accesses"].iloc[0])
        wl1_tot_inc.append(v1)
        wl4_tot_inc.append(v4)
    wl4_pct = [((v - wl4_tot_inc[0]) / wl4_tot_inc[0]) * 100.0 for v in wl4_tot_inc]

    x = np.arange(3)
    w = 0.27
    fig, ax = plt.subplots(figsize=(6.8, 4.3), dpi=300)
    b1 = ax.bar(x - w, logic_saved, w, label="Active PE Logic Saved (%)", color="#1D4ED8", edgecolor="#1E3A8A")
    b2 = ax.bar(x, wl4_pct, w, label="Total SRAM Traffic Increase (WL4 %)", color="#B45309", edgecolor="#78350F")
    b3 = ax.bar(x + w, act_increase, w, label="Activation SRAM Read Inflation (%)", color="#800000", edgecolor="#4A0404")

    for bars, col in [(b1, "#1D4ED8"), (b2, "#B45309"), (b3, "#800000")]:
        for bar in bars:
            val = bar.get_height()
            lbl = f"+{val:.1f}%" if bars is not b1 and val > 0 else f"{val:.1f}%"
            ax.text(bar.get_x() + bar.get_width() / 2.0, val + 6.0, lbl,
                    ha="center", va="bottom", fontsize=8.3, fontweight="bold", color=col)

    ax.set_ylabel("Percentage vs. 64-PE Mode (%)", fontsize=10, fontweight="bold", color="#0F172A")
    ax.set_title("PE Scaling Trade-Off (From TSK33_MEASUREMENT_RESULTS.csv)\n"
                 "50%–75% Active PE Logic Reduction vs. Multi-Pass SRAM Traffic",
                 fontsize=10.5, fontweight="bold", color="#800000", pad=10)
    ax.set_xticks(x)
    ax.set_xticklabels(modes, fontsize=9.5, fontweight="bold", color="#1E293B")
    ax.set_ylim(0, 345)
    ax.grid(axis="y", linestyle="--", alpha=0.5, color="#CBD5E1")
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(frameon=True, facecolor="white", edgecolor="#CBD5E1", fontsize=8.5, loc="upper left")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "chart_scaling_tradeoff.png"))
    plt.close(fig)


def make_policy_distribution_chart():
    # Exact counts from TSK35B_POLICY_BENEFIT_REPORT.md (560 runs: 280 Policy A, 280 Policy B)
    cats = ["16-PE\n(75% Logic Saved)", "32-PE\n(50% Logic Saved)", "64-PE\n(Peak Speed)", "Blocked Safe Lock\n(P_max < 16)"]
    pol_a = [76, 52, 32, 120]
    pol_b = [40, 40, 80, 120]
    x = np.arange(len(cats))
    w = 0.36
    fig, ax = plt.subplots(figsize=(6.4, 4.1), dpi=300)
    b1 = ax.bar(x - w/2, pol_a, w, label="Policy A (Energy / Min PEs)", color="#800000")
    b2 = ax.bar(x + w/2, pol_b, w, label="Policy B (Max Speed / Min Cycles)", color="#0F766E")
    for bar, col in list(zip(b1, ["#800000"]*4)) + list(zip(b2, ["#0F766E"]*4)):
        val = int(bar.get_height())
        ax.text(bar.get_x() + bar.get_width()/2, val + 2.5, f"{val}\n({val/2.8:.1f}%)",
                ha="center", va="bottom", fontsize=8.3, fontweight="bold", color=col)
    ax.set_ylabel("Policy Decisions (Out of 280 Runs/Policy)", fontsize=9.5, fontweight="bold", color="#0F172A")
    ax.set_title("560 Dynamic Policy Decisions (TSK-35B Evaluation)\n100% Unsafe Requests Blocked | Optimal Policy Convergence",
                 fontsize=10.5, fontweight="bold", color="#0F172A", pad=10)
    ax.set_xticks(x)
    ax.set_xticklabels(cats, fontsize=8.8, fontweight="bold", color="#1E293B")
    ax.set_ylim(0, 148)
    ax.grid(axis="y", linestyle="--", alpha=0.5, color="#CBD5E1")
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(frameon=True, facecolor="white", edgecolor="#CBD5E1", fontsize=8.5, loc="upper left")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "chart_policy_distribution.png"))
    plt.close(fig)


if __name__ == "__main__":
    make_sparsity_chart()
    make_scaling_tradeoff_chart()
    make_policy_distribution_chart()
    print("[SUCCESS] Generated 3 presentation charts in", OUT_DIR)

# ==============================================================================
# Project: Neural_Acc — Activation-Sparse CNN Accelerator
# Task: TSK-36P Vivado Automated Synthesis, Implementation & Power Flow
# Description: Fully reproducible, parameterized non-project Tcl automation script
#              supporting both vectorless estimation and SAIF/VCD activity annotation.
# Usage:
#   vivado -mode batch -source vivado_run.tcl -tclargs <PART> <TOP> <VCD_FILE>
# Example:
#   vivado -mode batch -source vivado_run.tcl -tclargs xc7a100tcsg324-1 neural_acc_integrated_top none
# ==============================================================================

# ------------------------------------------------------------------------------
# 1. Parameter and Environment Configuration
# ------------------------------------------------------------------------------
set DEFAULT_PART "xc7a100tcsg324-1"
set DEFAULT_TOP  "neural_acc_integrated_top"
set DEFAULT_VCD  "none"

if {$argc >= 1} {
    set TARGET_PART [lindex $argv 0]
} else {
    set TARGET_PART $DEFAULT_PART
}

if {$argc >= 2} {
    set TOP_MODULE [lindex $argv 1]
} else {
    set TOP_MODULE $DEFAULT_TOP
}

if {$argc >= 3} {
    set VCD_ACTIVITY [lindex $argv 2]
} else {
    set VCD_ACTIVITY $DEFAULT_VCD
}

set SCRIPT_DIR [file normalize [file dirname [info script]]]
set REPO_ROOT  [file normalize [file join $SCRIPT_DIR ".."]]
set RTL_DIR    [file join $REPO_ROOT "phase2_step1_microarchitecture_and_rtl"]
set REPORT_DIR [file join $SCRIPT_DIR "reports"]

file mkdir $REPORT_DIR

puts "================================================================================"
puts "NEURAL_ACC VIVADO POWER & SYNTHESIS RUNNER"
puts "  Target Part       : $TARGET_PART"
puts "  Top Module        : $TOP_MODULE"
puts "  Activity File     : $VCD_ACTIVITY"
puts "  RTL Directory     : $RTL_DIR"
puts "  Report Directory  : $REPORT_DIR"
puts "================================================================================"

# ------------------------------------------------------------------------------
# 2. Read Synthesizable SystemVerilog Sources
# ------------------------------------------------------------------------------
puts "--- Reading SystemVerilog Design Files ---"
set RTL_FILES [list \
    [file join $RTL_DIR "mac_unit_40b.sv"] \
    [file join $RTL_DIR "pe_array_40b.sv"] \
    [file join $RTL_DIR "adaptive_pe_controller.sv"] \
    [file join $RTL_DIR "ping_pong_buffer_controller.sv"] \
    [file join $RTL_DIR "hybrid_sram_bank.sv"] \
    [file join $RTL_DIR "multibank_sram_subsystem.sv"] \
    [file join $RTL_DIR "dma_controller.sv"] \
    [file join $RTL_DIR "layer_command_sequencer.sv"] \
    [file join $RTL_DIR "dma_to_sram_write_adapter.sv"] \
    [file join $RTL_DIR "datapath_compute_feeder.sv"] \
    [file join $RTL_DIR "ofmap_drain_controller.sv"] \
    [file join $RTL_DIR "memory_telemetry_monitor.sv"] \
    [file join $RTL_DIR "channel_tile_controller.sv"] \
    [file join $RTL_DIR "requantization_unit.sv"] \
    [file join $RTL_DIR "neural_acc_integrated_top.sv"] \
]

foreach f $RTL_FILES {
    if {[file exists $f]} {
        read_verilog -sv $f
    } else {
        puts "ERROR: Source file not found: $f"
        exit 1
    }
}

# ------------------------------------------------------------------------------
# 3. Read Design Constraints (XDC)
# ------------------------------------------------------------------------------
set XDC_FILE [file join $RTL_DIR "timing_constraints.xdc"]
if {[file exists $XDC_FILE]} {
    puts "--- Reading Constraints: $XDC_FILE ---"
    read_xdc $XDC_FILE
} else {
    puts "WARNING: No timing_constraints.xdc found. Running unconstrained."
}

# ------------------------------------------------------------------------------
# 4. RTL Synthesis
# ------------------------------------------------------------------------------
puts "--- Running RTL Synthesis (synth_design) ---"
synth_design -top $TOP_MODULE -part $TARGET_PART -directive PerformanceOptimized

report_utilization -file [file join $REPORT_DIR "synth_utilization.rpt"]
report_timing_summary -file [file join $REPORT_DIR "synth_timing.rpt"]

# ------------------------------------------------------------------------------
# 5. Implementation (Opt, Place, PhysOpt, Route)
# ------------------------------------------------------------------------------
puts "--- Running Implementation (opt, place, phys_opt, route) ---"
opt_design -directive Explore
place_design -directive Explore
phys_opt_design -directive Explore
route_design -directive Explore

# ------------------------------------------------------------------------------
# 6. Post-Route Verification & Implementation Reports
# ------------------------------------------------------------------------------
puts "--- Generating Post-Route Utilization and Timing Reports ---"
report_utilization -file [file join $REPORT_DIR "post_route_utilization.rpt"] -hierarchical
report_timing_summary -file [file join $REPORT_DIR "post_route_timing.rpt"] -max_paths 10
report_clock_networks -file [file join $REPORT_DIR "post_route_clocks.rpt"]

# ------------------------------------------------------------------------------
# 7. Power Estimation (Activity-Annotated or Vectorless)
# ------------------------------------------------------------------------------
if {$VCD_ACTIVITY ne "none" && [file exists $VCD_ACTIVITY]} {
    puts "--- Annotating Switching Activity from VCD: $VCD_ACTIVITY ---"
    read_vcd -strip_path "$TOP_MODULE" $VCD_ACTIVITY
    set POWER_REPORT [file join $REPORT_DIR "post_route_power_activity.rpt"]
    report_power -file $POWER_REPORT -hierarchical -verbose
    puts "Activity-annotated power report generated: $POWER_REPORT"
} else {
    puts "--- Generating Default Vectorless Power Estimation ---"
    set POWER_REPORT [file join $REPORT_DIR "post_route_power_vectorless.rpt"]
    report_power -file $POWER_REPORT -hierarchical -verbose
    puts "Vectorless power report generated: $POWER_REPORT"
}

# ------------------------------------------------------------------------------
# 8. Checkpoint Export
# ------------------------------------------------------------------------------
set ROUTED_DCP [file join $REPORT_DIR "${TOP_MODULE}_routed.dcp"]
write_checkpoint -force $ROUTED_DCP
puts "Implementation checkpoint written: $ROUTED_DCP"

puts "================================================================================"
puts "Vivado Execution Finished Successfully!"
puts "================================================================================"


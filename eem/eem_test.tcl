::cisco::eem::event_register_syslog pattern "SYS-5-CONFIG"

namespace import ::cisco::eem::*
namespace import ::cisco::lib::*

# === Configuration ===
set filename "flash:interface_log.txt"
set timestamp [clock format [clock seconds] -format "%Y-%m-%d_%H-%M-%S"]

# === Extract the interface name from the syslog message ===
set intf ""
if {[regexp {Interface ([A-Za-z0-9/]+),} $_syslog_msg match intf]} {
    puts "Matched interface: $intf"
} else {
    set intf "unknown"
}

# === Open CLI ===
if [catch {cli_open} result] {
    error "Unable to open CLI: $result"
}
array set cli $result
cli_exec $cli(fd) "enable"

# === Run command ===
set cmd "show interface $intf"
set output [cli_exec $cli(fd) $cmd]

# === Clean up spaces, colons, and periods ===
set clean [regsub -all {[ :\.]} $output "_"]

# === Build a log entry ===
set log_entry "==== $timestamp: $intf ====\n$clean\n\n"

# === Write to file ===
if {[catch {set fp [open $filename a]} result]} {
    error "Unable to open file: $result"
}
puts $fp $log_entry
close $fp

# === Close CLI ===
cli_close $cli(fd)

# === Syslog confirmation ===
action_syslog msg "EEM policy saved output for $intf to $filename"


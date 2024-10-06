from bcc import BPF
import sys
import time

# Check if a process name was provided as an argument
if len(sys.argv) != 2:
    print("Usage: sudo python3 monitor_process.py <process_name>")
    sys.exit(1)

process_name = sys.argv[1]

# Define BPF program using the sys_enter_execve tracepoint
prog = f"""
#include <linux/sched.h>

// Tracepoint for sys_enter_execve
TRACEPOINT_PROBE(syscalls, sys_enter_execve) {{
    char comm[TASK_COMM_LEN];
    bpf_get_current_comm(&comm, sizeof(comm));

    // Check if the current process matches the specified process name
    if (strcmp(comm, "{process_name}") == 0) {{
        bpf_trace_printk("Process exec: %s\\n", comm);
    }}

    return 0;
}}
"""

# Load BPF program with error handling
try:
    b = BPF(text=prog)
except Exception as e:
    print("Failed to compile/load BPF program:")
    print(e)
    sys.exit(1)

# Header for output
print("{:<18} {:<16} {:<6} {}".format("TIME(s)", "COMM", "PID", "MESSAGE"))

# Read and print trace output
try:
    while True:
        # b.trace_print() will block and print the trace output as it comes
        # We'll use a non-blocking approach with a timeout
        try:
            (task, pid, cpu, flags, ts, msg) = b.trace_fields()
            timestamp = time.time()
            # Print only if the message contains the process name
            if process_name in msg:
                print("{:<18.9f} {:<16} {:<6} {}".format(
                    timestamp, 
                    process_name, 
                    pid, 
                    msg.strip()
                ))
        except ValueError:
            # Ignore parsing errors
            continue
except KeyboardInterrupt:
    print("\nExiting...")
    sys.exit(0)

#!/usr/bin/env python3

from bcc import BPF
import sys
from string import Template
import time

# BPF program to trace system calls
bpf_program = Template("""
#include <uapi/linux/ptrace.h>
#include <linux/sched.h>
#include <linux/string.h>

#define MAX_PROCESS_NAME_LEN 16

BPF_HASH(counter, u64, u64);

int trace_sys_open(struct pt_regs *ctx, const char __user *filename) {
    char comm[TASK_COMM_LEN];
    bpf_get_current_comm(&comm, sizeof(comm));

    // Compare the current process name with the target name passed from Python
    if (strncmp(comm, "$process_name", strlen("$process_name")) == 0) {
        u64 key = 0, *count, zero = 0;
        count = counter.lookup_or_init(&key, &zero);
        (*count)++;
        bpf_trace_printk("Open syscall invoked by process: %s\\n", comm);
        bpf_trace_printk("Opening file: %s\\n", filename);
    }
    return 0;
}

int trace_sys_write(struct pt_regs *ctx, const char __user *buf, size_t count) {
    char comm[TASK_COMM_LEN];
    bpf_get_current_comm(&comm, sizeof(comm));

    // Compare the current process name with the target name passed from Python
    if (strncmp(comm, "$process_name", strlen("$process_name")) == 0) {
        bpf_trace_printk("Write syscall invoked by process: %s\\n", comm);
    }
    return 0;
}
""")

def log_to_file(message, log_file="syscalls.log"):
    with open(log_file, "a") as f:
        f.write(message)

def main(target_process_name, max_logs=10):
    # Initialize BPF with safe formatting
    bpf_text = bpf_program.substitute(process_name=target_process_name)
    print("BPF Code:\n", bpf_text)  # Print the BPF code for debugging

    try:
        b = BPF(text=bpf_text)
        print("BPF module compiled successfully.")
    except Exception as e:
        print("Failed to compile BPF module:")
        print(str(e))  # Print the compilation error
        return

    # Attach kprobe to __x64_sys_open and __x64_sys_write
    try:
        print("Attaching kprobes...")
        b.attach_kprobe(event="__x64_sys_open", fn_name="trace_sys_open")
        b.attach_kprobe(event="__x64_sys_write", fn_name="trace_sys_write")
        print("Kprobes attached successfully.")
    except Exception as e:
        print(f"Error attaching kprobe: {str(e)}")
        return

    print(f"Tracing syscalls for process: {target_process_name} (up to {max_logs} logs)... Press Ctrl+C to stop.")

    # Set up to collect logs
    log_count = 0

    try:
        # Collect logs
        while log_count < max_logs:
            time.sleep(1)  # Sleep to avoid busy waiting
            b.trace_print()  # Print the trace logs to stdout

            # Log to the file
            log_to_file(f"System call entry logged for process: {target_process_name}\n")  # Adjust this message as needed

            # Increment log count when a log is received
            log_count += 1

    except KeyboardInterrupt:
        print("\nStopping tracing...")

    # Cleanup
    b.detach_kprobe(event="__x64_sys_open")
    b.detach_kprobe(event="__x64_sys_write")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: sudo python3 main.py <process_name>")
        sys.exit(1)

    target_process_name = sys.argv[1]
    main(target_process_name)

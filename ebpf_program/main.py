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
        bpf_trace_printk("Process ID: %d\\n", bpf_get_current_pid_tgid() >> 32);
    }
    return 0;
}

int trace_sys_write(struct pt_regs *ctx, const char __user *buf, size_t count) {
    char comm[TASK_COMM_LEN];
    bpf_get_current_comm(&comm, sizeof(comm));

    // Compare the current process name with the target name passed from Python
    if (strncmp(comm, "$process_name", strlen("$process_name")) == 0) {
        bpf_trace_printk("Write syscall invoked by process: %s\\n", comm);
        bpf_trace_printk("Process ID: %d\\n", bpf_get_current_pid_tgid() >> 32);
    }
    return 0;
}
""")

def main(target_process_name, max_logs=10):
    # Initialize BPF with safe formatting
    bpf_text = bpf_program.substitute(process_name=target_process_name)

    # Print the BPF code for debugging
    print("BPF Code:\n", bpf_text)

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

    log_count = 0

    try:
        while log_count < max_logs:
            # This will wait for events and print them
            print("Waiting for events...")
            b.trace_print()

            # Check if any trace has occurred and increment the log count accordingly
            log_count += 1
            time.sleep(1)  # Sleep to avoid busy waiting

    except KeyboardInterrupt:
        print("\nStopping tracing...")

    # Cleanup
    b.detach_kprobe(event="__x64_sys_open")
    b.detach_kprobe(event="__x64_sys_write")
    print(f"Stopped tracing syscalls for process: {target_process_name}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: sudo python3 main.py <process_name>")
        sys.exit(1)

    target_process_name = sys.argv[1]
    main(target_process_name)

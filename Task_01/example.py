from bcc import BPF
import sys

# BPF program to trace syscalls
bpf_program = """
#include <linux/sched.h>
#include <linux/ptrace.h>
#include <linux/uio.h>
#include <uapi/linux/ptrace.h>

// BPF Hash for tracking syscall entry
BPF_HASH(start, u32);

int trace_syscalls(struct pt_regs *ctx, const char __user *filename) {
    u32 pid = bpf_get_current_pid_tgid() >> 32;

    // Check if the process name is 'ansar'
    char comm[TASK_COMM_LEN];
    bpf_get_current_comm(&comm, sizeof(comm));

    // Compare the process name with "ansar"
    if (comm[0] != 0 && bpf_strncmp(comm, "ansar", sizeof(comm)) == 0) {
        bpf_trace_printk("Process ansar invoked syscall: %s\\n", filename);
    }
    
    return 0;
}
"""

# Load the BPF program
b = BPF(text=bpf_program)

# Attach the trace to the syscall handler for execve
try:
    b.attach_kprobe(event="sys_execve", fn_name="trace_syscalls")
except Exception as e:
    print(f"Error attaching kprobe: {str(e)}")
    sys.exit(1)

print("Tracing syscalls for process 'ansar'... Press Ctrl+C to stop.")

# Print the output from the BPF trace
try:
    b.trace_print(fmt="{5}")
except KeyboardInterrupt:
    print("Detaching...")

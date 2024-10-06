Here's the updated `README.md` with the additional challenge:

---

# Assessment Task

This repository contains two tasks that demonstrate the use of eBPF in Python for system call monitoring and a doubly linked list implementation in C. These tasks showcase system-level programming with eBPF and fundamental data structures in C.

## Directory Structure

```bash
Assessment_task/
├── ebpf_program/
│   ├── main.py         # Python program to trace syscalls using eBPF
│   ├── test.c          # C program that triggers syscalls for testing
│   ├── example.py      # Another example BPF program (if any)
└── Task_02/
    └── linked_list.c   # C program implementing a doubly linked list
```

---

## Task 1: eBPF Program to Monitor System Calls

This task involves creating an eBPF program that monitors and logs system calls made by a process whose name is provided as a command-line argument. It was implemented using **BCC** in Python.

### Steps to Execute

1. **Install required dependencies**:
   - Install BCC (BPF Compiler Collection):
     ```bash
     sudo apt-get install bpfcc-tools linux-headers-$(uname -r) bpfcc-dev
     pip3 install bcc
     ```

2. **Compile and run the C test program**:
   - Navigate to the `ebpf_program/` directory and compile `test.c`:
     ```bash
     gcc -o test test.c
     ./test <your_name>
     ```

3. **Run the Python eBPF program**:
   - Ensure the `main.py` program is executable:
     ```bash
     sudo python3 main.py <your_name>
     ```

4. **Output**: The program logs `open` and `write` syscalls made by processes containing your name.

### Libraries/Resources Used

- **BCC (BPF Compiler Collection)**: The core library used to write and run eBPF programs.
- **Python**: Used to orchestrate the BPF program.
- **C Standard Library**: For the C program that triggers system calls.

### Challenges Encountered

- **Installing build tools for BCC**: I tried multiple environments, including **WSL**, **VMware**, and **dual boot** setups, to get the necessary build tools for BCC running properly. Each environment had its own issues with dependencies and kernel version compatibility.
- **Attaching kprobes**: Attaching the probes to the correct system calls like `__x64_sys_open` and `__x64_sys_write` was tricky due to variations in system call names across different kernel versions.
- **Real-time event tracing**: Managing the `b.trace_print()` loop to capture and display syscalls correctly required adjusting sleep times and loop conditions.

### Additional Features

- The eBPF program tracks system calls for any process based on a provided name, making it flexible for monitoring different processes.

---

## Task 2: Doubly Linked List Implementation in C

This task involves implementing a **doubly linked list** in C, where each node stores a user-provided name and a unique identifier (ID). The list supports insertion, deletion, and sorting operations.

### Steps to Execute

1. **Compile and run the linked list program**:
   - Navigate to the `Task_02/` directory and compile `linked_list.c`:
     ```bash
     gcc -o linked_list linked_list.c
     ./linked_list
     ```

2. **Input your name**: The program will prompt for your name and perform the operations based on the ID provided.

### Libraries/Resources Used

- **C Standard Library**: Used for file handling, memory management, and standard I/O operations.

### Challenges Encountered

- **Memory management**: Handling dynamic memory allocation and deallocation to avoid memory leaks.
- **Sorting**: Implementing the sorting operation efficiently using doubly linked pointers.

### Additional Features

- **Sorting functionality**: The list can be sorted based on the unique identifier, demonstrating flexibility in list manipulation.

---

## Conclusion

This project demonstrates both system-level monitoring using eBPF and a basic data structure implementation in C. The eBPF program is a powerful tool for process monitoring, while the linked list showcases fundamental operations in data structures.

--- 


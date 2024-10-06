
# Assessment Task

This repository contains two tasks demonstrating system-level programming using **eBPF** in Python for system call monitoring and a **doubly linked list** implementation in C. Both tasks aim to showcase practical skills in working with low-level systems and data structures.

---

## Directory Structure

```bash
Assessment_task/
├── Task_01/
│   ├── ebpf.py         # Python program to trace syscalls using eBPF
│   ├── test.c          # C program that triggers syscalls for testing
│   └── example.py      # (Optional) Another example of BPF program
└── Task_02/
    └── linked_list.c   # C program implementing a doubly linked list
```

---

## Task 1: eBPF Program to Monitor System Calls

This task involves creating an **eBPF** program that monitors and logs system calls made by a process whose name is passed as a command-line argument. The program is built using **BCC** (BPF Compiler Collection) in Python and captures the `open` and `write` syscalls for the target process.

### Key Features

- Dynamically monitors system calls (`open` and `write`) for any process based on the process name.
- Flexible for monitoring multiple processes.
- Real-time logging of syscalls, including details like file access and process IDs.

### Steps to Execute

1. **Install Dependencies**:
   - Install BCC and necessary kernel headers:
     ```bash
     sudo apt-get install bpfcc-tools linux-headers-$(uname -r) bpfcc-dev
     pip3 install bcc
     ```

2. **Compile and Run Test Program**:
   - Navigate to `Task_01/` directory and compile `test.c`:
     ```bash
     gcc -o test test.c
     ./test <process_name>
     ```

3. **Run the Python eBPF Program**:
   - Execute the Python script, providing the target process name:
     ```bash
     sudo python3 ebpf.py <process_name>
     ```

4. **Output**:
   - The program will log system calls like:
     ```bash
     Open syscall invoked by process: <process_name>
     Opening file: <filename>
     Process ID: <PID>
     ```

### Libraries/Resources Used

- **BCC**: Core library for eBPF programs.
- **Python**: Used to manage and attach probes for syscall tracing.
- **C Standard Library**: Used to simulate syscalls in the test program.

### Challenges Encountered

- **Installing BCC**: Various environments (WSL, VMware, dual boot) presented unique challenges in setting up the required kernel dependencies and build tools.
- **Kernel Compatibility**: Different Linux kernel versions have varying syscall names, which required careful probe attachment.
- **Real-time Event Handling**: Managing real-time system event streams and ensuring efficient log collection.

---

## Task 2: Doubly Linked List Implementation in C

This task involves implementing a **doubly linked list** in C, where each node stores a student's **name** and **ID**. The program supports essential operations like **insertion**, **deletion**, and **sorting** of nodes based on the student ID.

### Key Features

- Insertion at the head of the list.
- Display of the list in order.
- Deletion of nodes by student ID.
- Sorting the list by student ID using **bubble sort**.

### Steps to Execute

1. **Compile and Run the Linked List Program**:
   - Navigate to `Task_02/` directory and compile the `linked_list.c` file:
     ```bash
     gcc -o linked_list linked_list.c
     ./linked_list
     ```

2. **Input Data**:
   - The program prompts the user to input student details (name and ID) and performs operations like insertion, sorting, and deletion.

3. **Output**:
   - Displays the list before and after sorting, and after removing a specified node by ID.

### Libraries/Resources Used

- **C Standard Library**: Utilized for file handling, dynamic memory allocation, and I/O operations.

### Challenges Encountered

- **Memory Management**: Ensuring proper memory allocation and deallocation to avoid memory leaks.
- **Sorting**: Implementing bubble sort for the doubly linked list, ensuring data consistency while swapping node data.

---

## Conclusion

This project demonstrates a blend of system-level programming and fundamental data structure implementation. The **eBPF** task highlights efficient syscall monitoring, crucial for low-level debugging and tracing. Meanwhile, the **doubly linked list** task illustrates core data structure operations that are essential in various computing problems.

---


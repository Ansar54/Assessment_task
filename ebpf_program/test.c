#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <linux/stat.h>
#include <sys/stat.h>

int main(int argc, char *argv[]) {
    printf("Running process with name: %s\n", argv[1]);

    // Open a file to trigger a system call
    int fd = open("testfile.txt", O_CREAT | O_WRONLY | O_TRUNC, S_IRUSR | S_IWUSR);
    if (fd < 0) {
        perror("Error opening file");
        return 1;
    }

    for (int i = 1; i <= 5; i++) {
        printf("Process %s is doing some work... (%d)\n", argv[1], i);
        write(fd, "Hello, World!\n", 15);  // Writing to the file (system call)
        sleep(10);  // Simulate some work
    }

    close(fd);  // Close the file
    printf("Process %s completed its work.\n", argv[1]);
    return 0;
}


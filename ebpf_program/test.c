#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <linux/stat.h>
#include <sys/stat.h>

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <your_name>\n", argv[0]);
        return 1;
    }
    char *name = argv[1];
    printf("Running process with name: %s\n", name);

    // Open a file to trigger a system call
    int fd = open("testfile.txt", O_CREAT | O_WRONLY | O_TRUNC, S_IRUSR | S_IWUSR);
    if (fd < 0) {
        perror("Error opening file");
        return 1;
    }

    for (int i = 1; i <= 5; i++) {
        printf("Process %s is doing some work... (%d)\n", name, i);
        write(fd, "Hello, World!\n", 15);  // Writing to the file (system call)
        sleep(5);  // Simulate some work
    }

    close(fd);  // Close the file
    printf("Process %s completed its work.\n", name);
    return 0;
}

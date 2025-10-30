#include <stdio.h>
#include <iostream>

int main() {
    // This will trigger cpplint whitespace/style issues
    std::cout << "Hello, world!" << std::endl; 
    printf("bad style\n");
    return 0;
}

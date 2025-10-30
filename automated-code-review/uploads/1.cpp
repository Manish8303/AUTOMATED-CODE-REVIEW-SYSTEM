#include <iostream>
using namespace std;

int main() {
    int a, b;
    cout << "Enter two numbers: ";
    cin >> a >> b;

    // Suspicious assignment instead of comparison
    if (a = b) {  
        cout << "Numbers are equal" << endl;
    } else {
        cout << "Numbers are not equal" << endl;
    }

    // Memory leak
    int* ptr = new int[5];
    ptr[0] = 10;

    // Unused variable
    int unusedVar = 42;

    return 0;
}

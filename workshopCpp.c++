// Your First C++ Program

#include <iostream>
#include <stdlib.h>
using namespace std;

void troca_ab(int *p1, int *p2) {
    int temp = *p1;
    *p1 = *p2;
    *p2 = temp;

    return;
}

int main() {
    int a, b;
    a = 0;
    b = 1;
    cout << "a = " << a << " b = " << b << endl;
    troca_ab( &a, &b );
    cout << "a = " << a << " b = " << b << endl;

    return 0;
}

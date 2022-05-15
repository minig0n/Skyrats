// Your First C++ Program

#include <iostream>
using namespace std;
float area_triangulo(float b, float h);

int main() {
    float base, altura;
    cout << "Insira o tamanho da base: ";
    cin >> base;
    cout << "Insira o tamanho da altura: ";
    cin >> altura;
    cout << "Area: " << area_triangulo(base, altura) << endl;
    return 0;
}

float area_triangulo(float b, float h){
    return b * h / 2;
}

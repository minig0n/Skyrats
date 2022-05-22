#include <iostream>
#include <stdlib.h>
#include <cmath>
using namespace std;

void choose_environment(string *environment, string *tra, int *speed, int *height){
    int random_number;
    random_number = rand() % 3;

    if (random_number == 0){
        *environment = "Floresta";
        *tra = "Curva";
        *speed = 8;
        *height = 3;
    }
    if (random_number == 1){
        *environment = "Cidade";
        *tra = "Manhatan";
        *speed = 8;
        *height = 3;
    }
    if (random_number == 2){
        *environment = "Deserto";
        *tra = "Retilínea";
        *speed = 8;
        *height = 3;
    }
}

void change_position(string *name, string *tra, int *speed, float *x_init, float *y_init, float *x_goal, float *y_goal) {
    int i, n;
    float dt;
    float dx, dy, d;
    float x, y;

    dx = *x_goal - *x_init;
    dy = *y_goal - *y_init;
    d = sqrt(pow(dx, 2) + pow(dy,2));
    dt = 1;
    x = *x_init;
    y = *y_init;

    if (*tra == "Retilínea"){
        n = d / (*speed * dt);
        for (i = 0; i <= n; i++){
            cout << *name << " em ("<< ceil(x * 100.0)/100.0 << ", " << ceil(y * 100.0)/100.0 << ")" << endl;
            x = x + *speed * dt * dx/d;
            y = y + *speed * dt * dy/d;
        }
    }

    else if (*tra == "Curva"){
        float raio;
        float delta, phi;
        raio = d/2;
        n = 3.1416 * raio / (*speed * dt);
        delta = 3.1416 / n;
        phi = delta;
        for (i = 0; i < n; i++){
            cout << *name << " em (" << ceil(x * 100.0)/100.0 << ", " << ceil(y * 100.0)/100.0 << ")" << endl;
            x = *x_init + (dx/d * (1 - cos(phi)) + dy/d * sin(phi)) * raio;
            y = *y_init - (dy/d * (cos(phi) - 1) + dx/d * sin(phi)) * raio;
            phi = phi + delta;
        }
    }

    else {
        n = abs(dx) / (*speed * dt);
        for (i = 0; i <= n; i++){
            cout << *name << " em (" << ceil(x * 100.0)/100.0 << ", " << ceil(y * 100.0)/100.0 << ")" << endl;
            if (dx >= 0){
                x = x + *speed * dt;
            }
            else{
                x = x - *speed * dt;
            }
        }
        x = *x_goal;
        n = abs(dy) / (*speed * dt);
        for (i = 0; i <= n; i++){
            cout << *name << " em (" << ceil(x * 100.0)/100.0 << ", " << ceil(y * 100.0)/100.0 << ")" << endl;
            if (dy >= 0){
                y = y + *speed * dt;
            }
            else {
                y = y - *speed * dt;
            }
        }
    }
    x = *x_goal;
    y = *y_goal;
    cout << *name << " em (" << ceil(x * 100.0)/100.0 << ", " << ceil(y * 100.0)/100.0 << ")" << endl;
    return;
}

int main(){
    char nova_entrega;
    bool end = false;
    string name, environment, tra;
    int height, speed;
    float x_init, y_init, x_goal, y_goal;

    cout << "Bem vindo ao simulador de Package Delivery!" << endl;
    cout << "Qual drone voaremos hoje? ";
    cin >> name;
    cout << "Qual sua posição em x e y, respectivamente?" << endl;
    cin >> x_init;
    cin >> y_init;

    while (end == false){
        cout << "Qual o local de entrega em x e y, respectivamente?" << endl;
        cin >> x_goal;
        cin >> y_goal;

        choose_environment( &environment, &tra, &speed, &height );
        cout << "O ambiente é: " << environment << endl;
        cout << name << " armado com sucesso!" << endl;
        cout << "Altura de " << height << " metros atingida!" << endl;

        change_position( &name, &tra, &speed, &x_init, &y_init, &x_goal, &y_goal );
        cout << "O drone chegou ao destino!" << endl;

        cout << "Gostaria de realizar outra entrega? (s/n) ";
        cin >> nova_entrega;
        if (nova_entrega == 'n'){
            cout << "Obrigado por voar com a SkyRats! \n" << endl;
            end = true;
        }
        x_init = x_goal;
        y_init = y_goal;
    }
    return 0;
}

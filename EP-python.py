import random
import turtle
from turtle import Screen, Turtle, left
import time
import math
import numpy

# Padrões da tela
SCREEN_SIZE = 800
METRO = 4           # 1m = 2px
DOTSIZE1 = 5        # Pontos de trajetória
DOTSIZE2 = 10       # Início/Fim

# Configurações da Simulação
PASSO = 0.5         # Menor passo -> mais pontos
PARADA = 5          # Quanto antes o drone diminui a velocidade antes da curva

# Condições do ambiente (Nome, Velocidade, Altura):
FLORESTA = ["Floresta", 5, 5]
CIDADE = ["Cidade", [3, 5], [9, 10]]
DESERTO = ["Deserto", 8, 3]

class Drone(Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()

        # Inputs
        self.nome = input("Qual Drone voaremos hoje? ")
        self.x_init = float(input("Posição inicial em x: ")) * METRO
        self.y_init = float(input("Posição inicial em y: ")) * METRO

        # Escreve o nome do Drone
        self.penup()
        self.goto(-150,350)
        self.pendown()
        self.write(f"Drone Selecionado: {self.nome}", font="Verdana", align="right")
        self.penup()

        # Desenha ponto inicial
        self.penup()
        self.goto(self.x_init, self.y_init)
        self.pendown()
        self.dot(DOTSIZE2, "red")
        self.penup()

        # Desenha ponto final da primeira trajetória
        self.final_position()

        # Configura o x e y iniciais
        self.x = self.x_init
        self.y = self.y_init
        self.goto(self.x, self.y)

    def final_position(self):
        self.x_goal = float(input("Posição final em x: ")) * METRO
        self.y_goal = float(input("Posição final em y: ")) * METRO
        self.delta_x = (self.x_goal - self.x_init)
        self.delta_y = (self.y_goal - self.y_init)

        # Desenha ponto final de qualquer trajetória
        self.penup()
        self.goto(self.x_goal, self.y_goal)
        self.pendown()
        self.dot(DOTSIZE2, "red")
        self.penup()

    def choose_enviroment(self):
        # Sorteia o Ambiente
        self.sorteio = random.randint(1,3)
        if self.sorteio == 1:
            self.ambiente = FLORESTA
        elif self.sorteio == 2:
            self.ambiente = CIDADE
        else:
            self.ambiente = DESERTO

        print(f"O ambiente é: {self.ambiente[0]}")

    def arm_drone(self):
        # Função que arma o drone para decolagem
        print(f"{self.nome} armado com sucesso!")
        time.sleep(1)
        if self.sorteio == 2:
            print(f"Altura de {self.ambiente[2][1]}m atingida.")
        else:
            print(f"Altura de {self.ambiente[2]}m atingida.")

    def trajetoria(self):
        self.dist = (self.delta_x**2 + self.delta_y**2)**(1/2)
        self.cosseno = self.delta_x / self.dist
        self.seno = self.delta_y / self.dist

        # Na Floresta
        if self.sorteio == 1:
            self.vel = self.ambiente[1]
            print(f"A velocidade do drone é: {self.vel}m/s.")
            self.raio = self.dist / 2
            self.delta_theta = (self.vel*METRO) * PASSO / self.raio
            self.num_pontos = int(3.1415 // (self.delta_theta))
            self.phi = self.delta_theta
            return self.num_pontos

        # Na Cidade
        elif self.sorteio == 2:
            self.vel1 = self.ambiente[1][1]
            self.vel2 = self.ambiente[1][0]
            print(f"A velocidade do drone é: {self.vel1}m/s na reta e {self.vel2}m/s na curva.")

            self.passo1 = self.vel1*METRO*PASSO
            self.passo2 = self.vel2*METRO*PASSO
            self.sinal_x = numpy.sign(self.delta_x)
            self.sinal_y = numpy.sign(self.delta_y)

            self.num_pontos_x = int((abs(self.delta_x) - PARADA*self.passo1)// self.passo1) + int((PARADA*self.passo1)// self.passo2)
            self.num_pontos_y = int(abs(self.delta_y) // self.passo1) - 1
            return (self.num_pontos_x + self.num_pontos_y)

        # No Deserto
        else:
            self.vel = self.ambiente[1]
            print(f"A velocidade do drone é: {self.vel}m/s")
            self.num_pontos = int(self.dist // (self.vel*METRO*PASSO))
            return self.num_pontos

    def move_drone(self):
        # Na Floresta
        if self.sorteio == 1:
            self.x = self.x_init + self.raio * (self.cosseno * (1 - math.cos(self.phi)) + self.seno * math.sin(self.phi))
            self.y = self.y_init - self.raio * (self.seno * (math.cos(self.phi) - 1) + self.cosseno * math.sin(self.phi))
            self.goto(self.x, self.y)
            self.pendown()
            self.dot(DOTSIZE1, "green")
            self.penup()
            self.phi += self.delta_theta

        # Na Cidade
        elif self.sorteio == 2:
            self.dist_x = abs(self.x_goal - self.x)
            # Início
            if self.dist_x >= PARADA * self.passo1:
                self.x += self.sinal_x * self.passo1
            # Antes da curva
            elif PARADA*self.passo1 > self.dist_x >= self.passo2:
                self.x += self.sinal_x * self.passo2
            # Depois da curva
            else:
                self.y += self.sinal_y * self.passo1

            self.goto(self.x, self.y)
            self.pendown()
            self.dot(DOTSIZE1, "gray")
            self.penup()

        # No Deserto
        else:
            self.x += (self.vel*METRO) * PASSO * self.cosseno
            self.y += (self.vel*METRO) * PASSO * self.seno
            self.goto(self.x, self.y)
            self.pendown()
            self.dot(DOTSIZE1, "orange")
            self.penup()

        print(f"{self.nome} está em: ({round(self.x/METRO, 2)}, {round(self.y/METRO, 2)})")

    def nova_entrega(self):
        # Reseta os parâmetros de posição para nova entrega
        self.x_init = self.x_goal
        self.y_init = self.y_goal
        self.x = self.x_init
        self.y = self.y_init
        self.final_position()

def main():
    # Boas Vindas
    print("Bem vindo ao simulador de package Delivery!")

    # Inicialização da Tela
    screen = turtle.Screen()
    screen.setup(height=SCREEN_SIZE, width=SCREEN_SIZE)
    screen.tracer(0)
    screen.bgcolor("white")
    screen.title("Package Delivery Simulator")

    # Inicialização do Drone
    drone = Drone()
    time.sleep(2)

    terminou = False
    while not terminou:
        drone.choose_enviroment()
        time.sleep(1)

        drone.arm_drone()
        time.sleep(1)

        num_pontos = drone.trajetoria()
        time.sleep(1)

        i = 0
        chegou = False
        while not chegou:
            if i == num_pontos:
                chegou = True
            else:
                screen.update()
                time.sleep(PASSO)
                drone.move_drone()
                i += 1

        print("O drone chegou ao destino!")
        novo_delivery = input("Deseja fazer uma nova entrega? (S/N) ")
        if novo_delivery == "N":
            terminou = True
        else:
            drone.nova_entrega()

    print("\nObrigado por voar com a SkyRats! ʕ•́ᴥ•̀ʔっ\n")
    screen.bye()

if __name__ == "__main__":
    main()
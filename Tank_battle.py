import pygame
import sys
import math

# Inicializando pygame
pygame.init()

# Configurando janela
width, height = 1000, 700 #passando os valores das dimensões da janela para as variaveis width e height.
window = pygame.display.set_mode((width, height)) #configurando a janela
pygame.display.set_caption("Tank Battle Game") # passa o titulo que será exibido na janela

# Cores
#definindo as cores preta e vermelha.
black = (0, 0, 0)
red = (255, 0, 0)

# Tanques
class Tank: # Criando a classe tanque.
    def __init__(self, x, y, up_key, down_key, left_key, right_key):
        self.rect = pygame.Rect(x, y, 50, 50) # Rect é uma classe do pygames que
        self.health = 24 #aqui passamos a vida do tanque para 24
        self.direction = 0  # 0 para direita, 90 para cima, 180 para a esquerda, 270 para baixo.
        #criando variaveis de movimento
        self.up_key = up_key
        self.down_key = down_key
        self.left_key = left_key
        self.right_key = right_key

    def move(self, keys):
        speed = 3 #passando a velocidade desejada do tanque para a variavel speed
        #referencia para as direções  0 para direita, 90 para cima, 180 para a esquerda, 270 para baixo.
        if keys[self.up_key] and self.rect.y > 0:
            self.rect.y -= speed
            self.direction = 90
        if keys[self.down_key] and self.rect.y < height - self.rect.height:
            self.rect.y += speed
            self.direction = 270
        if keys[self.left_key] and self.rect.x > 0:
            self.rect.x -= speed
            self.direction = 180
        if keys[self.right_key] and self.rect.x < width - self.rect.width:
            self.rect.x += speed
            self.direction = 0

    def draw_healthbar(self):
        pygame.draw.rect(window, red, (self.rect.x, self.rect.y - 20, self.health * 2, 10))  #criação da barra de vida como uma janela com seu tamanho baseado no valor da variavel health

# Bullets
class Bullet:
    def __init__(self, x, y, direction):  #recebe prosições e sua direção.
        self.rect = pygame.Rect(x, y, 5, 5) #aqui passamos a posição e o tamanho do objeto bullet
        self.direction = direction  # 0 para direita, 90 para cima, 180 para a esquerda, 270 para baixo

    #metodo de movimento
    def move(self):
        speed = 8 #variavel para velociadade
        angle = math.radians(self.direction) #convertemos o valor da direção para um angulo
        self.rect.x += speed * math.cos(angle) # Usando coseno e seno para calcular o componete horizontal e vertical
        self.rect.y -= speed * math.sin(angle)

# Instancias dos tanques
# Passando os parametros de posição e teclas de movimentação para o objeto.
tank1 = Tank(x=50, y=100, up_key=pygame.K_w, down_key=pygame.K_s, left_key=pygame.K_a, right_key=pygame.K_d)
tank2 = Tank(x=900, y=600, up_key=pygame.K_i, down_key=pygame.K_k, left_key=pygame.K_j, right_key=pygame.K_l)

#criação de vetores que guardarão os objetos bala (bullet)
bullets1 = []
bullets2 = []

# Especificando o tamanho da fonte
font = pygame.font.Font(None, 32)

def draw_healthbars():
    #chamando os metodos de barra de vida
    tank1.draw_healthbar()
    tank2.draw_healthbar()

def reset_game():
    #metodo para reiniciar o jogo, rescrevendo os valores das variaveis abaixo, tanks recuperam a vida anterior e voltam a suas respectivas posições
    tank1.rect.x, tank1.rect.y = 50, 100
    tank2.rect.x, tank2.rect.y = 900, 600
    tank1.health = 24
    tank2.health = 24
    bullets1.clear()
    bullets2.clear()

# Loop do jogo
while True:
    for event in pygame.event.get():

        # condicional para a reiniar o jogo ao apertar "R"
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            reset_game()

        # Condicional para sair do jogo ao apertar "Q" (Quit)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            pygame.quit()
            sys.exit()

        #condicional para travar o jogo apos a destruição de um tank
        if tank1.health <= 0 or tank2.health <= 0:
            continue

        keys1 = pygame.key.get_pressed()
        keys2 = pygame.key.get_pressed()

        # Configurando o disparo do tanque 1
        tank1.move(keys1)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: #atribuindo a tecla de espaço para disparar as balas, (criar objetos bullets,)
            bullet = Bullet(tank1.rect.x + tank1.rect.width // 2, tank1.rect.y + tank1.rect.height // 2, tank1.direction) #recebendo os atributos nescessarios para o contrutor (x,y,direção)
            bullets1.append(bullet) # atribuindo as balas para o vetor do tanque 1

        # Tank 2 controls
        tank2.move(keys2)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN: #atribuindo a tecla enter para disparar as balas, (criar objetos bullets,)
            bullet = Bullet(tank2.rect.x + tank2.rect.width // 2, tank2.rect.y + tank2.rect.height // 2, tank2.direction) #recebendo os atributos nescessarios para o contrutor (x,y,direção)
            bullets2.append(bullet) # atribuindo as balas para o vetor do tanque 1

    # Loop para movimentação das balas (bullets)
    for bullet in bullets1:
        bullet.move()
    for bullet in bullets2:
        bullet.move()

    #verifica colisões usando o medoto coolliderect da Classe React da biblioteca pygame
    for bullet in bullets1:
        if tank2.rect.colliderect(bullet.rect) and tank2.health > 0 :
            tank2.health -= 3 # valor do dano
            bullets1.remove(bullet)

    # verifica colisões usando o medoto coolliderect da Classe React da biblioteca pygame
    for bullet in bullets2:
        if tank1.rect.colliderect(bullet.rect) and tank1.health > 0 :
            tank1.health -= 3 # valor do dano
            bullets2.remove(bullet)

    # Subindo as imagens
    window.blit(pygame.image.load("terrain.png"), (0, 0)) #Imagem de background
    window.blit(pygame.transform.rotate(pygame.image.load("tank1.png"), tank1.direction), tank1.rect.topleft) #passando a imagem para o tanque, usando o metodo rotate,
    window.blit(pygame.transform.rotate(pygame.image.load("tank2.png"), tank2.direction), tank2.rect.topleft) #que recebera uma superficie e uma direção.
                                                                                                              # o metodo blit ira sobrepor uma imagem a outra

    for bullet in bullets1:
        pygame.draw.rect(window, black, bullet.rect) # As balas serão desenhadas como um retangulo
    for bullet in bullets2:
        pygame.draw.rect(window, black, bullet.rect)

    draw_healthbars() #chamada do metodo da barra de vida

    # contagem de vida
    text = font.render(f"Tank 1 Health: {tank1.health}", True, black) #criando string para exibir a contagem da vida
    window.blit(text, (10, 10)) #usa medotodo blit para fazer a sobreposicao
    text = font.render(f"Tank 2 Health: {tank2.health}", True, black)
    window.blit(text, (width - 200, 10))

    # Verifica se o jogo terminou
    if tank1.health <= 0 or tank2.health <= 0:
        winner = "Tank 1" if tank2.health <= 0 else "Tank 2"
        text = font.render(f"{winner} vitoria! Aperte 'R' para reiniciar ou 'Q' para Sair.", True, black)
        window.blit(text, (width // 2 - 250, height // 2 - 50))

    pygame.display.flip() # atualiza o frame para exibição da mensagem

    # define o frame rate
    pygame.time.Clock().tick(30)

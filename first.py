import pygame
import sys

ancho = 645
alto = 489
color_azul = (0,0, 64)

class Bolita(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__
        #Load image
        self.image = pygame.image.load('*****bolita.png')
        # Obtain square
        self.rect = self.image.get_rect()
        # Ball position
        self.rect.centerx = ancho /2
        self.rect.centery = alto /2
        # Speed
        self.speed = [12, 12]

    def update(self):
        # Limit ball movement
        if self.rect.bottom >= alto or self.rect.top <= 0:
            self.speed[1] = -self.speed[1]
        if self.rect.right >= ancho or self.rect.left <= 0:
            self.speed[0] = -self.speed[0]
        # Movement
        self.rect.move_ip(self.speed)


class Paleta(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__
        #Load image
        self.image = pygame.image.load('*******paleta.png')
        # Obtain square
        self.rect = self.image.get_rect()
        # Paleta position X
        self.rect.midbottom = (ancho /2, alto-20)
        # Speed
        self.speed = [0, 0]
    
    def update(self, evento):
        # Player position

        if evento.key == pygame.K_RIGHT and self.rect.right > 0:
            self.speed = [30, 0]
        elif evento.key == pygame.K_LEFT and self.rect.left > 0:
            self.speed = [-30, 0]
        else:
            self.speed = [0,0]
         # Movement
        self.rect.move_ip(self.speed)

class Ladrillo(pygame.sprite.Sprite):
    def __init__(self, posicion):
        pygame.sprite.Sprite.__init__(self)
        #Load image
        self.image = pygame.image.load('*****ladrillo.png')
        # Obtain square
        self.rect = self.image.get_rect()
        # Initial position 
        self.rect.topleft= posicion

class Muro(pygame.sprite.Group):
    def __init__(self,cantidadladrillos):
        pygame.sprite.Group.__init__(self)

        pos_x = 0
        pos_y = 20
        for i in range(cantidadladrillos):
            ladrillo= Ladrillo((pos_x, pos_y))
            self.add(ladrillo)
            pos_x += ladrillo.rect.width
            if  pos_x >= ancho:
                pos_x = 0
                pos_y += ladrillo.rect.height

# Screen
pantalla = pygame.display.set_mode((ancho, alto))
# Screen caption
pygame.display.set_caption("Brick game")
# Watch
reloj = pygame.time.Clock()
# Set press key
pygame.key.set_repeat(30)

bolita= Bolita()
jugador= Paleta()
muro= Muro(50)

# Keep game-window working
while True:
    # Deploy FPS
    reloj.tick(60)
    # Events check
    for evento in pygame.event.get():
        # Close game window
        if evento.type == pygame.QUIT:
            sys.exit()
        # Keyboard events
        elif evento.type == pygame.KEYDOWN:
            jugador.update(evento)

    # Ball update
    bolita.update()

    # Colision ball vs player
    if pygame.sprite.collide_rect(bolita, jugador):
        bolita.speed[1] = -bolita.speed[1]
    # Colision ball vs brick
    lista= pygame.sprite.spritecollide(bolita, muro, False)
    if lista:
        ladrillo = lista[0]
        cx= bolita.rect.centerx
        if cx < ladrillo.rect.left or ladrillo.rect.right:
            bolita.speed[0] = -bolita.speed[0]
        else:
            bolita.speed[1] = -bolita.speed[1]
        muro.remove(ladrillo)
    # Screen color
    pantalla.fill(color_azul)
    # Draw our ball
    pantalla.blit(bolita.image, bolita.rect)
    # Draw our player
    pantalla.blit(jugador.image, jugador.rect )
    # Draw our bricks
    muro.draw(pantalla)
    # Refresh screen element
    pygame.display.flip()
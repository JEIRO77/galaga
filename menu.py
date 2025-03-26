# Importamos las librerías necesarias
import pygame  # Librería para crear juegos en Python
import random  # Librería para generar números aleatorios
import os  # Librería para manejar archivos y directorios

# Definimos el tamaño de la ventana del juego
WIDTH, HEIGHT = 800, 600  # Ancho y alto de la pantalla
BLACK, WHITE = (0, 0, 0), (255, 255, 255)  # Definimos colores en formato RGB

# Configuración de rutas para cargar imágenes y sonidos
ROOT_DIR = os.path.dirname(__file__)  # Obtiene la ruta del archivo actual
IMAGE_DIR = os.path.join(ROOT_DIR, 'assets')  # Ruta a la carpeta de recursos


# Inicializamos Pygame y el módulo de sonido
pygame.init()  # Inicializa Pygame
pygame.mixer.init()  # Inicializa el sistema de sonido
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Crea la ventana del juego
pygame.display.set_caption('GALAGA')  # Título de la ventana
clock = pygame.time.Clock()  # Reloj para controlar la velocidad del juego

# Cargar música de fondo
pygame.mixer.music.load(os.path.join(IMAGE_DIR, 'background_music.mp3'))  # Asegúrate de que el archivo existe
pygame.mixer.music.set_volume(1.0)  # Ajustar volumen (0.0 a 1.0)
pygame.mixer.music.play(-1)  # Reproducir en bucle (-1 significa infinito)

# Cargar sonidos del juego
shoot_sound = pygame.mixer.Sound(os.path.join(IMAGE_DIR, 'laser.wav'))  # Sonido de disparo
explosion_sound = pygame.mixer.Sound(os.path.join(IMAGE_DIR, 'explosion.wav'))  # Sonido de explosión

# Clase que representa al jugador
class Player(pygame.sprite.Sprite):# Clase del jugador
    def __init__(self):# Inicializa el jugador
        super().__init__()  # Llama al constructor de la clase padre
        self.image = pygame.image.load(os.path.join(IMAGE_DIR, 'iron.png')).convert()  # Carga la imagen del jugador
        self.image.set_colorkey(BLACK)  # Hace el color negro transparente
        self.rect = self.image.get_rect()  # Obtiene el rectángulo de la imagen
        self.rect.centerx = WIDTH // 2  # Posiciona el jugador en el centro de la pantalla
        self.rect.bottom = HEIGHT - 10  # Ubica al jugador en la parte inferior de la pantalla
        self.speed_x = 0  # Velocidad inicial del jugador

    def update(self):## Actualiza la posición del jugador
        self.speed_x = 0  # Resetea la velocidad
        keystate = pygame.key.get_pressed()  # Obtiene las teclas presionadas
        if keystate[pygame.K_LEFT]:  # Si se presiona la flecha izquierda
            self.speed_x = -5  # Mueve el jugador a la izquierda
        if keystate[pygame.K_RIGHT]:  # Si se presiona la flecha derecha
            self.speed_x = 5  # Mueve el jugador a la derecha
        self.rect.x += self.speed_x  # Aplica el movimiento

        # Evita que el jugador se salga de la pantalla
        if self.rect.right > WIDTH:# Si el jugador se sale de la pantalla por la derecha
            self.rect.right = WIDTH# Si el jugador se sale de la pantalla por la derecha
        if self.rect.left < 0:# Si el jugador se sale de la pantalla por la izquierda
            self.rect.left = 0# Si el jugador se sale de la pantalla por la izquierda

    def shoot(self):  # Método para disparar
        bullet = Bullet(self.rect.centerx, self.rect.top)  # Crea una bala en la posición del jugador
        all_sprites.add(bullet)  # Agrega la bala al grupo de sprites
        bullets.add(bullet)  # Agrega la bala al grupo de balas
        shoot_sound.play()  # Reproduce el sonido de disparo

# Clase que representa a los meteoritos
class Meteor(pygame.sprite.Sprite):# Clase que representa a los meteoritos
    def __init__(self):# Inicializa la clase
        super().__init__()# Inicializa la clase padre
        self.image = pygame.image.load(os.path.join(IMAGE_DIR, 'meteorGrey_big1.png')).convert()  # Carga la imagen del meteorito
        self.image.set_colorkey(BLACK)  # Hace el color negro transparente
        self.rect = self.image.get_rect()  # Obtiene el rectángulo de la imagen
        self.rect.x = random.randrange(WIDTH - self.rect.width)  # Posición aleatoria en X
        self.rect.y = random.randrange(-100, -40)  # Posición aleatoria arriba de la pantalla
        self.speedy = random.randrange(1, 10)  # Velocidad aleatoria en Y
        self.speedx = random.randrange(-5, 5)  # Velocidad aleatoria en X

    def update(self):# Actualiza la posición del meteorito
        self.rect.y += self.speedy  # Mueve el meteorito hacia abajo
        self.rect.x += self.speedx  # Mueve el meteorito de lado a lado

        # Si el meteorito sale de la pantalla, reaparece arriba con nuevas coordenadas
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 25:# Si el meteorito sale de la pantalla, reaparece arriba con nuevas coordenadas
            self.rect.x = random.randrange(WIDTH - self.rect.width)# Posición aleatoria en X
            self.rect.y = random.randrange(-100, -40)# Posición aleatoria arriba de la pantalla
            self.speedy = random.randrange(1, 10)# Velocidad aleatoria en Y

# Clase que representa las balas
class Bullet(pygame.sprite.Sprite):# Clase que representa las balas
    def __init__(self, x, y):# Inicializa el sprite
        super().__init__()# Inicializa el sprite
        self.image = pygame.Surface((5, 15))  # Crea una superficie para la bala
        self.image.fill(WHITE)  # Colorea la bala de blanco
        self.rect = self.image.get_rect()  # Obtiene el rectángulo de la bala
        self.rect.centerx = x  # Posiciona la bala en X
        self.rect.bottom = y  # Posiciona la bala en Y
        self.speedy = -10  # Velocidad de la bala (hacia arriba)

    def update(self):# Mueve la bala hacia arriba
        self.rect.y += self.speedy  # Mueve la bala hacia arriba
        if self.rect.bottom < 0:  # Si la bala sale de la pantalla
            self.kill()  # Elimina la bala

# Cargar imagen de fondo
background = pygame.image.load(os.path.join(IMAGE_DIR, 'fondo.png')).convert()# Carga la imagen de fondo

# Crear grupos de sprites
all_sprites = pygame.sprite.Group()# Crea el grupo de todos los sprites
meteor_list = pygame.sprite.Group()# Crea el grupo de meteoritos
bullets = pygame.sprite.Group()# Crea el grupo de balas

# Crear el jugador y agregarlo a los grupos de sprites
player = Player()# Crea el jugador
all_sprites.add(player)# Agrega el jugador al grupo de sprites

# Crear meteoritos y agregarlos a los grupos de sprites
for i in range(6):# Crea 6 meteoritos
    meteor = Meteor()# Crea un meteorito
    all_sprites.add(meteor)# Agrega el meteorito al grupo de sprites
    meteor_list.add(meteor)# Agrega el meteorito al grupo de meteoritos

# Configuración de la puntuación
score = 0  # Inicializa la puntuación en 0
font = pygame.font.SysFont("Arial", 30)  # Fuente para mostrar la puntuación

# Bucle principal del juego
running = True# Si el juego está corriendo
while running:# Si el juego está corriendo
    clock.tick(60)  # Controla la velocidad del juego (60 FPS)

    # Procesar eventos
    for event in pygame.event.get():# Si se presiona una tecla
        if event.type == pygame.QUIT:  # Si se cierra la ventana
            running = False  # Termina el juego
        elif event.type == pygame.KEYDOWN:# Si se presiona una tecla
            if event.key == pygame.K_SPACE:  # Si se presiona la barra espaciadora
                player.shoot()  # El jugador dispara

    # Actualizar posiciones y colisiones
    all_sprites.update()
    
    # Detectar colisión (Jugador vs Meteoritos)
    if pygame.sprite.spritecollide(player, meteor_list, False):# Si el jugador colisiona con un meteorito
        explosion_sound.play()  # Reproduce sonido de explosión
        screen.blit(background, [0, 0])  # Redibujar fondo antes de mostrar "Game Over"
        all_sprites.draw(screen)  # Dibujar los sprites actuales
        font = pygame.font.SysFont("Arial", 50)  # Fuente grande
        game_over_text = font.render("GAME OVER", True, WHITE)  # Texto de Game Over
        screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2))  # Posicionar texto
        pygame.display.flip()  # Actualizar pantalla
        pygame.mixer.music.stop()  # Detener la música de fondo
        pygame.time.delay(3000)  # Esperar 3 segundos antes de cerrar el juego
        running = False  # Salir del bucle del juego



    hits = pygame.sprite.groupcollide(meteor_list, bullets, True, True)  # Detección de colisión entre balas y meteoritos
    for hit in hits:# Para cada colisión detectada
        explosion_sound.play()  # Sonido de explosión
        score += 10  # Aumenta la puntuación
        meteor = Meteor()  # Crea un nuevo meteorito
        all_sprites.add(meteor)# Agrega el meteorito al grupo de sprites
        meteor_list.add(meteor)# Agrega el meteorito al grupo de meteoritos

    # Dibujar en pantalla
    screen.blit(background, [0, 0])# Dibuja el fondo
    all_sprites.draw(screen)# Dibuja todos los sprites
    score_text = font.render(f"Score: {score}", True, WHITE)  # Muestra la puntuación
    screen.blit(score_text, (10, 10))# Posicionar texto
    pygame.display.flip()# Actualizar pantalla

pygame.quit()# Salir del juego

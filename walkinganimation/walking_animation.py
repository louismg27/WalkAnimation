import os
import pygame

dir_actual = os.path.dirname(os.path.abspath(__file__))

IMAGE_FILE = [dir_actual, "assets", "imagen", "walking_animation.png"]
BACKGROUND = [dir_actual, "assets", "imagen", "background.jpg"]

class Animacion:
    def __init__(self):
        """Inicializa el juego de animación de caminar."""

        # Inicializamos  pygame.
        pygame.init()
        pygame.mixer.init()

        # Configuramos el tamaño de la pantalla.
        self.__ancho = 900
        self.__alto = 480
        self.__pantalla = pygame.display.set_mode((self.__ancho, self.__alto), 0, 32)
        pygame.display.set_caption("Walking Animation")

        # Cargamos archivos de imagen y de fondo
        self.__imagen = pygame.image.load(os.path.join(*IMAGE_FILE)).convert_alpha()
        self.__background = pygame.image.load(os.path.join(*BACKGROUND)).convert_alpha()
        self.__background = pygame.transform.scale(self.__background, (self.__ancho, self.__alto))

        # Creamos rectángulos a partir de la imagen.
        self.rectangulos = self.__crear_rectangulos()

        # Atributos de control.
        self.__puntero = 0  # Controla el rectángulo (imagen) actual.
        self.__x = 320  # Establecemos Posición x.
        self.__y = 352  # Establecemos la Posición y (parte baja de la pantalla).
        self.__direction = True  # Establecemos True el Sentido del movimiento.
        self.__running = False  # Controla si el juego está en ejecución.
        # self.__saltando = False  # Controla si el personaje está saltando.
        # self.__subiendo = True  # Controla si el person

    def run(self):
        """Ejecución de la aplicación"""
        
        self.__running = True
        fps_clock = pygame.time.Clock()
        
        seguir = True
        
        while self.__running:
            
            # Se procesan los eventos.
            self.__procesar_evento()
            
            # Controlamos la velocidad del paseo.
            if seguir:
                seguir = False
                t_i = pygame.time.get_ticks()   # Tiempo inicial.
                contador = 0                    # Milisengundos de espera.            
            
            t_a = pygame.time.get_ticks()       # Tiempo actual.
            
            contador += (t_a - t_i)
            
            if contador > 200:

                # Se actualiza.
                self.__update()
                seguir = True
            
            # Se pinta.
            self.__render()

            # 60 frames.
            fps_clock.tick(60)
            
        self.__quit()    
    
    def __update(self):
        """Actualizamos la imagen del personaje caminando."""

        # Controlamos el sentido del movimiento (derecha o izquierda).
        if self.__direction:
            # Establecemos el Movimiento hacia la derecha.
            self.__x += 5
            self.__puntero += 1

            # Ciclo de animación para caminar hacia la derecha.
            if self.__puntero > 9:
                self.__puntero = 1
        else:
            # Movimiento hacia la izquierda.
            self.__x -= 5
            self.__puntero += 1

            # Ciclo de animación para caminar hacia la izquierda.
            if self.__puntero > 19:
                self.__puntero = 11

        # Comprueba si el personaje llega a los límites de la ventana.
        if self.__ancho - self.__x <= 49:
            # Cambiamos la imagen al límite derecho de la pantalla.
            self.__puntero = 10
            self.__direction = False

        if self.__x <= 0:
            # Cambiamos la imagen al límite izquierdo de la pantalla.
            self.__puntero = 10
            self.__direction = True
        
    def __procesar_evento(self):
        """Procesa eventos"""
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                self.__running = False





    def __crear_rectangulos(self):
        """Crea y devuelve una lista de rectángulos para recortar una imagen en múltiples partes."""

        # Establecemos Dimensiones generales de los rectángulos y la imagen.
        ancho = 640
        alto = 256
        nfil = 2
        ncol = 10

        # Calculamos el ancho y largo de un único rectángulo.
        ancho_rec = int(ancho / ncol)
        largo_rec = int(alto / nfil)

        # Inicializamos una lista para almacenar los rectángulos.
        ret = []
        x = y = 0

        # Generamos los rectángulos en un patrón de cuadrícula.
        for j in range(nfil):
            for i in range(ncol):
                ret.append(pygame.Rect([x, y, ancho_rec, largo_rec]))
                x += ancho_rec

            x = 0
            y += int(alto / nfil)

        # Devuelve la lista de rectángulos generados.
        return ret

    def __render(self):
        """Renderiza gráficos en la pantalla."""

        # Establecemos el fondo de la pantalla.
        self.__pantalla.blit(self.__background, (0, 0))

        # Mostramos la imagen recortada dentro del rectángulo.
        self.__pantalla.blit(self.__imagen, (self.__x, self.__y), self.rectangulos[self.__puntero])

        # Dibujamos un rectángulo
        pygame.draw.rect(self.__pantalla, (0, 0, 0, 0), (0, 0, 0, 0), 0)

        # Actualizamos la pantalla para visualizar los cambios.
        pygame.display.flip()

    def __quit(self):
        """Salir del programa"""

        pygame.quit()
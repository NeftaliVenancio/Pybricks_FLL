
from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

brick = PrimeHub()


class Instrumento:
    """
    Clase para manejar un instrumento adicional en un robot LEGO® SPIKE™ Prime. 
    Permite controlar un motor como instrumento, proporcionando métodos para calibrarlo 
    y moverlo a posiciones específicas dentro de un rango definido.
    
    Atributos:
        instrumento (Motor): Motor que actúa como el instrumento controlado.
        ls (int): Límite superior del rango de movimiento del instrumento.
        li (int): Límite inferior del rango de movimiento del instrumento.
    
    Métodos:
        __init__: Inicializa una instancia de la clase Instrumento.
        calibrar: Calibra el instrumento a un ángulo inicial.
        mover: Mueve el instrumento a un ángulo objetivo dentro de los límites establecidos.
    """

    def __init__(self, motor_instrumento, limite_superior, limite_inferior):
        """
        Inicializa una nueva instancia de la clase Instrumento.
        
        Parámetros:
            motor_instrumento (Motor): El motor que se utilizará como instrumento.
            limite_superior (int): El límite superior del rango de movimiento permitido para el instrumento.
            limite_inferior (int): El límite inferior del rango de movimiento permitido para el instrumento.
        """
        self.actuador = motor_instrumento
        self._ls = limite_superior
        self._li = limite_inferior

    def calibrar(self, set_angulo=0):
        """
        Calibra el instrumento a un ángulo inicial.
        
        Parámetros:
            set_angulo (int): Ángulo inicial al que se debe calibrar el instrumento. Por defecto es 0.
        """
        self.actuador.run_angle(100, -20)  # Ejemplo de implementación
        self.actuador.reset_angle(set_angulo)
        self.actuador.hold()

    def calibra_Auto(self, direccion = True):
        """
        Calibra el instrumento automáticamente en función de la dirección especificada.
        
        Parámetros:
            direccion (bool): Si es True, calibra primero hacia abajo y luego hacia arriba. 
                      Si es False, calibra  primero hacia arriba y luego hacia abajo.
        """
        if direccion:
            # Calibrar hacia abajo
            self.actuador.run_until_stalled(-100, Stop.COAST, 30)
            self.actuador.reset_angle(0)
            self._li = self.actuador.angle()
            # Calibrar hacia arriba
            self.actuador.run_until_stalled(100, Stop.COAST, 30)
            self._ls = self.actuador.angle()
        else:
            # Calibrar hacia arriba
            self.actuador.run_until_stalled(100, Stop.COAST, 30)
            self.actuador.reset_angle(0)
            self._ls = self.actuador.angle()
            # Calibrar hacia abajo
            self.actuador.run_until_stalled(-100, Stop.COAST, 30)
            self._li = self.actuador.angle()

        self.actuador.hold()

    def calibrarManual(self, set_angulo = 0):
        """
        Calibra el instrumento a un ángulo inicial.
        
        Parámetros:
            set_angulo (int): Ángulo inicial al que se debe calibrar el instrumento. Por defecto es 0.
        """
        button = Button.LEFT

        while True:
            presed = PrimeHub.buttons.pressed()

            self.actuador.run_angle(100, -1)

            if button in presed:
                print(button)
                break

        while any(self.brick.buttons.pressed()):
            wait(10)


        self.instrumento.reset_angle(set_angulo)

        button = Button.RIGHT

        while True:
            presed = self.brick.buttons.pressed()

            self.instrumento.run_angle(100, 1)

            if button in presed:
                print(button)
                break

        while any(self.brick.buttons.pressed()):
            wait(10)

        self.ls = self.instrumento.angle()
        self.instrumento.hold()


    def mover(self, angulo_objetivo, velocidad=100):
        """
        Mueve el instrumento a un ángulo objetivo dentro de los límites establecidos.
        
        Parámetros:
            angulo_objetivo (int): Ángulo objetivo al que se debe mover el instrumento.
            velocidad (int): Velocidad a la que se debe mover el instrumento. Por defecto es 100.
        """
        # Implementación de ejemplo que mueve el instrumento al ángulo objetivo
        if angulo_objetivo > self.ls:
            angulo_objetivo = self.ls
        elif angulo_objetivo < self.li:
            angulo_objetivo = self.li
        
        angulo_actual = self.instrumento.angle()
        movimiento = angulo_objetivo - angulo_actual
        self.instrumento.run_angle(velocidad, movimiento)
        self.instrumento.hold()
        
    def arriba(self,velocidad=100):
        """
        Mueve el instrumento a un ángulo objetivo dentro de los límites establecidos.
        
        Parámetros:
            angulo_objetivo (int): Ángulo objetivo al que se debe mover el instrumento.
            velocidad (int): Velocidad a la que se debe mover el instrumento. Por defecto es 100.
        """
        # Implementación de ejemplo que mueve el instrumento a la posición arriba    
        angulo_Act = self.actuador.angle()
        while angulo_Act > self._ls:
            #self.actuador.run_angle(velocidad,-1)
            self.actuador.track_target(self._ls)
            angulo_Act = self.actuador.angle()
        self.actuador.hold()

    def abajo(self,velocidad=100):
        """
        Mueve el instrumento a un ángulo objetivo dentro de los límites establecidos.
        
        Parámetros:
            angulo_objetivo (int): Ángulo objetivo al que se debe mover el instrumento.
            velocidad (int): Velocidad a la que se debe mover el instrumento. Por defecto es 100.
        """
        # Implementación de ejemplo que mueve el instrumento al ángulo objetivo
        
        angulo_Act = self.actuador.angle()
        while angulo_Act < self._li:
            #self.actuador.run_angle(velocidad,1)
            self.actuador.track_target(self._li)
            angulo_Act = self.actuador.angle()
        self.actuador.hold()
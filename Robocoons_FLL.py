from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor
from pybricks.parameters import Button, Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait

class Robot:
    """
    Clase Robot diseñada para interactuar con el LEGO® SPIKE™ Prime.
    Proporciona funcionalidades para controlar motores y sensores, así como para realizar movimientos básicos.
    
    Atributos:
        brick (PrimeHub): El hub central de LEGO® SPIKE™ Prime.
        mI (Motor): Motor izquierdo.
        mD (Motor): Motor derecho.
        sI (ColorSensor): Sensor de color izquierdo.
        sD (ColorSensor): Sensor de color derecho.
        db (DriveBase): Base de manejo para controlar los movimientos del robot.
        
    Métodos:
        __init__: Inicializa una nueva instancia de la clase Robot.
        button_pressed: Verifica si un botón específico está presionado.
        wait_button: Espera hasta que un botón específico sea presionado.
        buttopn_program_stop: Establece un botón para detener el programa (Nombre del método parece tener un typo).
        girar: Gira el robot un ángulo específico a una velocidad dada.
    """

    def __init__(self, HUB=PrimeHub, MotorI=Motor, MotorD=Motor, SensorColorI=ColorSensor, SensorColorD=ColorSensor):
        """
        Inicializa el robot con los motores y sensores especificados.
        
        Parámetros:
            HUB (PrimeHub): El hub central de LEGO® SPIKE™ Prime.
            MotorI (Motor): Motor conectado al puerto izquierdo.
            MotorD (Motor): Motor conectado al puerto derecho.
            SensorColorI (ColorSensor): Sensor de color conectado a un puerto izquierdo.
            SensorColorD (ColorSensor): Sensor de color conectado a un puerto derecho.
        """
        self.brick = HUB

        self.mI = MotorI
        self.mD = MotorD
        self.sI = SensorColorI
        self.sD = SensorColorD

        self.d_rueda = 55
        self.d_eje = 115

        self.db = DriveBase(self.mI, self.mD, self.d_rueda, self.d_eje)
        self.db.use_gyro(True)

    def button_pressed(self, button=Button):
        """
        Verifica si un botón específico está presionado.
        
        Parámetros:
            button (Button): El botón a verificar.
            
        Retorna:
            bool: True si el botón está presionado, False en caso contrario.
        """
        presed = self.brick.buttons.pressed()
        return button in presed

    def wait_button(self, button=Button):
        """
        Espera hasta que un botón específico sea presionado.
        
        Parámetros:
            button (Button): El botón a esperar.
        """
        while True:
            presed = self.brick.buttons.pressed()
            if button in presed:
                print(button)
                break

        while any(self.brick.buttons.pressed()):
            wait(10)

    def buttopn_program_stop(self, button=Button):
        """
        Establece un botón para detener el programa. (Revisar el nombre del método para corrección de typo)
        
        Parámetros:
            button (Button): El botón para detener el programa.
        """
        self.brick.system.set_stop_button(button)

    def girar(self, angulo, velocidad=100):
        """
        Gira el robot un ángulo específico a una velocidad dada.
        
        Parámetros:
            angulo (int): El ángulo de giro en grados.
            velocidad (int): La velocidad de giro.
        """
        self.db.use_gyro(True)
        self.db.reset()
        self.db.settings(turn_acceleration=velocidad)
        self.db.turn(angulo, then=Stop.HOLD)

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
        self.instrumento = motor_instrumento
        self.ls = limite_superior
        self.li = limite_inferior

    def calibrar(self, set_angulo=0):
        """
        Calibra el instrumento a un ángulo inicial.
        
        Parámetros:
            set_angulo (int): Ángulo inicial al que se debe calibrar el instrumento. Por defecto es 0.
        """
        self.instrumento.run_angle(100, -20)  # Ejemplo de implementación
        self.instrumento.reset_angle(set_angulo)
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

class InstrumentoDoble:
    """
    Clase para manejar dos instrumentos adicionales en un robot LEGO® SPIKE™ Prime simultáneamente.
    Permite controlar dos motores como instrumentos de manera coordinada, ofreciendo métodos para calibrarlos
    y moverlos a posiciones específicas dentro de un rango definido.

    Atributos:
        iI (Motor): Motor que actúa como el instrumento izquierdo.
        iD (Motor): Motor que actúa como el instrumento derecho.
        ls (int): Límite superior del rango de movimiento permitido para los instrumentos.
        li (int): Límite inferior del rango de movimiento permitido para los instrumentos.

    Métodos:
        __init__: Inicializa una instancia de la clase InstrumentoDoble.
        calibrar: Calibra ambos instrumentos a un ángulo inicial común.
        mover: Mueve ambos instrumentos a un ángulo objetivo dentro de los límites establecidos.
    """

    def __init__(self, instrumentoIzq, instrumentoDer, limite_superior, limite_inferior):
        """
        Inicializa una nueva instancia de la clase InstrumentoDoble.

        Parámetros:
            instrumentoIzq (Motor): El motor que se utilizará como el instrumento izquierdo.
            instrumentoDer (Motor): El motor que se utilizará como el instrumento derecho.
            limite_superior (int): El límite superior del rango de movimiento permitido para los instrumentos.
            limite_inferior (int): El límite inferior del rango de movimiento permitido para los instrumentos.
        """
        self.iI = instrumentoIzq
        self.iD = instrumentoDer
        self.ls = limite_superior
        self.li = limite_inferior

    def calibrar(self, set_angulo=0):
        """
        Calibra ambos instrumentos a un ángulo inicial común.

        Parámetros:
            set_angulo (int): Ángulo inicial al que se deben calibrar ambos instrumentos. Por defecto es 0.
        """
        # Ejemplo de implementación de calibración
        self.iI.run_angle(100, -20, wait=False)
        self.iD.run_angle(100, -20, wait=True)
        self.iI.reset_angle(set_angulo)
        self.iD.reset_angle(set_angulo)
        self.iI.hold()
        self.iD.hold()

    def mover(self, angulo_objetivo, velocidad=100):
        """
        Mueve ambos instrumentos a un ángulo objetivo dentro de los límites establecidos de manera coordinada.

        Parámetros:
            angulo_objetivo (int): Ángulo objetivo al que se deben mover ambos instrumentos.
            velocidad (int): Velocidad a la que se deben mover los instrumentos. Por defecto es 100.
        """
        # Implementación de ejemplo que mueve ambos instrumentos al ángulo objetivo
        if angulo_objetivo > self.ls:
            angulo_objetivo = self.ls
        elif angulo_objetivo < self.li:
            angulo_objetivo = self.li
        
        angulo_actual_iI = self.iI.angle()
        angulo_actual_iD = self.iD.angle()
        movimiento_iI = angulo_objetivo - angulo_actual_iI
        movimiento_iD = angulo_objetivo - angulo_actual_iD
        self.iI.run_angle(velocidad, movimiento_iI, wait=False)
        self.iD.run_angle(velocidad, movimiento_iD, wait=True)
        self.iI.hold()
        self.iD.hold()

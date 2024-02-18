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

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

spike = PrimeHub()

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

        self.ref_black = 35

        self.d_rueda = 55
        self.d_eje = 115

        self.db = DriveBase(self.mI, self.mD, self.d_rueda, self.d_eje)
        self.db.use_gyro(True)

        self.p_ant = 0
        self.e1 = 0
        self.e2 = 0
        self.e3 = 0
        self.e4 = 0
        self.e5 = 0
        self.e6 = 0

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

    def girar(self, angulo, velocidad=150):
        """
        Gira el robot un ángulo específico a una velocidad dada.
        
        Parámetros:
            angulo (int): El ángulo de giro en grados.
            velocidad (int): La velocidad de giro.
        """
        self.db.reset()

        #Corrige angulo por desviación de 5º    
        if angulo > 0:
            
            angulo = angulo + 5

        elif angulo < 0: 

            angulo = angulo - 5
        
        self.db.use_gyro(True)
        self.db.settings(turn_rate=velocidad)
        self.db.turn(angulo, then=Stop.HOLD)

    def calibrarNegro(self, button_start = Button.RIGHT, muestras = 10):
        cont = 0
        prom = 0
        lec1 = 0
        lec2 = 0

        while True:
            presed = self.brick.buttons.pressed()
            if button in presed:
                print(button)
                break
        while any(self.brick.buttons.pressed()):
            wait(10)

        for i in range(1,muestras+1):
            lec1 += self.sD.reflection()
            lec2 += self.sI.reflection()
            wait(10)
        
        lec1 = lec1/muestras
        lec2 = lec2/muestras

        self.ref_black = (lec1+lec2)/2

        print(self.ref_black)

    def seguir_linea(self, velocidad = 50, LineaIzquierda = True, LineaDerecha = False):
        

        if velocidad > 100:
            velocidad = 100
            print("Velocidad maxima es 100%")

        if LineaIzquierda == True:

            if LineaDerecha == True:

                print("sigue linea con ambos sensores")
                
                lecI = self.sI.reflection()
                lecD = self.sD.reflection()

            else:
                print("sigue linea con sensor izquierdo")
                lecI = self.sI.reflection()

                error = lecI - 50
                correction = error * 2

                if lecI < self.ref_black :
                    self.mD.dc(velocidad)
                    self.mI.dc(0)
                elif lecI < 90:
                    self.mD.dc(velocidad)
                    self.mI.dc(velocidad)

                else:
                    self.mD.dc(0)
                    self.mI.dc(velocidad)

        elif LineaDerecha == True:
                print("sigue linea con sensor derecho")
                
                lecD = self.sD.reflection()
                if lecD < self.ref_black :
                    self.mI.dc(velocidad)
                    self.mD.dc(0)
                else:
                    self.mI.dc(0)
                    self.mD.dc(velocidad)

    def girarHastaLinea(self, sensor = ColorSensor, velocidad = 50 ):

        lec = sensor.reflection()

        if lec > self.ref_black:

            if velocidad < 0:
                self.mD.dc(-velocidad)
                self.mI.dc(velocidad)
            elif velocidad > 0:
                self.mD.dc(-velocidad)
                self.mI.dc(velocidad)
        else:
            self.mI.dc(0)
            self.mD.dc(0)

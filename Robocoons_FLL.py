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

    def calibrarManual(self, set_angulo = 0):
        """
        Calibra el instrumento a un ángulo inicial.
        
        Parámetros:
            set_angulo (int): Ángulo inicial al que se debe calibrar el instrumento. Por defecto es 0.
        """
        button = Button.LEFT

        while True:
            presed = PrimeHub.buttons.pressed()

            self.instrumento.run_angle(100, -1)

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

    def calibrarManual(self, set_angulo = 0, abajo = True, arriba = False):
        """
        Calibra el instrumento a un ángulo inicial.
        
        Parámetros:
            set_angulo (int): Ángulo inicial al que se debe calibrar el instrumento. Por defecto es 0.
        """

        if abajo == True:

            button = Button.LEFT

            while button not in spike.buttons.pressed():
                print("Esperando boton")

            while button in spike.buttons.pressed():

            #self.iI.run_angle(500, -10, wait=False)
            #self.iD.run_angle(500, -10, wait=True)

                self.iI.dc(-50)
                self.iD.dc(-50)

            print(button)


            self.iI.hold()
            self.iD.hold()

            self.iI.reset_angle(set_angulo)
            self.iD.reset_angle(set_angulo)

        if arriba == True:

            button = Button.RIGHT

            while button not in spike.buttons.pressed():
                print("Esperando boton")

            while button in spike.buttons.pressed():

            #self.iI.run_angle(500, 10, wait=False)
            #self.iD.run_angle(500, 10, wait=True)
                self.iI.dc(50)
                self.iD.dc(50)

            print(button)

            self.ls = self.iD.angle()
        
            self.iI.hold()
            self.iD.hold()
            print(self.ls)

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

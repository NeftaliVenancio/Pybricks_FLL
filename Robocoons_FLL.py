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

    def calibrarNegro(self, button_start=Button.RIGHT, muestras=10):
    """
    Calibra el valor de referencia para el color negro basado en las lecturas promedio de los sensores de color izquierdo y derecho.
    Este proceso inicia al presionar un botón específico y toma un número definido de muestras para calcular el promedio.
    
    Parámetros:
        button_start (Button): Botón para iniciar el proceso de calibración. Por defecto, es el botón derecho.
        muestras (int): Número de muestras a tomar para el cálculo del promedio. Por defecto, son 10 muestras.
    """
    # Inicialización de variables para almacenar sumas de lecturas y promedio
    lec1 = 0  # Suma de lecturas del sensor de color derecho
    lec2 = 0  # Suma de lecturas del sensor de color izquierdo

    # Espera hasta que el botón especificado sea presionado para comenzar la calibración
    while True:
        presed = self.brick.buttons.pressed()
        if button_start in presed:
            print(button_start)  # Imprime el botón presionado para confirmación
            break
    # Espera hasta que todos los botones sean liberados antes de continuar
    while any(self.brick.buttons.pressed()):
        wait(10)

    # Toma lecturas de los sensores de color especificadas veces y acumula los valores
    for i in range(1, muestras + 1):
        lec1 += self.sD.reflection()  # Lectura del sensor de color derecho
        lec2 += self.sI.reflection()  # Lectura del sensor de color izquierdo
        wait(10)  # Pequeña pausa entre lecturas para estabilización

    # Calcula el promedio de las lecturas de cada sensor y luego el promedio general para establecer el valor de referencia para negro
    lec1 = lec1 / muestras
    lec2 = lec2 / muestras
    self.ref_black = (lec1 + lec2) / 2  # Establece el valor promedio como el nuevo valor de referencia para negro

    # Imprime el valor de referencia para negro calculado
    print(self.ref_black)


    def seguir_linea(self, velocidad=50, LineaIzquierda=True, LineaDerecha=False):
    """
    Controla el robot para seguir una línea utilizando los sensores de color izquierdo y/o derecho. Ajusta la
    velocidad de los motores en base a la lectura de reflectancia de los sensores para mantener al robot alineado
    con la línea. La función permite una configuración flexible para seguir la línea solo con el sensor izquierdo,
    solo con el derecho, o con ambos.
    
    Parámetros:
        velocidad (int): Define la velocidad de seguimiento de la línea. Se limita a 100 como máximo para evitar errores.
        LineaIzquierda (bool): Si es verdadero, el robot intentará seguir la línea con el sensor de color izquierdo.
        LineaDerecha (bool): Si es verdadero, el robot usará el sensor de color derecho para seguir la línea.
    
    Notas:
        - Si ambos LineaIzquierda y LineaDerecha son verdaderos, el robot intentará seguir la línea utilizando ambos sensores,
          ajustando su trayectoria de forma que se mantenga en la línea según las lecturas de ambos sensores.
        - Si la velocidad especificada es mayor a 100, se ajustará automáticamente a 100, y se notificará al usuario.
    """
    # Ajusta la velocidad si es mayor a 100%
    if velocidad > 100:
        velocidad = 100
        print("Velocidad maxima es 100%")

    # Seguir línea con ambos sensores
    if LineaIzquierda and LineaDerecha:
        print("sigue linea con ambos sensores")
        lecI = self.sI.reflection()
        lecD = self.sD.reflection()

    # Seguir línea solo con sensor izquierdo
    elif LineaIzquierda:
        print("sigue linea con sensor izquierdo")
        lecI = self.sI.reflection()
        # Ajustes basados en la lectura del sensor izquierdo
        if lecI < self.ref_black:
            self.mD.dc(velocidad)
            self.mI.dc(0)
        elif lecI < 90:
            self.mD.dc(velocidad)
            self.mI.dc(velocidad)
        else:
            self.mD.dc(0)
            self.mI.dc(velocidad)

    # Seguir línea solo con sensor derecho
    elif LineaDerecha:
        print("sigue linea con sensor derecho")
        lecD = self.sD.reflection()
        # Ajustes basados en la lectura del sensor derecho
        if lecD < self.ref_black:
            self.mI.dc(velocidad)
            self.mD.dc(0)
        else:
            self.mI.dc(0)
            self.mD.dc(velocidad)


    def girarHastaLinea(self, sensor=ColorSensor, velocidad=50):
    """
    Gira el robot hasta que el sensor de color especificado detecta una línea. La detección se basa en comparar la
    reflectividad del sensor con un valor de referencia preestablecido que representa el color negro de la línea.
    
    Parámetros:
        sensor (ColorSensor): El sensor de color utilizado para detectar la línea. Debe ser una instancia de ColorSensor.
        velocidad (int): La velocidad a la que el robot gira para buscar la línea. Un valor negativo gira el robot
                         en dirección contraria a las agujas del reloj, mientras que un valor positivo gira en dirección
                         de las agujas del reloj.
    
    Notas:
        - El robot gira hasta que el sensor detecta una reflectividad menor o igual al valor de referencia para el negro,
          lo que indica que el sensor está sobre la línea.
        - Si la lectura del sensor es mayor al valor de referencia (indicando que aún no está sobre la línea), el robot
          gira en la dirección indicada por la velocidad.
        - Cuando el sensor detecta la línea, el robot se detiene.
    """
    # Obtener la lectura de reflectividad del sensor
    lec = sensor.reflection()

    # Comprobar si la lectura está por encima del valor de referencia para negro
    if lec > self.ref_black:
        # Girar el robot en la dirección y velocidad indicadas
        self.mD.dc(-velocidad)
        self.mI.dc(velocidad)
    else:
        # Detener el robot una vez que detecta la línea
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

   def calibrarManual(self, set_angulo=0):
    """
    Permite al usuario calibrar manualmente el ángulo del instrumento motorizado utilizando los botones del dispositivo.
    Esta calibración manual facilita el ajuste preciso del ángulo inicial o de referencia del instrumento antes de
    iniciar operaciones o mediciones. El método utiliza un proceso en dos pasos: primero, ajusta el ángulo en una dirección
    con el botón izquierdo, y luego en la dirección opuesta con el botón derecho, para un ajuste fino.

    Parámetros:
        set_angulo (int): El ángulo de calibración inicial o de referencia para el instrumento. Por defecto es 0.
    
    Notas:
        - El usuario debe presionar el botón izquierdo (Button.LEFT) para ajustar el ángulo en decrementos pequeños.
        - Tras alcanzar el ajuste deseado, el usuario puede presionar el botón derecho (Button.RIGHT) para incrementar
          el ángulo en pequeños pasos.
        - El proceso termina cuando el usuario suelta el botón, y el ángulo actual se establece como el ángulo de referencia.
        - El instrumento mantiene su posición (hold) al finalizar la calibración.
    """
    # Ajuste decreciente del ángulo con el botón izquierdo
    button = Button.LEFT
    while True:
        presed = PrimeHub.buttons.pressed()
        self.instrumento.run_angle(100, -1)  # Mueve el instrumento en pequeños decrementos
        if button in presed:
            print(button)
            break
    while any(self.brick.buttons.pressed()):
        wait(10)

    # Establece el ángulo de referencia
    self.instrumento.reset_angle(set_angulo)

    # Ajuste creciente del ángulo con el botón derecho
    button = Button.RIGHT
    while True:
        presed = self.brick.buttons.pressed()
        self.instrumento.run_angle(100, 1)  # Mueve el instrumento en pequeños incrementos
        if button in presed:
            print(button)
            break
    while any(self.brick.buttons.pressed()):
        wait(10)

    # Finaliza la calibración y mantiene la posición del instrumento
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

    def calibrarManual(self, set_angulo=0, abajo=True, arriba=False):
    """
    Facilita la calibración manual de los instrumentos motorizados (como brazos o herramientas) en el robot. Permite
    ajustar el ángulo de estos instrumentos hacia arriba o hacia abajo utilizando los botones del dispositivo, y
    establece un ángulo de referencia una vez completada la calibración.

    Parámetros:
        set_angulo (int): El ángulo de referencia deseado para los instrumentos después de la calibración. Por defecto es 0.
        abajo (bool): Si es True, el método espera la interacción con el botón izquierdo para mover los instrumentos hacia abajo.
        arriba (bool): Si es True, el método espera la interacción con el botón derecho para mover los instrumentos hacia arriba.

    Notas:
        - El usuario debe mantener presionado el botón correspondiente (izquierdo para abajo, derecho para arriba) para ajustar
          la posición de los instrumentos. La calibración termina cuando el usuario suelta el botón.
        - Los movimientos se realizan a una velocidad constante definida en el método para asegurar un ajuste fino y controlado.
        - Una vez completada la calibración, los instrumentos mantienen su posición y se establece el ángulo de referencia indicado.
    """
    # Calibración hacia abajo con el botón izquierdo
    if abajo:
        button = Button.LEFT
        # Espera hasta que el botón izquierdo sea presionado
        while button not in spike.buttons.pressed():
            print("Esperando boton")
        # Mueve los instrumentos hacia abajo mientras el botón esté presionado
        while button in spike.buttons.pressed():
            self.iI.dc(-50)
            self.iD.dc(-50)

        # Fija la posición de los instrumentos y establece el ángulo de referencia
        self.iI.hold()
        self.iD.hold()
        self.iI.reset_angle(set_angulo)
        self.iD.reset_angle(set_angulo)

    # Calibración hacia arriba con el botón derecho
    if arriba:
        button = Button.RIGHT
        # Espera hasta que el botón derecho sea presionado
        while button not in spike.buttons.pressed():
            print("Esperando boton")
        # Mueve los instrumentos hacia arriba mientras el botón esté presionado
        while button in spike.buttons.pressed():
            self.iI.dc(50)
            self.iD.dc(50)

        # Al terminar, fija la posición de los instrumentos y actualiza el límite superior
        self.ls = self.iD.angle()
        self.iI.hold()
        self.iD.hold()
        print(self.ls)


    def mover(self, angulo_objetivo, velocidad=100):
    """
    Mueve ambos instrumentos motorizados hacia un ángulo objetivo a una velocidad especificada. Antes de mover, verifica
    que el ángulo objetivo esté dentro de los límites superior e inferior definidos para el movimiento de los instrumentos.
    Si el ángulo objetivo está fuera de estos límites, se ajusta al límite más cercano.

    Parámetros:
        angulo_objetivo (int): El ángulo al que se deben mover los instrumentos.
        velocidad (int): La velocidad a la que se moverán los instrumentos. Especificada en grados por segundo.

    Notas:
        - El método ajusta automáticamente el ángulo objetivo si está fuera de los límites permitidos (ls para el límite superior, li para el inferior).
        - Los movimientos de los instrumentos se realizan de forma coordinada para alcanzar el ángulo objetivo al mismo tiempo.
        - Tras alcanzar el ángulo objetivo, los instrumentos se fijan en su posición actual (hold) para evitar movimientos no deseados.
    """
    # Ajusta el ángulo objetivo para que esté dentro de los límites permitidos
    if angulo_objetivo > self.ls:
        angulo_objetivo = self.ls
    elif angulo_objetivo < self.li:
        angulo_objetivo = self.li
    
    # Calcula el movimiento necesario para cada instrumento desde su posición actual
    angulo_actual_iI = self.iI.angle()
    angulo_actual_iD = self.iD.angle()
    movimiento_iI = angulo_objetivo - angulo_actual_iI
    movimiento_iD = angulo_objetivo - angulo_actual_iD
    
    # Realiza el movimiento de los instrumentos hacia el ángulo objetivo
    self.iI.run_angle(velocidad, movimiento_iI, wait=False)
    self.iD.run_angle(velocidad, movimiento_iD, wait=True)
    
    # Fija los instrumentos en su nueva posición
    self.iI.hold()
    self.iD.hold()


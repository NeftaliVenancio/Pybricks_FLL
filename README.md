# Pybricks_FLL
Modulo de python (Pybricks) creado por el Equipo ROBOCOONS 23747 para el uso herramientas y navegación en competencias que impliquen el uso de 
los sets LEGO® Spike Prime.

Se ha construido con la base de conocimientos que el equipo ha generado a lo largo de sus participaciones en competencias

Codificado en Veracruz, Mexico con ❤️ por:

 - Rodrgio Kai Cabrera
 - Neftali Caicero Venancio
 - Jose Pablo Contreras Dominguez
 - Scarlett Elisett Sarabia Barradas
 - Camila Navarrete Alarcón
 - Cuauhtemoc Fuentes Navarro
 - Mauricio Lascurain Ramirez
 - André MArtinez Vega



# Clases para Control de Robots con LEGO® SPIKE™ Prime

Este proyecto incluye tres clases diseñadas para facilitar el control y la interacción con robots LEGO® SPIKE™ Prime: `Robot`, `Instrumento`, e `InstrumentoDoble`. Estas clases permiten un manejo detallado de los motores y sensores, así como la implementación de funcionalidades específicas como la calibración y movimientos precisos de instrumentos.


## Clase Robot

La clase `Robot` facilita el control de movimientos básicos del robot, gestión de sensores y motores.

### Atributos
- `brick`: Instancia de `PrimeHub`.
- `mI`: Motor izquierdo.
- `mD`: Motor derecho.
- `sI`: Sensor de color izquierdo.
- `sD`: Sensor de color derecho.
- `db`: Base de conducción (`DriveBase`).

### Métodos
- `__init__(HUB, MotorI, MotorD, SensorColorI, SensorColorD)`: Inicializa el robot.
- `button_pressed(button)`: Verifica si un botón está presionado.
- `wait_button(button)`: Espera hasta que se presione un botón específico.
- `buttopn_program_stop(button)`: Establece un botón para detener el programa.
- `girar(angulo, velocidad=100)`: Gira el robot un ángulo específico a una velocidad dada.

### Ejemplo de Uso
```python
robot = Robot(HUB=PrimeHub(), MotorI=Motor(Port.A), MotorD=Motor(Port.B),
              SensorColorI=ColorSensor(Port.C), SensorColorD=ColorSensor(Port.D))
robot.girar(90)
```

## Clase Instrumento

### Descripción
La clase `Instrumento` está diseñada para controlar un único instrumento o motor adicional en un robot LEGO® SPIKE™ Prime. Facilita operaciones como la calibración del motor a un ángulo específico y el movimiento hacia un ángulo objetivo dentro de límites predefinidos.

### Atributos
- `instrumento`: Motor asociado al instrumento. Se espera que sea una instancia de `Motor` de Pybricks.
- `ls` (limite_superior): El límite superior del ángulo que el instrumento puede alcanzar.
- `li` (limite_inferior): El límite inferior del ángulo que el instrumento puede alcanzar.

### Métodos
#### `__init__(motor_instrumento, limite_superior, limite_inferior)`
Constructor de la clase `Instrumento`. Inicializa un nuevo instrumento con un motor y límites de ángulo.

- **Parámetros:**
  - `motor_instrumento`: Instancia de `Motor` que controla el instrumento.
  - `limite_superior`: Límite superior del ángulo para el movimiento del instrumento.
  - `limite_inferior`: Límite inferior del ángulo para el movimiento del instrumento.

#### `calibrar(set_angulo=0)`
Calibra el instrumento a un ángulo inicial. Útil para establecer un punto de referencia para movimientos posteriores.

- **Parámetros:**
  - `set_angulo`: Ángulo al cual el instrumento debe ser calibrado. El valor predeterminado es 0.

#### `mover(angulo_objetivo, velocidad=100)`
Mueve el instrumento a un ángulo objetivo, respetando los límites superior e inferior establecidos.

- **Parámetros:**
  - `angulo_objetivo`: El ángulo al cual el instrumento debe moverse.
  - `velocidad`: La velocidad a la cual se realiza el movimiento. El valor predeterminado es 100.

### Ejemplo de Uso
Este ejemplo muestra cómo crear una instancia de `Instrumento`, calibrarlo y luego moverlo a un ángulo de 90 grados.

```python
from pybricks.pupdevices import Motor
from pybricks.parameters import Port

# Creación de la instancia del instrumento
motor_instrumento = Motor(Port.A) # Asume que el motor está conectado al puerto A
instrumento = Instrumento(motor_instrumento=motor_instrumento, limite_superior=180, limite_inferior=0)

# Calibración del instrumento
instrumento.calibrar()

# Mover el instrumento a un ángulo de 90 grados
instrumento.mover(angulo_objetivo=90)
```

## Clase InstrumentoDoble

La clase `InstrumentoDoble` permite controlar dos instrumentos, como motores, simultáneamente. Está diseñada para situaciones donde se requiere sincronizar el movimiento de dos instrumentos, como en operaciones de precisión o cuando se manipulan objetos con el robot.

### Atributos

- `iI`: Motor del instrumento izquierdo.
- `iD`: Motor del instrumento derecho.
- `ls`: Límite superior de los ángulos de movimiento para ambos instrumentos.
- `li`: Límite inferior de los ángulos de movimiento para ambos instrumentos.

### Métodos

- `__init__(self, instrumentoIzq, instrumentoDer, limite_superior, limite_inferior)`: Constructor de la clase. Inicializa los motores de los instrumentos con los parámetros especificados y establece los límites superior e inferior de movimiento.
  
- `calibrar(self, set_angulo=0)`: Calibra ambos instrumentos a un ángulo inicial. Útil para establecer una posición de referencia antes de comenzar operaciones.
  
- `mover(self, angulo_objetivo, velocidad=100)`: Mueve ambos instrumentos a un ángulo objetivo especificado, con la opción de ajustar la velocidad. Asegura que ambos instrumentos alcancen el ángulo deseado de forma sincronizada.

- `print_angle(self)`: Imprime el ángulo actual de los motores de ambos instrumentos, proporcionando una forma rápida de verificar su estado.

### Ejemplo de Uso

```python
# Inicialización de los motores para los instrumentos izquierdo y derecho
instrumentoIzq = Motor(Port.F)
instrumentoDer = Motor(Port.G)

# Creación de la instancia de InstrumentoDoble
instrumentoDoble = InstrumentoDoble(instrumentoIzq, instrumentoDer)

# Calibración de los instrumentos a un ángulo inicial de 0 grados
instrumentoDoble.calibrar()

# Mover ambos instrumentos a un ángulo de 45 grados a una velocidad de 100
instrumentoDoble.mover(45, 100)

# Imprimir el ángulo actual de los instrumentos
instrumentoDoble.print_angle()


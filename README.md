# Pybricks_FLL
Modulo de python (Pybricks) creado por el Equipo ROBOCOONS 23747 para el uso herramientas y navegación en competencias que impliquen el uso de 
los sets LEGO® Spike Prime.

Se ha construido con la base de conocimientos que el equipo ha generado a lo largo de sus participaciones en competencias

Codificad en Veracruz, Mexico con ❤️ por:

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

### Descripción
La clase `Robot` está diseñada para controlar los movimientos básicos del robot, incluyendo giros y detección de botones. Utiliza el `DriveBase` de Pybricks para simplificar el control de los motores.

### Métodos Principales
- `__init__(self, HUB, MotorI, MotorD, SensorColorI, SensorColorD)`: Constructor de la clase.
- `button_pressed(self, button)`: Verifica si un botón específico está presionado.
- `wait_button(self, button)`: Espera hasta que un botón específico sea presionado.
- `girar(self, angulo, velocidad=100)`: Gira el robot un ángulo específico.

### Ejemplo de Uso
```python
miRobot = Robot(HUB=PrimeHub(), MotorI=Motor(Port.A), MotorD=Motor(Port.B),
                SensorColorI=ColorSensor(Port.C), SensorColorD=ColorSensor(Port.D))
miRobot.girar(90)

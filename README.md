# Mision Especial | Clasificacion de Amenazas
## Tabla de Contenido
1. [Introducción](#introducción)
2. [Descripción](#descripción)
3. [Funcionalidades](#funcionalidades)
4. [Repositorio](#link-del-repositorio)
5. [Autores](#autores-as-los-catadores)

## Introduccion
<div style = "text-align: justify;">

Esta es una práctica estudiantil, cuyo objetivo es crear, a través del Lenguaje de Programación Python, un simulador que emula los servicios de seguridad de la empresa Norton, al implementar un sistema eficiente de análisis de riesgos y clasificación de amenazas para identificar y asignar las denuncias recibidas por la Agencia de Seguridad Global (ASG) , utilizando el concepto de **pilas con prioridad**. El objetivo es identificar y asignar las denuncias recibidas, priorizando las amenazas urgentes para los escuadrones élite, asignando misiones de reconocimiento a otros escuadrones y archivando las amenazas falsas.

## Descripción

El emulador está construido alrededor de un archivo en python llamado [Simulador](simuladorV2.py) capacitado con un menú interactivo que permite a los usuarios la simulación automática de casos como el ingreso manual de denuncias, al permitir realizar la recepción, clasificación y seguimiento de denuncias de amenazas. De tal forma. cada denuncia se registra automáticamente con su hora de recepción y se clasifica en una de tres categorías:

- **Alto riesgo:** Amenazas urgentes que requieren intervención inmediata y son asignadas a escuadrones élite. Se archivan tras 1 minuto.
- **Bajo riesgo:** Amenazas no urgentes que requieren reconocimiento adicional. Se archivan tras 3 minutos.
- **Falsa amenaza:** Denuncias que no representan riesgo real y se archivan inmediatamente.

## Funcionalidades

1. **Recepción y clasificación automática de denuncias**  
   El sistema registra cada denuncia con su hora de recepción y la clasifica según el nivel de riesgo, asignando la acción correspondiente.

2. **Gestión de pilas con prioridad**  
   Las amenazas se almacenan en pilas separadas según su prioridad (alta, baja, falsa), permitiendo un manejo eficiente y ordenado.

3. **Archivado automático por tiempo**  
   Las amenazas se archivan automáticamente al superar el tiempo límite según su clasificación, pasando al historial para referencia futura.

4. **Generación de informes detallados**  
   El sistema puede generar informes en cualquier momento, mostrando el estado actual de las amenazas y el historial de casos atendidos.

5. **Simulación de casos oficiales**  
   Incluye una función para simular el ejemplo oficial de la actividad, permitiendo validar el funcionamiento del sistema con datos predefinidos.

6. **Interfaz interactiva**  
   Permite al usuario ingresar denuncias manualmente, consultar el estado del sistema y ejecutar simulaciones desde un menú sencillo.

## Link del Repositorio
[Norton - Emulador](https://github.com/migueCOLORADO/Norton-Emulador.git)

## Autores as Los Catadores
**Miguel Ángel Colorado Castaño** <br>
**Juan Manuel Hernandez Martelo** <br>
**Julieth Jhosiris Daza Villada** <br>
**Andres Eusse Chavarria** <br>
**Yan Frank Ríos López**
</div>

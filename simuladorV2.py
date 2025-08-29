from datetime import datetime, timedelta
from typing import List, Dict, Optional

class Amenaza:
    def __init__(self, id_mision: str, descripcion: str, clasificacion: str):
        self.id_mision = id_mision
        self.descripcion = descripcion
        self.clasificacion = clasificacion
        self.hora_recepcion = datetime.now()
        self.hora_archivado: Optional[datetime] = None
    
    def __str__(self):
        hora_str = self.hora_recepcion.strftime("%H:%M:%S")
        return f"{self.id_mision} ({self.clasificacion}), {hora_str}"

class SistemaASG:
    def __init__(self):
        self.amenazas_altas: List[Amenaza] = []
        self.amenazas_bajas: List[Amenaza] = []
        self.historial: List[Amenaza] = []
    
    def recibir_denuncia(self, id_mision: str, descripcion: str, clasificacion: str):
        """Recibe una nueva denuncia y la clasifica según su tipo de riesgo"""
        amenaza = Amenaza(id_mision, descripcion, clasificacion)
        
        if clasificacion == "Alto":
            self.amenazas_altas.append(amenaza)
            print(f"| ¡ALERTA! | Amenaza {id_mision} clasificada como ALTA => Asignada a escuadrones elite")
        elif clasificacion == "Bajo":
            self.amenazas_bajas.append(amenaza)
            print(f"| INFO | Amenaza {id_mision} clasificada como BAJA => Asignada para reconocimiento")
        elif clasificacion == "Falsa amenaza":
            amenaza.hora_archivado = amenaza.hora_recepcion
            self.historial.append(amenaza)
            print(f"| INFO | Amenaza {id_mision} archivada como FALSA AMENAZA")
    
    def procesar_tiempo_transcurrido(self, hora_actual: datetime):
        """Procesa las amenazas que han superado su tiempo limite y las mueve al historial"""
        amenazas_altas_vencidas = []
        for amenaza in self.amenazas_altas:
            tiempo_transcurrido = hora_actual - amenaza.hora_recepcion
            if tiempo_transcurrido >= timedelta(minutes=1):
                amenaza.hora_archivado = amenaza.hora_recepcion + timedelta(minutes=1)
                amenazas_altas_vencidas.append(amenaza)
        
        for amenaza in amenazas_altas_vencidas:
            self.amenazas_altas.remove(amenaza)
            self.historial.append(amenaza)
        
        amenazas_bajas_vencidas = []
        for amenaza in self.amenazas_bajas:
            tiempo_transcurrido = hora_actual - amenaza.hora_recepcion
            if tiempo_transcurrido >= timedelta(minutes=3):
                amenaza.hora_archivado = amenaza.hora_recepcion + timedelta(minutes=3)
                amenazas_bajas_vencidas.append(amenaza)
        
        for amenaza in amenazas_bajas_vencidas:
            self.amenazas_bajas.remove(amenaza)
            self.historial.append(amenaza)
    
    def generar_informe(self, hora_actual: datetime):
        """Genera un informe completo del estado actual del sistema"""
        # Actualizar el estado antes de generar el informe
        self.procesar_tiempo_transcurrido(hora_actual)
        
        print("\n" + "="*60)
        print("| ===ASG=== INFORME DE AMENAZAS | AGENCIA DE SEGURIDAD GLOBAL ===ASG=== |")
        print("="*60)
        
        print("\n| VERIFICACION | Analizando Lista de Amenazas Altas:")
        print("-"*50)
        if self.amenazas_altas:
            for amenaza in self.amenazas_altas:
                print(f"| INFO | {amenaza}")
        else:
            print("| ¡ALERTA! | No hay amenazas altas pendientes")
        
        print("\n| VERIFICACION | Analizando Lista de Amenazas Bajas:")
        print("-"*50)
        if self.amenazas_bajas:
            for amenaza in self.amenazas_bajas:
                print(f"| INFO | {amenaza}")
        else:
            print("| ¡ALERTA! | No hay amenazas bajas pendientes")
        
        print("\n| VERIFICACION | Revisando Historial de Amenazas:")
        print("-"*50)
        if self.historial:
            for amenaza in self.historial:
                hora_archivado = amenaza.hora_archivado.strftime("%H:%M:%S")
                print(f"| INFO | {amenaza.id_mision} ({amenaza.clasificacion}), {hora_archivado}")
        else:
            print("| ¡ALERTA! | No hay amenazas en el historial")
        
        print("\n" + "="*60)
        print("| ===ASG=== INFORME COMPLETADO ===ASG=== |")
        print("="*60)

def simular_ejemplo():
    """Simula el ejemplo proporcionado en el ejercicio"""
    sistema = SistemaASG()
    
    print("\n" + "="*60)
    print("| ===ASG=== SIMULACION DEL EJERCICIO OFICIAL ===ASG=== |")
    print("="*60)
    print("| INFO | Iniciando simulacion con datos predefinidos del ejercicio")
    print("| INFO | Procesando 8 misiones de ejemplo (M1-M8)")
    
    # Hora base para la simulacion
    hora_base = datetime.strptime("10:42:50", "%H:%M:%S")
    
    # Simular llegada de amenazas
    casos = [
        ("M1", "Amenaza critica en sector norte", "Alto", "10:42:50"),
        ("M2", "Reporte sin fundamento", "Falsa amenaza", "10:42:53"),
        ("M3", "Actividad sospechosa confirmada", "Alto", "10:42:57"),
        ("M4", "Vigilancia requerida en zona este", "Bajo", "10:43:11"),
        ("M5", "Alarma falsa activada", "Falsa amenaza", "10:43:27"),
        ("M6", "Movimiento irregular detectado", "Bajo", "10:44:01"),
        ("M7", "Reconocimiento necesario", "Bajo", "10:44:37"),
        ("M8", "Amenaza inminente confirmada", "Alto", "10:44:43")
    ]
    
    print("\n| VERIFICACION | Procesando denuncias recibidas:")
    print("-"*50)
    
    for id_mision, descripcion, clasificacion, hora_str in casos:
        # Simular la hora de recepcion
        hora_recepcion = datetime.strptime(hora_str, "%H:%M:%S")
        
        # Crear amenaza con hora simulada
        amenaza = Amenaza(id_mision, descripcion, clasificacion)
        amenaza.hora_recepcion = hora_recepcion
        
        if clasificacion == "Alto":
            sistema.amenazas_altas.append(amenaza)
        elif clasificacion == "Bajo":
            sistema.amenazas_bajas.append(amenaza)
        elif clasificacion == "Falsa amenaza":
            amenaza.hora_archivado = hora_recepcion
            sistema.historial.append(amenaza)
        
        print(f"| INFO | Recibida => {id_mision} ({clasificacion}) a las {hora_str}")
    
    # Generar informe a las 10:45:00
    hora_informe = datetime.strptime("10:45:00", "%H:%M:%S")
    print(f"\n| ¡ALERTA! | Generando informe oficial a las {hora_informe.strftime('%H:%M:%S')}")
    sistema.generar_informe(hora_informe)

def menu_interactivo():
    """Menu interactivo para usar el sistema"""
    sistema = SistemaASG()
    
    while True:
        print("\n" + "="*60)
        print("| ===ASG=== SISTEMA DE ANALISIS DE RIESGOS | MENU PRINCIPAL ===ASG=== |")
        print("="*60)
        print("| INFO | Opciones disponibles:")
        print("| INFO | 1 => Recibir nueva denuncia")
        print("| INFO | 2 => Generar informe de estado")
        print("| INFO | 3 => Ejecutar simulacion del ejercicio")
        print("| INFO | 4 => Salir del sistema")
        print("-"*60)
        
        opcion = input("| PREGUNTA | Seleccione una opcion (Teclee 1, 2, 3 o 4) => ").strip()
        
        if opcion == "1":
            print("\n" + "="*50)
            print("| ===ASG=== RECEPCION DE NUEVA DENUNCIA ===ASG=== |")
            print("="*50)
            
            id_mision = input("| PREGUNTA | Ingrese ID de la mision (ejemplo: M123) => ").strip()
            descripcion = input("| PREGUNTA | Ingrese descripcion de la amenaza => ").strip()
            
            print("\n| INFO | Clasificaciones de riesgo disponibles:")
            print("| INFO | 1 => Alto riesgo (archivado en 1 minuto)")
            print("| INFO | 2 => Bajo riesgo (archivado en 3 minutos)")
            print("| INFO | 3 => Falsa amenaza (archivado inmediatamente)")
            
            while True:
                clasificacion_num = input("| PREGUNTA | Seleccione clasificacion (Teclee 1, 2 o 3) => ").strip()
                if clasificacion_num == "1":
                    clasificacion = "Alto"
                    break
                elif clasificacion_num == "2":
                    clasificacion = "Bajo"
                    break
                elif clasificacion_num == "3":
                    clasificacion = "Falsa amenaza"
                    break
                else:
                    print("| ERROR | Opcion invalida. Intente nuevamente.")
            
            sistema.recibir_denuncia(id_mision, descripcion, clasificacion)
            print("| ¡ALERTA! | Denuncia procesada exitosamente")
        
        elif opcion == "2":
            print("\n| ¡ALERTA! | Generando informe de estado actual...")
            hora_actual = datetime.now()
            sistema.generar_informe(hora_actual)
        
        elif opcion == "3":
            simular_ejemplo()
        
        elif opcion == "4":
            print("\n| ¡ALERTA! | Cerrando Sistema ASG...")
            print("| INFO | Gracias por usar el Sistema de Analisis de Riesgos")
            print("| INFO | Agencia de Seguridad Global - Mision cumplida")
            break
        
        else:
            print("| ERROR | Opcion invalida. Intente nuevamente.")

if __name__ == "__main__":
    print("\n" + "="*70)
    print("| ===ASG=== SISTEMA DE ANALISIS DE RIESGOS ===ASG=== |")
    print("| ===ASG=== AGENCIA DE SEGURIDAD GLOBAL ===ASG=== |")
    print("="*70)
    print("| INFO | Bienvenido al Sistema de Clasificacion de Amenazas")
    print("| INFO | Este sistema procesa denuncias y clasifica riesgos automaticamente")
    print("| INFO | Desarrollado para el control y seguimiento de amenazas de seguridad")
    
    print("\n| INFO | Modos de operacion disponibles:")
    print("| INFO | 1 => Menu interactivo (ingreso manual de denuncias)")
    print("| INFO | 2 => Simulacion del ejercicio (datos predefinidos)")
    print("-"*70)
    
    while True:
        modo = input("| PREGUNTA | Seleccione modo de operacion (Teclee 1 o 2) => ").strip()
        if modo == "1":
            print("| ¡ALERTA! | Iniciando modo interactivo...")
            menu_interactivo()
            break
        elif modo == "2":
            print("| ¡ALERTA! | Iniciando simulacion del ejercicio...")
            simular_ejemplo()
            break
        else:
            print("| ERROR | Debe teclear un número válido (1 o 2). Intente nuevamente.")
            
        #else:
        #print("| ERROR | Opcion invalida. Ejecutando simulacion por defecto...")
        #print("| ¡ALERTA! | Iniciando simulacion del ejercicio...")
        #simular_ejemplo()"
            

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
            print(f"Amenaza {id_mision} clasificada como ALTA - Asignada a escuadrones elite")
        elif clasificacion == "Bajo":
            self.amenazas_bajas.append(amenaza)
            print(f"Amenaza {id_mision} clasificada como BAJA - Asignada para reconocimiento")
        elif clasificacion == "Falsa amenaza":
            amenaza.hora_archivado = amenaza.hora_recepcion
            self.historial.append(amenaza)
            print(f"Amenaza {id_mision} archivada como FALSA AMENAZA")
    
    def procesar_tiempo_transcurrido(self, hora_actual: datetime):
        """Procesa las amenazas que han superado su tiempo limite y las mueve al historial"""
        # Procesar amenazas altas (1 minuto)
        amenazas_altas_vencidas = []
        for amenaza in self.amenazas_altas:
            tiempo_transcurrido = hora_actual - amenaza.hora_recepcion
            if tiempo_transcurrido >= timedelta(minutes=1):
                amenaza.hora_archivado = amenaza.hora_recepcion + timedelta(minutes=1)
                amenazas_altas_vencidas.append(amenaza)
        
        for amenaza in amenazas_altas_vencidas:
            self.amenazas_altas.remove(amenaza)
            self.historial.append(amenaza)
        
        # Procesar amenazas bajas (3 minutos)
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
        
        print("\n" + "="*50)
        print("INFORME DE AMENAZAS - AGENCIA DE SEGURIDAD GLOBAL")
        print("="*50)
        
        print("\nLista de Amenazas Altas:")
        if self.amenazas_altas:
            for amenaza in self.amenazas_altas:
                print(f"  {amenaza}")
        else:
            print("  No hay amenazas altas pendientes")
        
        print("\nLista de Amenazas Bajas:")
        if self.amenazas_bajas:
            for amenaza in self.amenazas_bajas:
                print(f"  {amenaza}")
        else:
            print("  No hay amenazas bajas pendientes")
        
        print("\nHistorial:")
        if self.historial:
            for amenaza in self.historial:
                hora_archivado = amenaza.hora_archivado.strftime("%H:%M:%S")
                print(f"  {amenaza.id_mision} ({amenaza.clasificacion}), {hora_archivado}")
        else:
            print("  No hay amenazas en el historial")
        
        print("="*50)

def simular_ejemplo():
    """Simula el ejemplo proporcionado en el ejercicio"""
    sistema = SistemaASG()
    
    # Hora base para la simulacion
    hora_base = datetime.strptime("10:42:50", "%H:%M:%S")
    
    print("SIMULACION DEL EJEMPLO")
    print("="*30)
    
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
        
        print(f"Recibida: {id_mision} ({clasificacion}) a las {hora_str}")
    
    # Generar informe a las 10:45:00
    hora_informe = datetime.strptime("10:45:00", "%H:%M:%S")
    print(f"\nGenerando informe a las {hora_informe.strftime('%H:%M:%S')}")
    sistema.generar_informe(hora_informe)

def menu_interactivo():
    """Menu interactivo para usar el sistema"""
    sistema = SistemaASG()
    
    while True:
        print("\n" + "="*40)
        print("SISTEMA ASG - MENU PRINCIPAL")
        print("="*40)
        print("1. Recibir nueva denuncia")
        print("2. Generar informe")
        print("3. Simular ejemplo del ejercicio")
        print("4. Salir")
        
        opcion = input("\nSeleccione una opcion (1-4): ").strip()
        
        if opcion == "1":
            print("\n--- NUEVA DENUNCIA ---")
            id_mision = input("ID de la mision (ej: M123): ").strip()
            descripcion = input("Descripcion de la amenaza: ").strip()
            
            print("\nClasificaciones disponibles:")
            print("1. Alto")
            print("2. Bajo") 
            print("3. Falsa amenaza")
            
            while True:
                clasificacion_num = input("Seleccione clasificacion (1-3): ").strip()
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
                    print("Opcion invalida. Intente nuevamente.")
            
            sistema.recibir_denuncia(id_mision, descripcion, clasificacion)
        
        elif opcion == "2":
            hora_actual = datetime.now()
            sistema.generar_informe(hora_actual)
        
        elif opcion == "3":
            simular_ejemplo()
        
        elif opcion == "4":
            print("Saliendo del sistema ASG...")
            break
        
        else:
            print("Opcion invalida. Intente nuevamente.")

if __name__ == "__main__":
    print("SISTEMA DE ANALISIS DE RIESGOS")
    print("AGENCIA DE SEGURIDAD GLOBAL (ASG)")
    print("="*40)
    
    print("\nOpciones disponibles:")
    print("1. Menu interactivo")
    print("2. Ejecutar simulacion del ejemplo")
    
    modo = input("\nSeleccione modo (1-2): ").strip()
    
    if modo == "1":
        menu_interactivo()
    elif modo == "2":
        simular_ejemplo()
    else:
        print("Opcion invalida. Ejecutando simulacion por defecto...")
        simular_ejemplo()
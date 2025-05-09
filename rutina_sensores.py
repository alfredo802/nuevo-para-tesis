import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates
from sklearn.metrics import mean_absolute_percentage_error, confusion_matrix, precision_score, recall_score, f1_score
import seaborn as sns
from concurrent.futures import ProcessPoolExecutor
import sqlite3
from pathlib import Path
import logging
from datetime import datetime
import os

# Configurar el sistema de registro
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AnalizadorDatosSensores:
    def __init__(self, archivo_datos='datos/valpoall.txt', ubicacion='Valparaíso'):
        self.archivo_datos = archivo_datos
        self.ubicacion = ubicacion
        self.ruta_db = Path('database/datos_sensores.db')
        self.configurar_base_datos()
        
    def configurar_base_datos(self):
        """Inicializa las tablas de la base de datos"""
        self.ruta_db.parent.mkdir(exist_ok=True)
        with sqlite3.connect(str(self.ruta_db)) as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS resultados_analisis
                          (fecha_hora TEXT, ubicacion TEXT, sensor TEXT, 
                           promedio REAL, desv_std REAL, minimo REAL, maximo REAL)''')
            conn.execute('''CREATE TABLE IF NOT EXISTS historial_consultas
                          (fecha_hora TEXT, tipo_consulta TEXT, parametros TEXT)''')
    
    def cargar_datos(self):
        """Carga y preprocesa los datos de los sensores"""
        logger.info("Cargando datos de sensores...")
        try:
            self.datos = np.loadtxt(self.archivo_datos)
            self.procesar_timestamps()
            self.extraer_datos_sensores()
            return True
        except Exception as e:
            logger.error(f"Error al cargar datos: {e}")
            return False

    def procesar_timestamps(self):
        """Procesa los datos de tiempo"""
        aa, mm, dd, hh = self.datos[:, 0], self.datos[:, 1], self.datos[:, 2], self.datos[:, 3]
        self.tiempo = [datetime(int(y), int(m), int(d), int(h)) 
                      for y, m, d, h in zip(aa, mm, dd, hh)]

    def extraer_datos_sensores(self):
        """Extrae y preprocesa los datos de los sensores"""
        self.prs = self.datos[:, 4]  # Sensor Keller
        self.rad = self.datos[:, 5]  # Sensor Vega
        self.ta = self.datos[:, 6]   # Temperatura del aire
        self.bp = self.datos[:, 7]   # Presión atmosférica
        self.rh = self.datos[:, 8]   # Humedad relativa
        self.tw = self.datos[:, 9]   # Temperatura del agua
        
        # Calcular promedios para normalización
        self.prsnm = np.nanmean(self.prs)
        self.radnm = np.nanmean(self.rad)

    def graficar_todos_sensores(self):
        """Crea gráfico combinado para todos los sensores"""
        logger.info("Generando gráfico combinado de sensores...")
        fig, axes = plt.subplots(3, 2, figsize=(15, 12))
        fig.suptitle(f'Análisis de Datos de Sensores - {self.ubicacion}', fontsize=16)
        
        graficos = [
            (self.prs, 'Sensor Keller', 'Altura (m)'),
            (self.rad, 'Sensor Vega', 'Altura (m)'),
            (self.ta, 'Temperatura Aire', 'Temperatura (°C)'),
            (self.bp, 'Presión Atmosférica', 'Presión (mbar)'),
            (self.rh, 'Humedad Relativa', '%'),
            (self.tw, 'Temperatura Agua', 'Temperatura (°C)')
        ]
        
        for (datos, titulo, etiqueta_y), ax in zip(graficos, axes.flat):
            ax.plot(self.tiempo, datos)
            ax.set_title(titulo)
            ax.set_ylabel(etiqueta_y)
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%y'))
            
        plt.tight_layout()
        plt.savefig('resultados/graficos_sensores.png', dpi=300, bbox_inches='tight')
        plt.close()

    def analizar_datos_sensores(self):
        """Realiza análisis estadístico de los datos de los sensores"""
        logger.info("Realizando análisis estadístico...")
        sensores = {
            'Keller': self.prs,
            'Vega': self.rad,
            'Temperatura_Aire': self.ta,
            'Presion_Atmosferica': self.bp,
            'Humedad_Relativa': self.rh,
            'Temperatura_Agua': self.tw
        }
        
        with sqlite3.connect(str(self.ruta_db)) as conn:
            for nombre_sensor, datos in sensores.items():
                estadisticas = {
                    'promedio': np.nanmean(datos),
                    'desv_std': np.nanstd(datos),
                    'minimo': np.nanmin(datos),
                    'maximo': np.nanmax(datos)
                }
                
                conn.execute('''INSERT INTO resultados_analisis 
                              VALUES (?, ?, ?, ?, ?, ?, ?)''',
                           (datetime.now().isoformat(), self.ubicacion, nombre_sensor,
                            estadisticas['promedio'], estadisticas['desv_std'], 
                            estadisticas['minimo'], estadisticas['maximo']))

    def graficar_matriz_correlacion(self):
        """Genera mapa de calor de la matriz de correlación"""
        logger.info("Generando matriz de correlación...")
        datos_sensores = pd.DataFrame({
            'Keller': self.prs,
            'Vega': self.rad,
            'Temp_Aire': self.ta,
            'Presion': self.bp,
            'Humedad': self.rh,
            'Temp_Agua': self.tw
        })
        
        matriz_corr = datos_sensores.corr()
        plt.figure(figsize=(10, 8))
        sns.heatmap(matriz_corr, annot=True, cmap='coolwarm', center=0)
        plt.title('Matriz de Correlación - Datos de Sensores')
        plt.tight_layout()
        plt.savefig('resultados/matriz_correlacion.png', dpi=300, bbox_inches='tight')
        plt.close()

    def ejecutar_analisis(self):
        """Ejecuta el pipeline completo de análisis"""
        if not self.cargar_datos():
            return False
            
        # Ejecutar tareas secuencialmente
        logger.info("Iniciando análisis secuencial...")
        
        # 1. Generar gráfico de todos los sensores
        logger.info("Paso 1: Generando gráfico combinado de sensores...")
        self.graficar_todos_sensores()
        
        # 2. Realizar análisis estadístico
        logger.info("Paso 2: Realizando análisis estadístico...")
        self.analizar_datos_sensores()
        
        # 3. Generar matriz de correlación
        logger.info("Paso 3: Generando matriz de correlación...")
        self.graficar_matriz_correlacion()
            
        logger.info("Análisis completado exitosamente")
        return True

def main():
    """Función principal que ejecuta el análisis de sensores"""
    # Crear directorio de resultados si no existe
    os.makedirs('resultados', exist_ok=True)
    
    # Instanciar y ejecutar el analizador
    analizador = AnalizadorDatosSensores()
    return analizador.ejecutar_analisis()

if __name__ == "__main__":
    main() 
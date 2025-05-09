import os
import shutil
import logging
import time
from datetime import datetime

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('analisis_completo.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def ejecutar_analisis_completo():
    # Crear directorios necesarios
    for dir_name in ['resultados', 'reportes', 'database', 'datos_procesados']:
        os.makedirs(dir_name, exist_ok=True)
    
    start_time = time.time()
    logging.info(f"Iniciando ejecución completa: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logging.info("=" * 50)
    
    # 1. Análisis básico de sensores
    logging.info("INICIANDO ANÁLISIS BÁSICO DE SENSORES")
    logging.info("=" * 50)
    try:
        import rutina_sensores
        rutina_sensores.main()
        logging.info("[OK] Análisis básico de sensores completado exitosamente")
    except Exception as e:
        logging.error(f"[ERROR] Error en análisis básico: {str(e)}")
    
    # 2. Control de calidad
    logging.info("=" * 50)
    logging.info("INICIANDO CONTROL DE CALIDAD")
    logging.info("=" * 50)
    try:
        # Copiar el archivo en lugar de crear enlace simbólico
        if not os.path.exists('valpoall.txt'):
            if os.path.exists('datos/valpoall.txt'):
                shutil.copy2('datos/valpoall.txt', 'valpoall.txt')
            else:
                logging.error("[ERROR] Archivo valpoall.txt no encontrado en datos/")
                raise FileNotFoundError("Archivo valpoall.txt no encontrado")
        
        import control_calidad
        control_calidad.main()
        logging.info("[OK] Control de calidad completado exitosamente")
    except Exception as e:
        logging.error(f"[ERROR] Error en control_calidad: {str(e)}")
    
    # 3. Análisis de pronósticos
    logging.info("=" * 50)
    logging.info("INICIANDO ANÁLISIS DE PRONÓSTICOS")
    logging.info("=" * 50)
    try:
        # Asegurar que existe el directorio de datos procesados
        if not os.path.exists('datos_procesados'):
            os.makedirs('datos_procesados')
        
        import scripts.pronostico_sensores as pronostico
        pronostico.main()
        logging.info("[OK] Análisis de pronósticos completado exitosamente")
    except Exception as e:
        logging.error(f"[ERROR] Error en el análisis de pronósticos: {str(e)}")
    
    # Resumen final
    end_time = time.time()
    logging.info("=" * 50)
    logging.info("RESUMEN DE EJECUCIÓN")
    logging.info("=" * 50)
    logging.info(f"Tiempo total de ejecución: {end_time - start_time:.2f} segundos")
    
    # Verificar resultados
    rutina_ok = any([
        os.path.exists('resultados/graficos_sensores.png'),
        os.path.exists('resultados/todos_sensores_combinado.png'),
        os.path.exists('resultados/matriz_correlacion.png')
    ])
    
    control_ok = any([
        os.path.exists('resultados/Control_Calidad.png'),
        os.path.exists('resultados/control_calidad.png'),
        os.path.exists('resultados/correlacion_sensores.png'),
        os.path.exists('resultados/control_sensor_keller.png'),
        os.path.exists('resultados/control_sensor_vega.png')
    ])
    
    pronostico_ok = any([
        os.path.exists('resultados/pronostico_keller.png'),
        os.path.exists('resultados/pronostico_vega.png'),
        os.path.exists('resultados/pronostico_presion.png'),
        os.path.exists('resultados/pronostico_temp_aire.png'),
        os.path.exists('resultados/pronostico_temp_agua.png'),
        os.path.exists('resultados/pronostico_humedad.png')
    ])
    
    logging.info(f"rutina_sensores: [{'OK' if rutina_ok else 'ERROR'}] {'Completado' if rutina_ok else 'Fallido'}")
    logging.info(f"control_calidad: [{'OK' if control_ok else 'ERROR'}] {'Completado' if control_ok else 'Fallido'}")
    logging.info(f"pronosticos: [{'OK' if pronostico_ok else 'ERROR'}] {'Completado' if pronostico_ok else 'Fallido'}")
    
    if not all([rutina_ok, control_ok, pronostico_ok]):
        logging.error("\n[ERROR] Algunos análisis fallaron")
    else:
        logging.info("\n[OK] Todos los análisis se completaron exitosamente")

if __name__ == "__main__":
    ejecutar_analisis_completo() 
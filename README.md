# Análisis de Sensores de Marea

Este proyecto realiza el análisis y control de calidad de datos de sensores de marea (Keller y Vega).

## Estructura del Proyecto

```
proyecto/
├── datos/               # Archivos de datos de entrada
│   ├── valpoall.txt    # Datos de Valparaíso
│   └── ancudall.txt    # Datos de Ancud
├── scripts/            # Scripts de Python
│   ├── rutina_sensores.py     # Análisis básico de sensores
│   ├── control_calidad.py     # Control de calidad
│   └── ejecutar_analisis.py   # Script principal
├── resultados/         # Gráficos y resultados
└── reportes/          # Reportes generados
```

## Requisitos

- Python 3.x
- Bibliotecas requeridas:
  - numpy
  - matplotlib
  - seaborn
  - scipy

## Instalación

1. Instalar las dependencias:
```bash
python -m pip install numpy matplotlib seaborn scipy
```

## Uso

1. Colocar los archivos de datos en la carpeta `datos/`

2. Ejecutar el análisis completo:
```bash
python scripts/ejecutar_analisis.py
```

Este script ejecutará en secuencia:
1. `rutina_sensores.py`: Análisis básico de los sensores
2. `control_calidad.py`: Control de calidad detallado

## Resultados

Los resultados se guardarán en:
- `resultados/`: Gráficos y visualizaciones
- `reportes/`: Reportes detallados en formato texto

## Archivos Generados

### Gráficos
- `analisis_sensores.png`: Análisis general de los sensores
- `diferencia_sensores.png`: Diferencia entre sensores
- `correlacion_sensores.png`: Correlación entre sensores
- `control_sensor_keller.png`: Gráfico de control para Keller
- `control_sensor_vega.png`: Gráfico de control para Vega

### Reportes
- `reporte_control_calidad.txt`: Reporte detallado del análisis 
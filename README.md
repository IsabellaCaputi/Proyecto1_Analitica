# Dashboard Análisis Pruebas Saber 11 - Atlántico

Un proyecto de análisis y visualización interactiva de datos de las Pruebas Saber 11 en la región del Atlántico, desarrollado para la materia de Analítica Computacional para la Toma de Decisiones.

---

## Descripción del Proyecto

Este proyecto implementa un dashboard interactivo que permite explorar y analizar los resultados de las Pruebas Saber 11 en el departamento del Atlántico. Incluye procesos de limpieza de datos, análisis exploratorio y visualizaciones interactivas construidas con **Dash** y **Plotly**.

### Características Principales

- **Dashboard Interactivo** - Visualizaciones dinámicas con filtros por estrato socioeconómico
- **Limpieza de Datos** - Procesos ETL documentados en notebooks Jupyter
- **Análisis Multidimensional** - Análisis de desempeño por materia y variables socioeconómicas
- **Deploy Ready** - Estructura lista para despliegue en producción
- **Datos Estructurados** - CSV limpios y procesados para análisis

---

## 📁 Estructura del Proyecto

```
Proyecto1_Analitica/
│
├── README.md                                          # Este archivo
├── Tarea 3 - Exploracion y analisis de datos.ipynb   # Análisis exploratorio de datos
├── Tarea 4 - Dashboard.py                            # Dashboard principal
│
├── 📂 Tarea 2 - Limpieza_Datos/
│   └── limpieza_proyecto1.ipynb                      # Notebook con proceso ETL
│
├── 📂 Tarea 6 - Despliegue/
│   └── Dashboard.py                                  # Versión de despliegue del dashboard
│
├── 📂 Datos_Salida_Extraccion/
│   ├── Datos_AWS_Atlantico.csv                       # Datos originales de AWS
│   └── saber11_limpio.csv                            # Datos limpios y procesados
│
└── 📂 Soportes/
    ├── Soporte_AnalisisDeDatos_Proyecto1.ipynb       # Material de soporte y referencias
    └── Soporte Despligue/                            # Documentación de despliegue

```

### Descripción de Directorios

| Directorio | Descripción |
|-----------|-----------|
| **Tarea 2 - Limpieza_Datos/** | Notebook Jupyter con el proceso de limpieza y transformación de datos (ETL) |
| **Tarea 6 - Despliegue/** | Dashboard listo para producción y documentación de despliegue |
| **Datos_Salida_Extraccion/** | Datos fuente (originales de AWS) y datos limpios en formato CSV |
| **Soportes/** | Material de soporte académico, referencias y documentación técnica |

---

## Dependencias

El proyecto requiere las siguientes librerías Python:

### Librerías Principales

| Librería | Versión | Propósito |
|----------|---------|----------|
| **pandas** | ≥1.0.0 | Manipulación y análisis de datos |
| **dash** | ≥2.0.0 | Framework web para dashboard interactivo |
| **plotly** | ≥5.0.0 | Visualizaciones interactivas |
| **numpy** | ≥1.19.0 | Computación numérica |

## Equipo de Desarrollo

| Integrante | Rol |
|-----------|-----|
| **Isabella Caputi** | Análisis de negocio, Análisis de datos, Ingeniería de datos |
| **Sofia Vásquez** | Análisis de negocio, Análisis de datos, Despliegue y mantenimiento |
| **Maria Paula Ospina** | Análisis de negocio, Análisis de datos, Tablero de datos |

---

## Contexto Académico

- **Materia**: Analítica Computacional para la Toma de Decisiones
- **Departamento**: Ingeniería Industrial
- **Universidad**: Universidad de los Andes
- **Año**: 2025


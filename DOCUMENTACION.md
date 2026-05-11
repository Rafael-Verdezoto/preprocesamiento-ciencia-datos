# DOCUMENTACIÓN TÉCNICA
## Proyecto: preprocesamiento-cienciadatos
### Universidad Nacional de Chimborazo — Facultad de Ingeniería
**Materia:** Cultura Digital y Sociedad  
**Unidad:** 2 — Herramientas y Metodologías en Ciencia de Datos  

## 1. Introducción

### Objetivo del Proyecto
El proyecto **preprocesamiento-cienciadatos** tiene como propósito aplicar de manera práctica el control de versiones con Git y GitHub en el contexto de un proyecto real de Ciencia de Datos. Paralelamente, se implementa un pipeline completo de preprocesamiento de datos usando la biblioteca **Pandas** de Python.

### Funcionalidades Implementadas
El script `scripts/preprocesamiento.py` contiene las siguientes funciones:

| Función | Descripción |
|---|---|
| `cargar_dataset(ruta)` | Carga un archivo CSV como DataFrame |
| `crear_dataset_ejemplo()` | Genera un dataset sintético con nulos y duplicados |
| `explorar_dataset(df)` | Muestra información general, tipos y estadísticas |
| `eliminar_duplicados(df)` | Elimina filas repetidas y resetea el índice |
| `manejar_valores_nulos(df, ...)` | Rellena nulos numéricos (media/mediana) y categóricos (moda) |
| `normalizar_columnas(df, columnas)` | Escala columnas al rango [0, 1] con MinMaxScaler |
| `codificar_categoricas(df, cols, metodo)` | Aplica Label Encoding u One-Hot Encoding |
| `preprocesar_dataset(df, ...)` | Pipeline completo que ejecuta los pasos anteriores |

## 2. Comandos Git Utilizados

### Configuración inicial

```bash
# Configurar identidad del usuario (una sola vez por máquina)
git config --global user.name "Rafael Verdezoto"
git config --global user.email "rafael.verdezoto@unach.edu.ec"
```
**Propósito:** Asociar cada commit con el nombre y correo del autor.

### Clonar el repositorio

```bash
git clone https://github.com/TU_USUARIO/preprocesamiento-cienciadatos.git
cd preprocesamiento-cienciadatos
```
**Propósito:** Descargar una copia completa del repositorio remoto en la máquina local.

### Commit inicial

```bash
git add README.md .gitignore
git commit -m "Inicio del proyecto: README y .gitignore"
git push origin main
```
**Propósito:** Registrar el primer estado del proyecto con los archivos base.

### Crear y cambiar de rama

```bash
git checkout -b feature-preprocesamiento
```
**Propósito:** Crear una rama de trabajo aislada para desarrollar la funcionalidad de preprocesamiento sin afectar la rama `main`.

### Agregar cambios y hacer commit en la rama

```bash
git add scripts/preprocesamiento.py
git commit -m "Agregar función para preprocesamiento completo de datos"
git push origin feature-preprocesamiento
```
**Propósito:** Guardar el progreso del script en el historial de Git y subir los cambios al repositorio remoto.


### Pull Request y fusión

```bash
# Después de aprobar el Pull Request en GitHub:
git checkout main
git merge feature-preprocesamiento
git push origin main
```
**Propósito:** Integrar el trabajo de la rama `feature-preprocesamiento` a la rama principal `main` tras revisión.


### Eliminar la rama tras la fusión

```bash
# Eliminar rama local
git branch -d feature-preprocesamiento

# Eliminar rama remota
git push origin --delete feature-preprocesamiento
```
**Propósito:** Mantener el repositorio limpio eliminando ramas que ya fueron fusionadas.


### Verificar estado e historial

```bash
# Ver el estado actual del área de trabajo
git status

# Ver el historial de commits
git log --oneline --graph --all
```
**Propósito:** Monitorear qué archivos han cambiado y visualizar la historia de commits en forma gráfica.


## 3. Automatización con GitHub Actions

### Descripción del Workflow (`.github/workflows/ci.yml`)

El archivo `ci.yml` define un **workflow de integración continua (CI)** que se activa automáticamente en dos situaciones:

- Cuando se realiza un **push** a `main` o `feature-preprocesamiento`.
- Cuando se abre o actualiza un **Pull Request** hacia `main`.

### Pasos del Workflow

| Paso | Acción | Propósito |
|---|---|---|
| 1 | `actions/checkout@v3` | Clona el repositorio dentro del runner |
| 2 | `actions/setup-python@v4` | Instala Python 3.11 en el entorno |
| 3 | `pip install pandas numpy scikit-learn` | Instala las dependencias necesarias |
| 4 | `python scripts/preprocesamiento.py` | Ejecuta el script y verifica que no haya errores |
| 5 | `flake8 ...` | Revisa el estilo del código (PEP 8) |
| 6 | `echo " ..."` | Confirma la ejecución exitosa |

### Beneficios del CI
- Detecta errores automáticamente antes de fusionar código.
- Garantiza que el script siempre sea ejecutable.
- Fomenta buenas prácticas de calidad de código.


## 4. Capturas de Pantalla

### Creación del repositorio en GitHub
<img width="1890" height="1002" alt="image" src="https://github.com/user-attachments/assets/1fb9487c-3bcf-4e1f-92f5-aec354e268d6" />

###  Creación de la rama `feature-preprocesamiento`
<img width="1919" height="979" alt="image" src="https://github.com/user-attachments/assets/91ee22d0-da18-43b3-9d91-d2c0efed83ec" />

###  GitHub Actions
<img width="1919" height="971" alt="image" src="https://github.com/user-attachments/assets/eadc752b-6f6c-4e3b-bbc9-ee7183159172" />


## 5. Bibliografía

- Chacon, S., & Straub, B. (2014). *Pro Git*. Apress. Disponible en: https://git-scm.com/book/es/v2  
- McKinney, W. (2018). *Python for Data Analysis* (2.ª ed.). O'Reilly Media.  
- Pandas Development Team. (2024). *pandas documentation*. https://pandas.pydata.org/docs/  
- GitHub. (2024). *GitHub Actions documentation*. https://docs.github.com/en/actions  

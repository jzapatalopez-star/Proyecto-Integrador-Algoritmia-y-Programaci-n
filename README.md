# SIPA: SISTEMA INTEGRAL DE PROTECCIONES ANIMALES

**Informe del Proyecto Integrador y Documentación Técnica de Software**

Julieth Andrea Zapata López, Anlli Paola Rojas Rúa, Alba Milena Castro y Alejandra Zuluaga Cardona

Facultad de Ingeniería, Departamento de Ingeniería Industrial, Universidad de Antioquia

Curso 2026-2: Algoritmia y Programación

Profesor John Heider Dávila

17 de septiembre de 2026

## 1. Integrantes

El equipo de trabajo está conformado por Anlli Rojas Rúa, Alba Milena Castro, Alejandra Zuluaga Cardona, y Julieth Andrea Zapata López quienes participan en las diferentes etapas de análisis, diseño, desarrollo y documentación del proyecto.

## 2. Vínculos académicos y descripción

### Julieth Andrea Zapata López

Estudiante de Ingeniería Industrial de 25 años, residente en el municipio de Bello. Se caracteriza por ser una persona responsable, perseverante, comprometida y con atención al detalle, con disposición para aprender y mejorar. Actualmente en proceso de formación y fortalecimiento de habilidades relacionadas con el análisis y mejoramiento de procesos, la organización, la planificación y la resolución de problemas. Tiene interés en comprender a profundidad las situaciones que analiza, identificar y desarrollar oportunidades de mejora.

### Anlli Paola Rojas Rúa

Estudiante de Ingeniería Industrial de 19 años, residente en el municipio de Santa Rosa de Osos. Se distingue por una marcada pasión por la adquisición continua de conocimiento, una gran capacidad analítica y un firme compromiso con la excelencia académica. En su etapa actual de formación, enfoca su desarrollo profesional hacia el dominio del idioma inglés, la lógica de programación y el análisis de datos, integrando estas herramientas técnicas con el diseño y la gestión eficiente de procesos industriales.

### Alba Milena Castro

Estudiante de Ingeniería Industrial de 43 años, residente en el municipio de Girardota. Se distingue por su rigor metodológico, alta responsabilidad y constante pasión por el aprendizaje. Posee capacidad analítica para la formulación de proyectos, con un firme compromiso laboral y académico. En su etapa actual de formación, profundiza en la lógica de programación y el análisis de datos. Su visión trasciende la ejecución operativa de procesos, priorizando su diseño estratégico para impulsar la competitividad organizacional.

### Alejandra Zuluaga Cardona

Estudiante de Ingeniería Industrial, de 23 años, reside en el municipio del Carmen de Viboral, Antioquia. Se distingue por ser una persona curiosa, perseverante y comprometida con su aprendizaje. Le interesa comprender las situaciones, analizar diferentes perspectivas y encontrar soluciones prácticas. En su formación ha desarrollado interés por el análisis y mejoramiento de procesos, la organización y la planificación, buscando asumir nuevos retos que le permitan fortalecer sus capacidades.

## 3. Nombre del proyecto y detalles

**Nombre del sistema:** SIPA (Sistema Integral de Protecciones Animales).

**Descripción:** SIPA constituye una solución informática desarrollada en la plataforma Python, concebida para la sistematización y gestión organizada de las Peticiones, Quejas, Reclamos y Sugerencias (PQRS) dirigidas al cuidado de la fauna doméstica (perros y gatos) en la Universidad de Antioquia. La herramienta sustituye los esquemas de registro manuales mediante el uso de cuatro estructuras independientes de datos persistentes en archivos planos, un validador integral de campos de entrada, un módulo de generación de radicación ASCII estandarizado a 120 caracteres horizontales y un panel analítico estadístico.
<img width="522" height="505" alt="LOGOSIPAALGORITMIA" src="https://github.com/user-attachments/assets/7963d331-1ace-40ba-bd42-42b33c6bebe3" />

## 4. Licencia del software

SIPA © 2026 por [Anlli Rojas, Milena Castro, Julieth Zapata, Alejandra Zuluaga] tiene la licencia [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/?ref=chooser-v1).

![CC BY-NC-SA 4.0](https://mirrors.creativecommons.org/presskit/buttons/88x31/png/by-nc-sa.png)

## 5. Reporte de visión

### Descripción general del software

SIPA fue conceptualizado para resolver la ineficiencia operativa generada por el diligenciamiento en físico de PQRS dentro del campus universitario; el sistema proporciona un entorno en consola altamente estable que garantiza el seguimiento preciso de las solicitudes canalizadas hacia las dependencias veterinarias correspondientes.

### Objetivos y beneficios del Sistema

- Establecer una secuencia numérica de carácter incremental, por cada tipo de documento de PQRS registrado.
- Asegurar el cumplimiento de los términos legales máximos para la respuesta, que se equivalen a 30 días calendario contados desde la radicación.
- Estructurar la persistencia de datos en los archivos físicos Peticion.txt, Queja.txt, Reclamo.txt y Sugerencia.txt.
- Entregar métricas de desempeño sobre la efectividad institucional por sede académica y especie animal.

## 6. Especificación de requisitos

### Requisitos Funcionales (RF)

| Identificador | Denominación | Regla de Negocio y Alcance Operativo |
|---|---|---|
| RF-01 | Secuencia Radicadora | Asignación automática de identificador numérico entero, iniciando en 1 para cada tipología documental. |
| RF-02 | Validación del Usuario | Comprobación estricta de formato: Nombres (3-100 caracteres alfabéticos); Documentos autorizados (CC, TI, CE, PP, NIT; 3-15 dígitos); Teléfono (10 caracteres numéricos); Correo (estándar con @ y extensión válida); Dirección (opcional, 5-200 caracteres). |
| RF-03 | Validación de la PQRS | Control sobre tipología (Petición, Queja, Reclamo, Sugerencia); Fecha mediante módulo datetime (sin fechas futuras); Canal de recepción oficial; Asunto (5-150 caracteres); Descripción detallada (20-2000 caracteres). |
| RF-04 | Atributos Específicos | Clasificación de especie (Perro o Gato) y asignación al campus universitario correspondiente entre las sedes oficiales declaradas. |
| RF-05 | Tiempos y Ciclo de Vida | Cálculo dinámico de la fecha límite (Fecha actual + 30 días). Transición regulada de estados: Registrada → En proceso → Solucionada. |
| RF-06 | Persistencia Plana | Almacenamiento delimitado por caracteres especiales en 4 archivos independientes en la ruta data/. |
| RF-07 | Radicado ASCII | Impresión de comprobante con marco estructural ASCII a 120 caracteres de ancho exacto, omitiendo campos extensos para optimizar espacio. |
| RF-08 | Módulo Estadístico | Generación del indicador obligatorio de días promedio de respuesta y cinco mediciones analíticas complementarias. |

### Requisitos No Funcionales (RNF)

- **RNF-01 (Arquitectura Modular):** Código fuente separado en archivos especializados (validaciones.py, archivos.py, reportes.py.
- **RNF-02 (Estándar Repositorio):** Estructuración del proyecto en las carpetas src/, docs/, images/ y data/ dentro del entorno GitHub.
- **RNF-03 (Usabilidad en Consola):** Interfaz textual interactiva, clara y guiada mediante menú principal.

## 7. Plan de proyecto

### Diagrama de Gantt
<img width="1295" height="370" alt="Diagrama de Gantt SIPA algoritmia" src="https://github.com/user-attachments/assets/41c8997a-114b-488e-ba46-f44a57aa71f1" />

### Presupuesto del proyecto
<img width="1022" height="222" alt="PresupuestoproyectoSIPA" src="https://github.com/user-attachments/assets/12c03576-53e2-41fa-9fe7-cc8d7045c2cf" />


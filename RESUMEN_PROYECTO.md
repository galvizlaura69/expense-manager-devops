# 📄 Resumen del Proyecto — Expense Manager DevOps

Este documento explica qué se ha hecho en el proyecto, cómo se ha construido paso a paso a partir de los commits reales del repositorio, y cuál es el estado actual del código. Está basado exclusivamente en el historial de Git y en el código fuente presente en la rama `develop`.

---

## 1. ¿Qué es este proyecto?

**Expense Manager** es una aplicación web para la gestión de ingresos y gastos personales desarrollada con **Django 5.2** y **Python 3.12**. Permite a usuarios autenticados:

- Crear y gestionar categorías de ingresos y gastos.
- Registrar, editar, listar y eliminar movimientos financieros.
- Consultar un dashboard con el resumen de ingresos totales, gastos totales y balance disponible.
- Mantener la información separada por usuario.

Además, incorpora prácticas DevOps: contenedorización con Docker, pipeline de CI/CD con Jenkins y organización de ramas bajo GitFlow.

---

## 2. Historial de desarrollo (según commits de Git)

El proyecto se construyó de forma incremental. A continuación se detalla cada entrega registrada en el historial de la rama `develop`:

| Commit | Tipo | Descripción | Archivos afectados |
|--------|------|-------------|--------------------|
| `db26a09` | feat | Inicialización del proyecto Django base | `manage.py`, `config/`, `expenses/` |
| `3681b86` | feat | Creación de modelos de datos: `Category` y `Transaction` | `expenses/models.py` |
| `41aba0c` | feat | Implementación del CRUD de categorías (vistas, URLs, formularios) | `expenses/views.py`, `expenses/forms.py`, `expenses/urls.py`, plantillas |
| `14baee8` | feat | Implementación del CRUD de transacciones financieras | `expenses/views.py`, `expenses/forms.py`, plantillas |
| `ba19b3c` | feat | Dashboard financiero con resumen de balance, ingresos y gastos | `expenses/views.py`, `templates/expenses/dashboard.html` |
| `c8a44ad` | test | Pruebas unitarias para la gestión financiera | `expenses/tests.py` |
| `ae35fe8` | build | Contenedorización de la aplicación con Docker | `Dockerfile`, `docker-compose.yml`, `.dockerignore`, `config/settings.py` |
| `45568ee` | ci | Pipeline de Jenkins para pruebas y despliegue automatizado | `Jenkinsfile`, `Dockerfile.jenkins` |
| `a193705` | fix | Corrección de importaciones en `settings.py` | `config/settings.py` |
| `a1ff0b8` / `fa59b10` | feat | Documentación completa en README | `README` |
| `3922b83` | fix | Corrección de comandos Docker en Jenkinsfile | `Jenkinsfile` |
| `6f0b8ab` / `3da7f0e` / `5da0fd2` | fix | Habilitación y ajuste de la etapa de despliegue en Jenkins | `Jenkinsfile` |
| `6685b2d` | fix | **Actualización de diseño de interfaz (UI/UX)** | `static/css/style.css`, `templates/base.html`, todas las plantillas HTML, `config/settings.py`, `DOCUMENTACION_DISEÑO_INTERFAZ.md` |

### Último commit (`6685b2d` — fix: design update)

Este es el cambio más reciente y el enfoque de la intervención actual:

- **Creación de `static/css/style.css`**: hoja de estilos propia con tema verde y blanco, gradientes, sombras, componentes reutilizables (botones, tarjetas, tablas, badges, estados vacíos) y animaciones de entrada para alertas.
- **Creación de `templates/base.html`**: layout maestro con navegación fija, área de mensajes flash (éxito/error) y pie de página.
- **Rediseño de todas las plantillas** (`dashboard`, `transaction_list`, `transaction_form`, `transaction_confirm_delete`, `category_list`, `category_form`, `category_confirm_delete`, `login`) heredando de `base.html`.
- **Ajuste en `config/settings.py`**: se agregó `STATICFILES_DIRS` para servir los archivos estáticos (CSS).
- **Creación de `DOCUMENTACION_DISEÑO_INTERFAZ.md`**: documentación del flujo y decisiones de diseño.

> **Importante:** este commit no modificó la lógica de negocio (`models.py`, `views.py`, `forms.py`, `urls.py`). Solo mejoró la capa de presentación y la documentación de interfaz.

---

## 3. Estructura actual del proyecto

```
expense-manager-devops/
├── config/                 # Configuración de Django (settings, urls, wsgi, asgi)
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── expenses/               # App principal de gestión de gastos
│   ├── models.py           # Modelos: Category, Transaction
│   ├── views.py            # Vistas: dashboard, CRUD categorías y transacciones
│   ├── forms.py            # Formularios Django (CategoryForm, TransactionForm)
│   ├── urls.py             # Rutas de la aplicación
│   ├── admin.py            # Registro en admin de Django
│   ├── tests.py            # Pruebas unitarias
│   └── migrations/         # Migraciones de base de datos
├── templates/              # Plantillas HTML
│   ├── base.html           # Layout maestro (nuevo)
│   ├── expenses/
│   │   ├── dashboard.html
│   │   ├── transaction_list.html
│   │   ├── transaction_form.html
│   │   ├── transaction_confirm_delete.html
│   │   ├── category_list.html
│   │   ├── category_form.html
│   │   └── category_confirm_delete.html
│   └── registration/
│       └── login.html
├── static/                 # Archivos estáticos
│   └── css/
│       └── style.css       # Diseño verde/blanco con gradientes (nuevo)
├── Dockerfile              # Imagen de producción
├── Dockerfile.jenkins      # Imagen para entorno Jenkins
├── docker-compose.yml      # Orquestación de servicios
├── Jenkinsfile             # Pipeline CI/CD
├── manage.py
├── requirements.txt
└── README
```

---

## 4. Modelo de datos

La base de datos (SQLite) consta de dos modelos principales:

### Category
- `name`: nombre de la categoría.
- `type`: tipo (`INCOME` o `EXPENSE`).
- `user`: usuario propietario (clave foránea a `User` de Django).
- `created_at`: fecha de creación automática.
- Restricción única: un usuario no puede tener dos categorías con el mismo nombre y tipo.

### Transaction
- `description`: descripción del movimiento.
- `amount`: monto decimal positivo (validado por constraint de base de datos).
- `date`: fecha del movimiento.
- `category`: categoría asociada (protegida contra eliminación si tiene transacciones).
- `user`: usuario propietario.
- `created_at`: fecha de creación automática.
- Ordenamiento: por fecha descendente.

---

## 5. Flujo de la aplicación

El usuario autenticado sigue este recorrido:

```
Login → Dashboard → Movimientos / Categorías → Login (cerrar sesión)
```

### Rutas principales

| Ruta | Vista | Acción |
|------|-------|--------|
| `/` | `dashboard` | Resumen financiero (ingresos, gastos, balance) |
| `/categories/` | `category_list` | Listar categorías |
| `/categories/create/` | `category_create` | Crear categoría |
| `/categories/<int:pk>/edit/` | `category_update` | Editar categoría |
| `/categories/<int:pk>/delete/` | `category_delete` | Eliminar categoría |
| `/transactions/` | `transaction_list` | Listar movimientos |
| `/transactions/create/` | `transaction_create` | Registrar movimiento |
| `/transactions/<int:pk>/edit/` | `transaction_update` | Editar movimiento |
| `/transactions/<int:pk>/delete/` | `transaction_delete` | Eliminar movimiento |
| `/accounts/login/` | Django auth | Iniciar sesión |

Todas las vistas requieren autenticación (`@login_required`) y filtran los datos por el usuario autenticado (`user=request.user`).

---

## 6. Diseño de interfaz (intervención reciente)

La última entrega (`6685b2d`) se centró exclusivamente en mejorar la experiencia visual sin alterar la lógica:

### Paleta de colores
- **Verde principal** (`#10b981`): botones, acentos, elementos activos.
- **Verde oscuro** (`#047857`): títulos y textos de marca.
- **Fondo degradado**: verde muy claro → blanco → verde muy claro (`linear-gradient(135deg, #ecfdf5, #ffffff, #f0fdf4)`).
- **Blanco**: tarjetas y superficies elevadas.
- **Éxito**: fondo verde claro, ícono de check.
- **Error**: fondo rojo claro, ícono de alerta.

### Componentes implementados
- Navbar fija con efecto vidrio esmerilado (`backdrop-filter`).
- Tarjetas de métricas en el dashboard (ingresos, gastos, balance).
- Tablas con filas zebra, hover y badges de tipo (ingreso/gasto).
- Formularios centrados con validación visual y mensajes de error inline.
- Estados vacíos con ilustraciones SVG y botones de acción clara.
- Alertas de éxito y error con animación de entrada (`slideIn`).
- Diseño responsive para móviles.

---

## 7. Stack tecnológico y DevOps

| Tecnología | Uso |
|------------|-----|
| Python 3.12 | Lenguaje de programación |
| Django 5.2 | Framework web |
| SQLite | Base de datos |
| HTML / CSS | Interfaz de usuario |
| Docker | Contenedorización |
| Docker Compose | Administración de servicios |
| Jenkins | Pipeline CI/CD |
| Git / GitHub | Control de versiones |
| GitFlow | Organización de ramas |
| Gunicorn | Servidor de aplicación |
| WhiteNoise | Gestión de archivos estáticos |

### Pipeline CI/CD (Jenkins)
El `Jenkinsfile` define las etapas:
1. **Checkout**: obtiene el código del repositorio.
2. **Build Docker Image**: construye la imagen de la aplicación.
3. **Django Check**: verifica la configuración de Django.
4. **Run Tests**: ejecuta las pruebas automatizadas.
5. **Deploy**: despliega cuando se trabaja sobre la rama `main`.

---

## 8. Cómo ejecutar el proyecto

### Localmente
```bash
# Clonar y entrar al repositorio
git clone URL_DEL_REPOSITORIO
cd expense-manager-devops

# Entorno virtual
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/macOS

# Dependencias
pip install -r requirements.txt

# Migraciones
python manage.py migrate

# Superusuario (opcional)
python manage.py createsuperuser

# Servidor de desarrollo
python manage.py runserver

# Abrir en el navegador
http://127.0.0.1:8000
```

### Con Docker
```bash
docker compose up -d --build
http://localhost:8000
```

### Validaciones
```bash
python manage.py check      # Verifica configuración
python manage.py test       # Ejecuta pruebas unitarias
```

---

## 9. Estado actual

- **Rama activa**: `develop`
- **Último commit**: `6685b2d` — `fix: design update`
- **Working tree**: limpio (sin cambios pendientes)
- **Interfaz**: rediseñada con tema verde/blanco y gradientes
- **Lógica de negocio**: intacta, sin modificaciones desde los commits anteriores de funcionalidad

---

> Este documento resume el proyecto basado en el historial real de commits y en el código fuente presente en el repositorio. No incluye funcionalidades que no estén implementadas en el código actual.
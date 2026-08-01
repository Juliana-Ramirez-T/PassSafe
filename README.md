# PassSafe

Gestor de contraseñas seguro desarrollado con **Django** siguiendo una arquitectura basada en **ICONIX Process** y el patrón **MVT (Model–View–Template)**.

---

## Tecnologías utilizadas

* Python 3
* Django 5
* SQLite (desarrollo local)
* HTML5
* CSS3
* JavaScript
* PlantUML
* Git / GitHub

---

## Funcionalidades implementadas

* Registro e inicio de sesión de usuarios.
* Gestión de contraseña maestra.
* CRUD completo de credenciales.
* Organización de credenciales por categorías.
* Generador de contraseñas seguras.
* Generación de frases Diceware.
* Auditoría de seguridad:

  * detección de contraseñas débiles,
  * detección de reutilización,
  * cálculo de puntuación de seguridad,
  * recomendaciones automáticas.
* Interfaz oscura responsive tipo dashboard.
* Pruebas unitarias para la lógica de auditoría.

---

## Justificación tecnológica

La propuesta inicial del proyecto contemplaba el uso de **Flask** para el backend y **React** para el frontend. Sin embargo, el requerimiento oficial de la asignatura solicitó explícitamente un **Proyecto de Django** y su despliegue en una plataforma compatible como **PythonAnywhere**.

Por esta razón, PassSafe fue implementado completamente en **Django**, aprovechando:

* el sistema de autenticación integrado,
* el ORM seguro de Django,
* la arquitectura MVT,
* las herramientas de validación y protección CSRF,
* el sistema de plantillas para construir una interfaz moderna sin depender de un framework frontend externo.

Esta decisión permitió mantener los objetivos funcionales y de seguridad del proyecto mientras se cumplían los requisitos académicos establecidos.

---

## Consideraciones de escalabilidad

El proyecto fue diseñado teniendo en cuenta el requisito no funcional de soportar **al menos 10.000 usuarios registrados**.

Para ello se adoptaron las siguientes decisiones arquitectónicas:

* separación de credenciales por usuario autenticado,
* consultas filtradas mediante `request.user`,
* uso del ORM de Django para evitar acceso global a los datos,
* estructura modular basada en aplicaciones (`accounts`, `vault`, `generator`, `audit`),
* posibilidad de incorporar paginación y optimizaciones de consultas.

### Nota importante

La versión actual utiliza **SQLite** como base de datos de desarrollo local. Para un entorno de producción orientado a cargas cercanas a **10.000 usuarios registrados**, se recomienda utilizar **PostgreSQL**, manteniendo la misma estructura de modelos y lógica de negocio implementada en PassSafe.

---

## Arquitectura del proyecto

```text
apps/
├── accounts/
├── vault/
├── generator/
└── audit/
```

Cada módulo mantiene separación entre:

* **Modelos** → persistencia de datos.
* **Vistas y servicios** → lógica de negocio.
* **Templates** → interfaz de usuario.

Esta estructura facilita la **mantenibilidad**, la **escalabilidad** y la trazabilidad entre los diagramas UML de ICONIX y el código fuente.

---

## Ejecución local

```bash
python -m venv .venv

# Windows
.venv\\Scripts\\activate

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver
```

La aplicación quedará disponible en:

```text
http://127.0.0.1:8000/
```

---

## Pruebas

Ejecutar las pruebas unitarias del módulo de auditoría:

```bash
python manage.py test apps.audit
```

Resultado esperado:

```text
Ran 4 tests
OK
```

---

## Despliegue

La aplicación está preparada para desplegarse en **PythonAnywhere** utilizando:

* `gunicorn`,
* `collectstatic`,
* configuración WSGI de Django.

---

## Metodología

El desarrollo se apoyó en **ICONIX Process**, utilizando:

* Diagrama de Casos de Uso.
* Especificaciones de Casos de Uso.
* Diagramas de Robustez.
* Diagramas de Secuencia.
* Implementación trazable Boundary → Control → Entity.

---

## Autora

**Juliana Ramírez - Juan José Munera - Pedro Aristizabal**
Ingeniería de Sistemas e Informática — Universidad Nacional de Colombia

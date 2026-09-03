# IA Library

Biblioteca de recursos de IA en formato de aplicación de escritorio portable.

## Objetivo

Centralizar prompts, técnicas, documentación y otros recursos de IA en una interfaz sencilla, editable y ampliable.

## Funciones iniciales

- Biblioteca de recursos organizada por carpetas y categorías.
- Buscador rápido.
- Editor para personalizar recursos antes de copiarlos.
- Copia directa al portapapeles.
- Asistente IA contextual sobre el recurso seleccionado.
- Configuración local para la conexión con la API.
- Construcción como ejecutable portable de Windows, sin instalador.

## Estructura

```text
IA-library/
├── app.py
├── requirements.txt
├── build_portable.bat
├── config.example.json
└── resources/
    └── prompts/
```

## Ejecutar en desarrollo

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
python app.py
```

## Crear versión portable

Ejecuta `build_portable.bat`. El ejecutable aparecerá en `dist/IA-Library.exe`.

La API key se configura localmente en `config.json`. Este archivo está excluido de Git para evitar publicar credenciales.

## Licencia

MIT para el código del proyecto. Los materiales de terceros incorporados a la biblioteca mantienen sus propias condiciones de uso y derechos.

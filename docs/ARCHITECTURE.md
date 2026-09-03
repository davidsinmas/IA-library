# Arquitectura inicial

La aplicación se divide conceptualmente en cuatro capas:

1. Interfaz: navegación, búsqueda, edición y diálogo IA.
2. Biblioteca: recursos JSON organizados por carpetas.
3. Integración IA: cliente HTTP desacoplado del contenido.
4. Distribución: ejecución Python en desarrollo y ejecutable portable con PyInstaller.

El contenido se mantiene fuera del código siempre que sea posible para que la biblioteca pueda crecer sin rehacer la aplicación.

# Política de seguridad

## Versiones compatibles

Radar Community todavía se encuentra en desarrollo inicial. Solo la versión más reciente publicada recibe correcciones de seguridad.

El backend en desarrollo no debe considerarse desplegado ni disponible públicamente hasta que exista evidencia de producción.

## Reportar una vulnerabilidad

No abras un issue público ni un pull request con detalles de una vulnerabilidad.

Utiliza el formulario privado **Report a vulnerability** de la sección **Security** del repositorio:

<https://github.com/Radar-Cultural/radar-community/security/advisories/new>

Incluye, cuando sea posible:

- Descripción y alcance del problema.
- Pasos mínimos para reproducirlo.
- Impacto observado o potencial.
- Versión, commit o URL afectada.
- Mitigación sugerida, si existe.

No incluyas credenciales reales, datos personales ni información de terceros. Si el formulario privado no está disponible, no publiques el reporte; solicita a una persona propietaria de la organización que habilite Private Vulnerability Reporting.

## Controles del backend

- La API pública es de sólo lectura y filtra exclusivamente publicaciones visibles.
- Las operaciones administrativas requieren sesión y CSRF.
- No se aceptan orígenes CORS, hosts o permisos globales mediante comodines.
- Los reportes sensibles nunca deben convertirse en issues públicas.

Un cambio que reduzca estos controles requiere revisión de seguridad explícita y pruebas que demuestren el nuevo límite de acceso.

El equipo acusará recibo cuando exista un canal privado operativo, evaluará el impacto y coordinará la divulgación. No se prometen plazos hasta definir formalmente el proceso de respuesta.

# 📊 Meli SAT Manager

Sistema web para gestionar información SAT de publicaciones de Mercado Libre.

## ⚡ Inicio Rápido

```bash
# 1. Clonar e instalar
git clone https://github.com/mrg0809/MercadoLibreAPISATupdate.git
cd MercadoLibreAPISATupdate
pip install -r requirements.txt

# 2. Configurar credenciales
cp .env.example .env
# Edita .env con tu ACCESS_TOKEN y USER_ID

# 3. Iniciar el servidor
python main.py

# 4. Abrir en navegador
# http://localhost:8000
```

## 🎯 Características

- **Descargar publicaciones**: Obtén todas tus publicaciones en formato CSV o XLSX con columnas SAT listas para editar
- **Actualizar campos SAT**: Sube tu archivo editado para actualizar los siguientes campos:
  - ClaveProdServ
  - ClaveUnidad
  - Unidad_SAT
  - Descripción_SAT
- **Interfaz web amigable**: UI simple y moderna para gestionar tus publicaciones
- **Logs detallados**: Sistema completo de logging para rastrear actualizaciones

## 🚀 Instalación

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Cuenta de Mercado Libre con acceso a la API

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/mrg0809/MercadoLibreAPISATupdate.git
cd MercadoLibreAPISATupdate
```

2. **Crear y activar un entorno virtual (recomendado)**
```bash
# En Linux/Mac
python3 -m venv venv
source venv/bin/activate

# En Windows
python -m venv venv
venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**

Copia el archivo de ejemplo y edita con tus credenciales:
```bash
cp .env.example .env
```

Edita el archivo `.env` con tu editor favorito:
```env
ACCESS_TOKEN=tu_access_token_de_mercadolibre
USER_ID=tu_user_id_de_mercadolibre
```

**¿Cómo obtener tus credenciales?**
Ver la sección de [Autenticación con OAuth](#-autenticación-con-oauth) para instrucciones detalladas paso a paso.

## 🔐 Autenticación con OAuth

### Introducción

MercadoLibre utiliza OAuth 2.0 para autenticación. Este proceso permite que tu aplicación acceda a la API de forma segura sin manejar directamente las credenciales del usuario.

### Paso 1: Crear una Aplicación en MercadoLibre

1. **Ir al Portal de Desarrolladores**
   - Visita: https://developers.mercadolibre.com/
   - Inicia sesión con tu cuenta de Mercado Libre

2. **Crear una Nueva Aplicación**
   - Haz clic en "Mis aplicaciones" o "My applications"
   - Haz clic en "Crear nueva aplicación" o "Create new application"

3. **Completar el Formulario de Registro**
   - **Nombre de la aplicación**: `Meli SAT Manager` (o el nombre que prefieras)
   - **Descripción corta**: `Sistema para gestionar información SAT`
   - **Descripción larga**: Breve descripción de tu aplicación
   - **URL de callback/redirect**: Para desarrollo local, usa:
     ```
     http://localhost:8000/auth/callback
     ```
     O simplemente: `http://localhost:8000`
   - **Sitio web**: Puedes usar `http://localhost:8000` para desarrollo

4. **Obtener las Credenciales**
   Después de crear la aplicación, obtendrás:
   - **App ID** (Client ID)
   - **Secret Key** (Client Secret)
   
   ⚠️ **Guarda el Secret Key de forma segura** - No lo compartas ni lo subas a repositorios públicos

### Paso 2: Flujo de Autenticación OAuth para Localhost

Para una aplicación local/desarrollo, hay dos opciones:

#### Opción A: Test User Token (Recomendado para Desarrollo Local)

Esta es la forma más sencilla para desarrollo y testing local:

1. **Generar Token de Prueba**
   - Ve a: https://developers.mercadolibre.com/
   - Entra a tu aplicación
   - Busca la sección "Credenciales de prueba" o "Test credentials"
   - Haz clic en "Generar token de prueba" o "Generate test token"
   - Selecciona los **scopes necesarios**:
     - ✅ `read` - Para leer tus publicaciones
     - ✅ `write` - Para actualizar campos SAT
     - ✅ `offline_access` - Para mantener el acceso por más tiempo

2. **Copiar el Access Token**
   - El token generado será algo como: `APP_USR-1234567890123456-111111-abcdef1234567890abcdef1234567890-123456789`
   - Este token es válido por 6 horas aproximadamente

3. **Obtener tu USER_ID**
   Puedes obtenerlo de dos formas:
   
   **Opción 1 - Desde la API:**
   ```bash
   curl -X GET \
     'https://api.mercadolibre.com/users/me' \
     -H 'Authorization: Bearer TU_ACCESS_TOKEN'
   ```
   
   **Opción 2 - Desde el portal:**
   - El USER_ID aparece en el portal de desarrolladores bajo tu perfil

4. **Actualizar el archivo .env**
   ```env
   ACCESS_TOKEN=APP_USR-1234567890123456-111111-abcdef1234567890abcdef1234567890-123456789
   USER_ID=123456789
   ```

⚠️ **Nota sobre Expiración**: Los tokens de prueba expiran. Cuando veas errores 403 o 401, simplemente genera un nuevo token siguiendo estos mismos pasos.

#### Opción B: Flujo OAuth Completo (Para Producción)

Si necesitas un token de larga duración o para producción, sigue este flujo:

1. **Construir la URL de Autorización**
   ```
   https://auth.mercadolibre.com.mx/authorization?response_type=code&client_id=TU_APP_ID&redirect_uri=http://localhost:8000/auth/callback&state=random_string
   ```
   
   Parámetros:
   - `client_id`: Tu App ID
   - `redirect_uri`: Debe coincidir exactamente con la URL registrada
   - `state`: String aleatorio para seguridad (opcional para desarrollo)

2. **Autorizar la Aplicación**
   - Abre la URL en tu navegador
   - Inicia sesión si es necesario
   - Autoriza los permisos solicitados
   - Serás redirigido a: `http://localhost:8000/auth/callback?code=TG-xxxxx&state=random_string`

3. **Intercambiar el Code por un Access Token**
   
   Ejecuta este comando (reemplaza los valores):
   ```bash
   curl -X POST \
     'https://api.mercadolibre.com/oauth/token' \
     -H 'Content-Type: application/json' \
     -d '{
       "grant_type": "authorization_code",
       "client_id": "TU_APP_ID",
       "client_secret": "TU_SECRET_KEY",
       "code": "TG-xxxxx",
       "redirect_uri": "http://localhost:8000/auth/callback"
     }'
   ```
   
   Respuesta:
   ```json
   {
     "access_token": "APP_USR-1234567890123456-111111-abc...",
     "token_type": "Bearer",
     "expires_in": 21600,
     "scope": "read write offline_access",
     "user_id": 123456789,
     "refresh_token": "TG-xxxxx..."
   }
   ```

4. **Guardar las Credenciales**
   ```env
   ACCESS_TOKEN=APP_USR-1234567890123456-111111-abc...
   USER_ID=123456789
   REFRESH_TOKEN=TG-xxxxx...
   ```

5. **Refrescar el Token (cuando expire)**
   ```bash
   curl -X POST \
     'https://api.mercadolibre.com/oauth/token' \
     -H 'Content-Type: application/json' \
     -d '{
       "grant_type": "refresh_token",
       "client_id": "TU_APP_ID",
       "client_secret": "TU_SECRET_KEY",
       "refresh_token": "TU_REFRESH_TOKEN"
     }'
   ```

### Resumen: ¿Cuál Opción Elegir?

| Escenario | Opción Recomendada |
|-----------|-------------------|
| Desarrollo local / Testing | **Opción A** - Test User Token |
| Primera vez usando la API | **Opción A** - Test User Token |
| Aplicación de producción | **Opción B** - Flujo OAuth Completo |
| Necesitas auto-refresh | **Opción B** - Flujo OAuth Completo |

### Notas Importantes

1. **Callback en Localhost**: Para desarrollo local, el callback puede ser cualquier URL local como `http://localhost:8000`. No necesitas implementar la ruta `/auth/callback` si usas la Opción A (Test User Token).

2. **Sin Callback Público**: No necesitas un servidor público ni dominio. Todo el proceso puede hacerse en localhost.

3. **Expiración de Tokens**: 
   - Los tokens de prueba expiran en ~6 horas
   - Los tokens OAuth expiran en ~6 horas pero se pueden refrescar
   - Usa `refresh_token` para obtener nuevos access tokens sin re-autorizar

4. **Scopes Necesarios**:
   - `read`: Para descargar publicaciones
   - `write`: Para actualizar campos SAT
   - `offline_access`: Para tokens de larga duración

5. **Testing**: Usa la Opción A (Test User Token) para simplificar el desarrollo. Es la forma más rápida de empezar.

## 🎮 Uso

### Iniciar el servidor

```bash
python main.py
```

O usando uvicorn directamente:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

El servidor estará disponible en: **http://localhost:8000**

### Usando la Interfaz Web

1. **Descargar publicaciones**:
   - Abre http://localhost:8000 en tu navegador
   - Selecciona el formato (Excel o CSV)
   - Haz clic en "📥 Descargar Publicaciones"
   - El archivo se descargará automáticamente

2. **Editar el archivo**:
   - Abre el archivo descargado en Excel o tu editor preferido
   - Completa las columnas: `ClaveProdServ`, `ClaveUnidad`, `Unidad_SAT`, `Descripción_SAT`
   - Guarda el archivo

3. **Subir actualizaciones**:
   - En la interfaz web, selecciona tu archivo editado
   - Haz clic en "📤 Subir y Actualizar"
   - Espera a que el proceso complete
   - Verás un resumen con los resultados

## 📁 Estructura del Proyecto

```
MercadoLibreAPISATupdate/
├── main.py                 # Aplicación FastAPI principal
├── utils.py                # Funciones auxiliares y logging
├── requirements.txt        # Dependencias del proyecto
├── .env.example           # Ejemplo de configuración
├── .env                   # Tu configuración (no incluido en git)
├── services/
│   ├── __init__.py
│   ├── meli_client.py     # Cliente de la API de MercadoLibre
│   └── file_manager.py    # Gestor de archivos CSV/XLSX
├── templates/
│   └── index.html         # Interfaz web
├── static/                # Archivos estáticos (vacío por ahora)
└── meli_sat_manager.log   # Archivo de logs (se genera automáticamente)
```

## 🔧 Configuración Avanzada

### Variables de Entorno Adicionales

Puedes agregar estas variables opcionales a tu archivo `.env`:

```env
# Puerto del servidor (default: 8000)
PORT=8000

# Host del servidor (default: 0.0.0.0)
HOST=0.0.0.0
```

### Logs

Los logs se guardan automáticamente en `meli_sat_manager.log` y también se muestran en la consola. Puedes consultar este archivo para ver el historial completo de operaciones.

## 📋 Columnas del Archivo

El archivo descargado incluye las siguientes columnas:

- `id`: ID de la publicación en MercadoLibre
- `title`: Título del producto
- `category_id`: ID de categoría
- `brand`: Marca del producto
- `atributos_completos`: JSON con todos los atributos
- `seller_custom_field`: Campo personalizado del vendedor
- `ClaveProdServ`: Clave de producto/servicio SAT (para editar)
- `ClaveUnidad`: Clave de unidad SAT (para editar)
- `Unidad_SAT`: Unidad SAT (para editar)
- `Descripción_SAT`: Descripción SAT (para editar)

## ⚠️ Notas Importantes

1. **Autenticación**: Este sistema usa un access token manual. No implementa OAuth desde la interfaz.
2. **Actualizaciones seguras**: Solo se actualizan los 4 campos SAT especificados, nada más del producto.
3. **Rate limiting**: La API de MercadoLibre tiene límites de tasa. El sistema procesa los items secuencialmente.
4. **Validaciones**: El sistema valida que el archivo tenga las columnas requeridas antes de procesar.
5. **Formato de archivo**: Soporta tanto CSV como XLSX para mayor flexibilidad.

## 🐛 Solución de Problemas

### Error: "ACCESS_TOKEN and USER_ID must be set in .env file"
- Verifica que el archivo `.env` existe en el directorio raíz
- Asegúrate de que las variables estén correctamente definidas sin espacios

### Error 403 Forbidden al descargar publicaciones
Este error indica que el token de acceso no tiene los permisos necesarios o ha expirado. Solución:

1. **Verifica que tu ACCESS_TOKEN sea válido**:
   - Los tokens de MercadoLibre expiran después de cierto tiempo
   - Genera un nuevo token en: https://developers.mercadolibre.com/

2. **Asegúrate de que el token tenga los scopes necesarios**:
   - `read` - Para leer tus publicaciones
   - `write` - Para actualizar campos SAT
   - `offline_access` - Para mantener el acceso

3. **Verifica que el USER_ID sea correcto**:
   - El USER_ID debe coincidir con el usuario autenticado del token
   - Puedes verificar tu USER_ID en tu perfil de MercadoLibre

4. **Regenera tu token**:
   - Ve a https://developers.mercadolibre.com/
   - Crea una nueva aplicación o usa una existente
   - Genera un nuevo token con los scopes necesarios
   - Actualiza el archivo `.env` con el nuevo token

### Error 401 Unauthorized
- Tu ACCESS_TOKEN es inválido o ha expirado
- Genera un nuevo token en: https://developers.mercadolibre.com/
- Actualiza el archivo `.env` con el nuevo token

### Error al descargar publicaciones (otros errores)
- Verifica que tu ACCESS_TOKEN sea válido y no haya expirado
- Asegúrate de tener publicaciones activas en tu cuenta
- Verifica tu conexión a Internet

### Error al subir archivo
- Verifica que el archivo tenga las columnas requeridas: `id`, `ClaveProdServ`, `ClaveUnidad`, `Unidad_SAT`, `Descripción_SAT`
- Asegúrate de que los IDs en el archivo coincidan con tus publicaciones

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Haz fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT.

## 👤 Autor

Desarrollado por mrg0809

## 🔗 Enlaces Útiles

- [Documentación API MercadoLibre](https://developers.mercadolibre.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

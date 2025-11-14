# Guía de Uso: Scripts de Autenticación MercadoLibre

Esta guía explica cómo usar los scripts PowerShell para obtener tokens de MercadoLibre de forma sencilla.

## 📋 Requisitos Previos

1. Windows con PowerShell (Windows 7 o superior)
2. Una aplicación creada en https://developers.mercadolibre.com/
3. Tu **App ID** y **Client Secret** de la aplicación

## 🚀 Opción 1: Obtener Tokens Nuevos (Primera Vez)

### Paso 1: Configurar el Script

1. Abre el archivo `get_ml_tokens.ps1` en el Bloc de notas o tu editor favorito

2. Encuentra la sección de CONFIGURACIÓN al inicio del archivo:
   ```powershell
   $APP_ID = "TU_APP_ID"
   $CLIENT_SECRET = "TU_CLIENT_SECRET"
   $REDIRECT_URI = "https://google.com"
   ```

3. Reemplaza los valores:
   - `TU_APP_ID`: Reemplázalo con tu App ID (ejemplo: `1234567890123456`)
   - `TU_CLIENT_SECRET`: Reemplázalo con tu Client Secret (ejemplo: `AbCdEfGh1234567890`)
   - `REDIRECT_URI`: Déjalo como `https://google.com` (funciona perfectamente)

4. Guarda el archivo

### Paso 2: Ejecutar el Script

1. Abre PowerShell:
   - Presiona `Windows + X` y selecciona "Windows PowerShell"
   - O busca "PowerShell" en el menú Inicio

2. Navega a la carpeta del proyecto:
   ```powershell
   cd C:\ruta\a\tu\proyecto\MercadoLibreAPISATupdate
   ```

3. Si es la primera vez ejecutando scripts, habilita la ejecución:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
   Responde "S" (Sí) cuando se te pregunte

4. Ejecuta el script:
   ```powershell
   .\get_ml_tokens.ps1
   ```

### Paso 3: Seguir las Instrucciones del Script

El script te mostrará:

1. **Una URL para autorizar**
   - Copia y pega la URL en tu navegador
   - Ejemplo: `https://auth.mercadolibre.com.mx/authorization?response_type=code&client_id=123...`

2. **Pantalla de autorización**
   - Inicia sesión con tu cuenta de Mercado Libre
   - Acepta los permisos solicitados

3. **Redirección**
   - Serás redirigido a una URL como: `https://google.com/?code=TG-6470a8b3-xxxx-xxxx-xxxx-xxxxxxxxxxxx`
   - Copia SOLO el valor después de `code=` (ejemplo: `TG-6470a8b3-xxxx-xxxx-xxxx-xxxxxxxxxxxx`)

4. **Pegar el código**
   - Regresa a PowerShell
   - Pega el código cuando se te solicite
   - Presiona Enter

### Paso 4: Obtener el Archivo de Tokens

El script generará un archivo llamado `ml_tokens.txt` con este contenido:

```
# Tokens de MercadoLibre
# Generado: 2025-11-14 10:30:00

ACCESS_TOKEN=APP_USR-1234567890123456-111111-abcdef1234567890abcdef1234567890-123456789
USER_ID=123456789
REFRESH_TOKEN=TG-6470a8b3-1234-5678-90ab-cdef12345678
```

### Paso 5: Configurar el Archivo .env

1. Abre o crea el archivo `.env` en la raíz del proyecto

2. Copia el contenido de `ml_tokens.txt` al archivo `.env`:
   ```env
   ACCESS_TOKEN=APP_USR-1234567890123456-111111-abcdef1234567890abcdef1234567890-123456789
   USER_ID=123456789
   REFRESH_TOKEN=TG-6470a8b3-1234-5678-90ab-cdef12345678
   ```

3. Guarda el archivo

4. **¡Listo!** La aplicación ya puede conectarse a la API de MercadoLibre

## 🔄 Opción 2: Renovar Tokens (Cuando Expiren)

Los tokens de MercadoLibre expiran aproximadamente cada 6 horas. Cuando veas errores 403 o 401, significa que el token expiró.

### Paso 1: Configurar el Script de Renovación

1. Abre `refresh_ml_tokens.ps1` en un editor

2. Actualiza la configuración:
   ```powershell
   $APP_ID = "TU_APP_ID"
   $CLIENT_SECRET = "TU_CLIENT_SECRET"
   ```

3. Guarda el archivo

### Paso 2: Ejecutar el Script

```powershell
.\refresh_ml_tokens.ps1
```

El script:
1. Leerá el `REFRESH_TOKEN` del archivo `ml_tokens.txt` (si existe)
2. Si no lo encuentra, te pedirá que lo ingreses manualmente
3. Renovará los tokens automáticamente
4. Actualizará el archivo `ml_tokens.txt`

### Paso 3: Actualizar el .env

Copia los nuevos valores de `ml_tokens.txt` a tu archivo `.env`

## ⚠️ Notas Importantes

### ¿Qué hacer si el REFRESH_TOKEN también expiró?

Si el script `refresh_ml_tokens.ps1` falla con un error, significa que el `REFRESH_TOKEN` también expiró. En este caso:
- Ejecuta nuevamente `get_ml_tokens.ps1` para obtener tokens completamente nuevos
- Esto requiere volver a autorizar la aplicación en el navegador

### Seguridad de los Tokens

- **NUNCA** compartas tus tokens públicamente
- **NO** subas el archivo `.env` a GitHub u otros repositorios públicos
- Los archivos `.env` y `ml_tokens.txt` ya están en `.gitignore` para protegerte

### Duración de los Tokens

- **ACCESS_TOKEN**: Válido por ~6 horas
- **REFRESH_TOKEN**: Válido por ~6 meses (si no se usa, puede expirar)
- **Recomendación**: Guarda el `REFRESH_TOKEN` de forma segura

## 🎯 Flujo Completo para el Dueño de la Cuenta

### Escenario: El desarrollador necesita tus tokens

1. **Ejecuta el script en tu computadora**
   ```powershell
   .\get_ml_tokens.ps1
   ```

2. **Sigue las instrucciones** (autorizar en navegador, copiar código)

3. **Envía el archivo `ml_tokens.txt`** al desarrollador de forma segura:
   - Por email
   - Por mensaje directo
   - Por sistema de archivos compartido seguro

4. **El desarrollador copia** el contenido al archivo `.env` en su computadora

5. **¡Listo!** El desarrollador puede trabajar con tu cuenta

### Escenario: Los tokens expiraron

Simplemente ejecuta:
```powershell
.\refresh_ml_tokens.ps1
```

Y envía el nuevo `ml_tokens.txt` al desarrollador.

## 📞 Solución de Problemas

### Error: "No se puede ejecutar el script"

**Solución**: Habilita la ejecución de scripts:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Error: "El código es inválido o ya fue usado"

**Solución**: El código de autorización solo se puede usar una vez. Genera uno nuevo:
1. Ejecuta el script nuevamente
2. Abre la URL en el navegador nuevamente
3. Obtendrás un nuevo código

### Error: "APP_ID o CLIENT_SECRET incorrectos"

**Solución**: Verifica que copiaste correctamente:
1. Tu App ID del portal de desarrolladores
2. Tu Client Secret del portal de desarrolladores
3. Asegúrate de no incluir espacios extras

### Error: "REDIRECT_URI no coincide"

**Solución**: Verifica que en el portal de desarrolladores:
1. Hayas configurado `https://google.com` como URL de callback
2. O usa la URL exacta que configuraste en tu aplicación

## ✅ Checklist Final

Antes de enviar los tokens al desarrollador, verifica:

- [ ] Ejecutaste `get_ml_tokens.ps1` exitosamente
- [ ] El archivo `ml_tokens.txt` contiene 3 líneas con valores (ACCESS_TOKEN, USER_ID, REFRESH_TOKEN)
- [ ] Los valores no dicen "your_xxx_here" sino que tienen datos reales
- [ ] Guardaste una copia del archivo en un lugar seguro
- [ ] Enviaste el archivo al desarrollador de forma segura

## 🔗 Enlaces Útiles

- Portal de Desarrolladores: https://developers.mercadolibre.com/
- Documentación de la API: https://developers.mercadolibre.com/es_ar/autenticacion-y-autorizacion
- Soporte: https://developers.mercadolibre.com/support

---

**¿Necesitas ayuda?** Contacta al desarrollador del proyecto.

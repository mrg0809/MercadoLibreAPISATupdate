# ===============================
# Script para obtener tokens de MercadoLibre OAuth
# ===============================

# ===============================
# CONFIGURACIÓN
# ===============================
# Reemplaza estos valores con los de tu aplicación en developers.mercadolibre.com
$APP_ID = "TU_APP_ID"
$CLIENT_SECRET = "TU_CLIENT_SECRET"
$REDIRECT_URI = "https://google.com"  # Déjalo así si no configuraste otro

# ===============================
# 1) Mostrar URL de autorización
# ===============================
$AUTH_URL = "https://auth.mercadolibre.com.mx/authorization?response_type=code&client_id=$APP_ID&redirect_uri=$REDIRECT_URI"

Write-Host ""
Write-Host "===============================================================" -ForegroundColor Cyan
Write-Host "   Script para obtener tokens de MercadoLibre" -ForegroundColor Cyan
Write-Host "===============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "PASO 1: Autorizar la aplicación" -ForegroundColor Yellow
Write-Host "-------------------------------"
Write-Host ""
Write-Host "Abre este enlace en el navegador:" -ForegroundColor White
Write-Host $AUTH_URL -ForegroundColor Green
Write-Host ""
Write-Host "Instrucciones:" -ForegroundColor White
Write-Host "  1. Inicia sesión con tu cuenta de Mercado Libre"
Write-Host "  2. Acepta los permisos solicitados"
Write-Host "  3. Serás redirigido a una URL como:"
Write-Host "     https://google.com/?code=TG-XXXXX-123456789-XXXXXXXX" -ForegroundColor Gray
Write-Host "  4. Copia SOLO el valor del parámetro 'code' (después de 'code=')"
Write-Host ""
Write-Host "===============================================================" -ForegroundColor Cyan
Write-Host ""

# Solicitar el código de autorización
$code = Read-Host "Pega aquí el código (code)"

if ([string]::IsNullOrWhiteSpace($code)) {
    Write-Host ""
    Write-Host "ERROR: No ingresaste ningún código." -ForegroundColor Red
    Write-Host "Ejecuta el script nuevamente." -ForegroundColor Red
    exit 1
}

# ===============================
# 2) Intercambiar code por tokens
# ===============================
Write-Host ""
Write-Host "PASO 2: Obteniendo tokens..." -ForegroundColor Yellow
Write-Host "-------------------------------"

$token_url = "https://api.mercadolibre.com/oauth/token"

$body = @{
    grant_type    = "authorization_code"
    client_id     = $APP_ID
    client_secret = $CLIENT_SECRET
    code          = $code
    redirect_uri  = $REDIRECT_URI
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Method Post -Uri $token_url -Body $body -ContentType "application/json"
} catch {
    Write-Host ""
    Write-Host "ERROR al obtener tokens:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    Write-Host "Posibles causas:" -ForegroundColor Yellow
    Write-Host "  - El código ya fue usado (genera uno nuevo)" -ForegroundColor White
    Write-Host "  - APP_ID o CLIENT_SECRET incorrectos" -ForegroundColor White
    Write-Host "  - REDIRECT_URI no coincide con el configurado en la app" -ForegroundColor White
    exit 1
}

$access_token = $response.access_token
$refresh_token = $response.refresh_token
$user_id = $response.user_id

Write-Host "✓ Tokens obtenidos exitosamente" -ForegroundColor Green
Write-Host ""

# ===============================
# 3) Guardar tokens en archivo
# ===============================
Write-Host "PASO 3: Guardando tokens..." -ForegroundColor Yellow
Write-Host "-------------------------------"

# Crear contenido para el archivo de tokens
$file_content = @"
# Tokens de MercadoLibre
# Generado: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

ACCESS_TOKEN=$access_token
USER_ID=$user_id
REFRESH_TOKEN=$refresh_token
"@

# Guardar en ml_tokens.txt
try {
    Set-Content -Path "ml_tokens.txt" -Value $file_content -Encoding UTF8
    Write-Host "✓ Archivo ml_tokens.txt creado exitosamente" -ForegroundColor Green
} catch {
    Write-Host "ERROR al crear el archivo:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}

# ===============================
# 4) Información final
# ===============================
Write-Host ""
Write-Host "===============================================================" -ForegroundColor Cyan
Write-Host "   ¡Proceso completado exitosamente!" -ForegroundColor Green
Write-Host "===============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Información de tu cuenta:" -ForegroundColor Yellow
Write-Host "  USER_ID: $user_id" -ForegroundColor White
Write-Host "  Token expira en: ~6 horas" -ForegroundColor White
Write-Host ""
Write-Host "Archivo generado:" -ForegroundColor Yellow
Write-Host "  📄 ml_tokens.txt" -ForegroundColor White
Write-Host ""
Write-Host "Próximos pasos:" -ForegroundColor Yellow
Write-Host "  1. Envía el archivo ml_tokens.txt al desarrollador" -ForegroundColor White
Write-Host "  2. El desarrollador copiará los valores al archivo .env" -ForegroundColor White
Write-Host "  3. La aplicación estará lista para funcionar" -ForegroundColor White
Write-Host ""
Write-Host "Contenido del archivo:" -ForegroundColor Yellow
Write-Host "-------------------------------" -ForegroundColor Gray
Get-Content "ml_tokens.txt" | ForEach-Object { Write-Host $_ -ForegroundColor Gray }
Write-Host "-------------------------------" -ForegroundColor Gray
Write-Host ""
Write-Host "IMPORTANTE: Guarda el REFRESH_TOKEN para renovar el acceso" -ForegroundColor Yellow
Write-Host "cuando el ACCESS_TOKEN expire." -ForegroundColor Yellow
Write-Host ""
Write-Host "===============================================================" -ForegroundColor Cyan

# ===============================
# Script para renovar tokens de MercadoLibre
# ===============================

# ===============================
# CONFIGURACIÓN
# ===============================
# Reemplaza estos valores con los de tu aplicación
$APP_ID = "TU_APP_ID"
$CLIENT_SECRET = "TU_CLIENT_SECRET"

Write-Host ""
Write-Host "===============================================================" -ForegroundColor Cyan
Write-Host "   Script para renovar tokens de MercadoLibre" -ForegroundColor Cyan
Write-Host "===============================================================" -ForegroundColor Cyan
Write-Host ""

# Leer el archivo de tokens existente si existe
$refresh_token = ""
if (Test-Path "ml_tokens.txt") {
    Write-Host "Leyendo tokens existentes..." -ForegroundColor Yellow
    $content = Get-Content "ml_tokens.txt" -Raw
    if ($content -match "REFRESH_TOKEN=(.+)") {
        $refresh_token = $matches[1].Trim()
        Write-Host "✓ REFRESH_TOKEN encontrado" -ForegroundColor Green
    }
}

# Si no se encontró, solicitar manualmente
if ([string]::IsNullOrWhiteSpace($refresh_token)) {
    Write-Host ""
    Write-Host "No se encontró REFRESH_TOKEN en ml_tokens.txt" -ForegroundColor Yellow
    Write-Host "Por favor, ingresa tu REFRESH_TOKEN:" -ForegroundColor White
    $refresh_token = Read-Host "REFRESH_TOKEN"
}

if ([string]::IsNullOrWhiteSpace($refresh_token)) {
    Write-Host ""
    Write-Host "ERROR: No se proporcionó un REFRESH_TOKEN." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Renovando tokens..." -ForegroundColor Yellow
Write-Host "-------------------------------"

# ===============================
# Renovar el token
# ===============================
$token_url = "https://api.mercadolibre.com/oauth/token"

$body = @{
    grant_type    = "refresh_token"
    client_id     = $APP_ID
    client_secret = $CLIENT_SECRET
    refresh_token = $refresh_token
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Method Post -Uri $token_url -Body $body -ContentType "application/json"
} catch {
    Write-Host ""
    Write-Host "ERROR al renovar tokens:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    Write-Host "Posibles causas:" -ForegroundColor Yellow
    Write-Host "  - El REFRESH_TOKEN ha expirado o es inválido" -ForegroundColor White
    Write-Host "  - APP_ID o CLIENT_SECRET incorrectos" -ForegroundColor White
    Write-Host ""
    Write-Host "Solución: Ejecuta get_ml_tokens.ps1 para obtener nuevos tokens" -ForegroundColor Yellow
    exit 1
}

$new_access_token = $response.access_token
$new_refresh_token = $response.refresh_token
$user_id = $response.user_id

Write-Host "✓ Tokens renovados exitosamente" -ForegroundColor Green
Write-Host ""

# ===============================
# Guardar nuevos tokens
# ===============================
Write-Host "Guardando nuevos tokens..." -ForegroundColor Yellow

$file_content = @"
# Tokens de MercadoLibre (Renovados)
# Generado: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

ACCESS_TOKEN=$new_access_token
USER_ID=$user_id
REFRESH_TOKEN=$new_refresh_token
"@

try {
    Set-Content -Path "ml_tokens.txt" -Value $file_content -Encoding UTF8
    Write-Host "✓ Archivo ml_tokens.txt actualizado" -ForegroundColor Green
} catch {
    Write-Host "ERROR al actualizar el archivo:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}

# ===============================
# Información final
# ===============================
Write-Host ""
Write-Host "===============================================================" -ForegroundColor Cyan
Write-Host "   ¡Tokens renovados exitosamente!" -ForegroundColor Green
Write-Host "===============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Información:" -ForegroundColor Yellow
Write-Host "  USER_ID: $user_id" -ForegroundColor White
Write-Host "  Nuevo token expira en: ~6 horas" -ForegroundColor White
Write-Host ""
Write-Host "Archivo actualizado:" -ForegroundColor Yellow
Write-Host "  📄 ml_tokens.txt" -ForegroundColor White
Write-Host ""
Write-Host "Contenido del archivo:" -ForegroundColor Yellow
Write-Host "-------------------------------" -ForegroundColor Gray
Get-Content "ml_tokens.txt" | ForEach-Object { Write-Host $_ -ForegroundColor Gray }
Write-Host "-------------------------------" -ForegroundColor Gray
Write-Host ""
Write-Host "Próximos pasos:" -ForegroundColor Yellow
Write-Host "  1. Envía el archivo actualizado al desarrollador" -ForegroundColor White
Write-Host "  2. El desarrollador actualizará el archivo .env" -ForegroundColor White
Write-Host ""
Write-Host "===============================================================" -ForegroundColor Cyan

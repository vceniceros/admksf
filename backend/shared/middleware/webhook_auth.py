"""
Middleware de autenticación para webhooks de n8n.
Solo aplica a POST /api/liquidar/
"""
from django.http import JsonResponse
from django.conf import settings
import os

class WebhookTokenAuthMiddleware:
    """
    Valida el header X-Webhook-Token contra N8N_WEBHOOK_SECRET.
    Retorna 401 si el token no coincide o no existe.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.webhook_secret = os.getenv('N8N_WEBHOOK_SECRET')
        
    def __call__(self, request):
        # Solo validar en el endpoint de liquidación
        if request.path == '/api/liquidar/' and request.method == 'POST':
            # Verificar que el secret esté configurado
            if not self.webhook_secret:
                return JsonResponse({
                    'error': 'Webhook authentication not configured on server'
                }, status=500)
            
            # Validar token del request
            token = request.headers.get('X-Webhook-Token')
            
            if token != self.webhook_secret:
                return JsonResponse({
                    'error': 'Unauthorized - Invalid or missing webhook token'
                }, status=401)
        
        # Continuar con el request
        return self.get_response(request)

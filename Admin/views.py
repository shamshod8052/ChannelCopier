from django.db import connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET


@csrf_exempt
@require_GET
def healthz(request):
    # Only the database is checked; the Telegram session belongs to the userbot.
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
    except Exception as e:
        error = (str(e).strip().splitlines() or [type(e).__name__])[0]
        return JsonResponse({'status': 'error', 'db': error[:200]}, status=503)
    return JsonResponse({'status': 'ok'})

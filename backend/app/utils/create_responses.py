from datetime import datetime
#-------------------------------RESPONSES-------------------------------
# metodo para estrcturar el patron de las respuestas
def create_response(success=True, data=None, message="", errors=None, status_code=200):

        response = {
            "success": success,
            "data": data if data is not None else None,
            "message": message,
            "errors": errors if errors else None,
            "timestamp": datetime.utcnow().isoformat(),
            "status_code": status_code
        }
        return response
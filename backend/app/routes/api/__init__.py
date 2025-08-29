from .auth_api import auth_api
from .clientes_api import cliente_api
from .productos_api import productos_api
from .pedidos_api import pedidos_api
from .inventario_api import inventario_api

all_blueprints = [
    auth_api,
    cliente_api,
    productos_api,
    pedidos_api,
    inventario_api
]

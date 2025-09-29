from flask_marshmallow import Marshmallow

ma = Marshmallow()

class PedidoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        from .models import Pedido
        model = Pedido
        include_fk = True
        load_instance = True
from tortoise import fields
from src.models.base import Base


class Empresa(Base):

    id = fields.IntField(pk=True, source_field="id_empresa")
    nombre_oficial = fields.CharField(max_length=100,null=True)
    direccion_postal = fields.TextField(null=True)
    direccion_email = fields.TextField(null=True)
    cant_trab_estatales = fields.IntField(null=True)
    cant_trab_noestatales = fields.IntField(null=True)
    director_general = fields.TextField(null=True)
    director_adjunto = fields.TextField(null=True)
    director_cana = fields.TextField(null=True)
    latitud = fields.DecimalField(max_digits=100, decimal_places=10, null=True)
    longitud = fields.DecimalField(max_digits=100, decimal_places=10, null=True)

    class Meta:
        table = "empresa_agroindustrial"









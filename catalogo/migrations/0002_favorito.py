import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("catalogo", "0001_initial"),
    ]
    operations = [
        migrations.CreateModel(
            name="Favorito",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("creado_en", models.DateTimeField(auto_now_add=True)),
                ("producto", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="marcado_como_favorito", to="catalogo.producto")),
                ("usuario", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="favoritos", to=settings.AUTH_USER_MODEL)),
            ],
            options={"verbose_name": "favorito", "verbose_name_plural": "favoritos"},
        ),
        migrations.AddConstraint(model_name="favorito", constraint=models.UniqueConstraint(fields=("usuario", "producto"), name="favorito_unico_por_usuario")),
    ]

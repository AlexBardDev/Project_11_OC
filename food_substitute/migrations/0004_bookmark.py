# Generated by Django 2.0.6 on 2018-06-02 08:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('food_substitute', '0003_delete_bookmarks'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_original_food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='original_food', to='food_substitute.Food')),
                ('id_substitute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='substitute', to='food_substitute.Food')),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

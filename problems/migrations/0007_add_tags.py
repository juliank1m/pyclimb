# Generated migration for Tag model and Problem.tags M2M

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0006_add_classic_problems'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=60, unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='problem',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='problems', to='problems.tag'),
        ),
    ]

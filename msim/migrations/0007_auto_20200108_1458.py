# Generated by Django 3.0.2 on 2020-01-08 14:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('msim', '0006_privatechat_privatechatmessage_privatechatreference'),
    ]

    operations = [
        migrations.AlterField(
            model_name='privatechatmessage',
            name='prev_msg_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='msim.PrivateChatMessage'),
        ),
    ]
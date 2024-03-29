# Generated by Django 4.1.1 on 2022-11-02 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("base", "0002_delete_person"),
    ]

    operations = [
        migrations.CreateModel(
            name="Patient",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("patientname", models.CharField(max_length=100)),
                ("age", models.CharField(max_length=100)),
                ("sex", models.CharField(max_length=100)),
                ("adress1", models.CharField(max_length=100)),
                ("adress2", models.CharField(max_length=100)),
                ("workphone", models.CharField(max_length=100)),
                ("city", models.CharField(max_length=100)),
                ("st", models.CharField(max_length=100)),
                ("zip", models.CharField(max_length=100)),
                ("country", models.CharField(max_length=100)),
                ("county", models.CharField(max_length=100)),
                ("homephone", models.CharField(max_length=100)),
                ("primaryinsurance", models.CharField(max_length=100)),
                ("insurancename1", models.CharField(max_length=100)),
                ("ID1", models.CharField(max_length=100)),
                ("GP1", models.CharField(max_length=100)),
                ("EFF1", models.CharField(max_length=100)),
                ("EXP1", models.CharField(max_length=100)),
                ("secondaryinsurance", models.CharField(max_length=100)),
                ("insurancename2", models.CharField(max_length=100)),
                ("ID2", models.CharField(max_length=100)),
                ("GP2", models.CharField(max_length=100)),
                ("EFF2", models.CharField(max_length=100)),
                ("EXP2", models.CharField(max_length=100)),
                ("tertiaryinsurance", models.CharField(max_length=100)),
                ("insurancename3", models.CharField(max_length=100)),
                ("ID3", models.CharField(max_length=100)),
                ("GP3", models.CharField(max_length=100)),
                ("EFF3", models.CharField(max_length=100)),
                ("EXP3", models.CharField(max_length=100)),
                ("referringmd", models.CharField(max_length=100)),
                ("phone", models.CharField(max_length=100)),
                ("fax", models.CharField(max_length=100)),
                ("NearestRelativeName", models.CharField(max_length=100)),
                ("NearestRelativeRelation", models.CharField(max_length=100)),
                ("NearestRelativeAddress", models.CharField(max_length=100)),
                ("NearestRelativeHomePhone", models.CharField(max_length=100)),
                ("NearestRelativeCity", models.CharField(max_length=100)),
                ("NearestRelativeST", models.CharField(max_length=100)),
                ("NearestRelativeZip", models.CharField(max_length=100)),
                ("NearestRelativeWorkPhone", models.CharField(max_length=100)),
                ("NearestRelativeWorkPhoneExt", models.CharField(max_length=100)),
            ],
        ),
    ]

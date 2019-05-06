# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Diagnoses(models.Model):
    encounter = models.ForeignKey('Encounter', models.DO_NOTHING, primary_key=True)
    icd_code = models.ForeignKey('Diagnosis', models.DO_NOTHING, db_column='icd_code')
    priority = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'diagnoses'
        unique_together = (('encounter', 'icd_code'),)


class Diagnosis(models.Model):
    icd_code = models.CharField(primary_key=True, max_length=10)
    diag_name = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'diagnosis'


class Discharge(models.Model):
    discharge_id = models.IntegerField(primary_key=True)
    discharge_name = models.CharField(max_length=125, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'discharge'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Encounter(models.Model):
    encounter_id = models.IntegerField(primary_key=True)
    num_lab_procedures = models.SmallIntegerField(blank=True, null=True)
    num_medications = models.IntegerField(blank=True, null=True)
    admiss_type = models.IntegerField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    age = models.CharField(max_length=8, blank=True, null=True)
    readmitted = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'encounter'


class Getspatientfrom(models.Model):
    encounter = models.ForeignKey(Encounter, models.DO_NOTHING, primary_key=True)
    source = models.ForeignKey('Source', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'getspatientfrom'


class Has(models.Model):
    patient = models.ForeignKey('Patient', models.DO_NOTHING)
    encounter = models.ForeignKey(Encounter, models.DO_NOTHING, primary_key=True)

    class Meta:
        managed = False
        db_table = 'has'


class Medication(models.Model):
    med_name = models.CharField(primary_key=True, max_length=100)

    class Meta:
        managed = False
        db_table = 'medication'


class Patient(models.Model):
    patient_id = models.IntegerField(primary_key=True)
    race = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(max_length=6, blank=True, null=True)
    payer_code = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patient'

    def __str__(self):
        return '%s %s %s %s' % (self.patient_id, self.race, self.gender, self.payer_code)


class Physician(models.Model):
    encounter = models.ForeignKey(Encounter, models.DO_NOTHING, primary_key=True)
    specialty = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'physician'


class Prescribes(models.Model):
    encounter = models.ForeignKey(Encounter, models.DO_NOTHING, primary_key=True)
    med_name = models.ForeignKey(Medication, models.DO_NOTHING, db_column='med_name')
    dosage_change = models.CharField(max_length=6, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'prescribes'
        unique_together = (('encounter', 'med_name'),)


class Sendspatientto(models.Model):
    encounter = models.ForeignKey(Encounter, models.DO_NOTHING, primary_key=True)
    discharge = models.ForeignKey(Discharge, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'sendspatientto'


class Source(models.Model):
    source_id = models.IntegerField(primary_key=True)
    source_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'source'


class Vitals(models.Model):
    encounter = models.ForeignKey(Encounter, models.DO_NOTHING, primary_key=True)
    a1c_result = models.CharField(max_length=4, blank=True, null=True)
    glucose_result = models.CharField(max_length=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vitals'

# Generated by Django 2.0 on 2018-02-08 11:32

from django.db import migrations


def forwards(apps, schema_editor):
    """
    Change all ClassicalWork objects into Work objects, and their associated
    data into WorkRole and WorkSelection models, then delete the ClassicalWork.
    """
    ClassicalWork = apps.get_model("spectator_events", "ClassicalWork")
    Work = apps.get_model("spectator_events", "Work")
    WorkRole = apps.get_model("spectator_events", "WorkRole")
    WorkSelection = apps.get_model("spectator_events", "WorkSelection")

    for cw in ClassicalWork.objects.all():

        work = Work.objects.create(
            kind="classicalwork", title=cw.title, title_sort=cw.title_sort
        )

        for role in cw.roles.all():
            WorkRole.objects.create(
                creator=role.creator,
                work=work,
                role_name=role.role_name,
                role_order=role.role_order,
            )

        for selection in cw.events.all():
            WorkSelection.objects.create(
                event=selection.event, work=work, order=selection.order
            )

        cw.delete()


class Migration(migrations.Migration):

    dependencies = [
        ("spectator_events", "0026_auto_20180208_1126"),
    ]

    operations = [
        migrations.RunPython(forwards),
    ]

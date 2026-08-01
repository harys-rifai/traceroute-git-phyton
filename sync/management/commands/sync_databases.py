from django.core.management.base import BaseCommand
from django.apps import apps
from django.db import connections, transaction


class Command(BaseCommand):
    help = 'Sync data between SQLite and PostgreSQL databases'

    def add_arguments(self, parser):
        parser.add_argument(
            '--from',
            dest='source',
            default='sqlite',
            choices=['sqlite', 'postgres'],
            help='Source database'
        )
        parser.add_argument(
            '--to',
            dest='target',
            default='postgres',
            choices=['sqlite', 'postgres'],
            help='Target database'
        )
        parser.add_argument(
            '--models',
            nargs='+',
            help='Specific models to sync (e.g., accounts.CustomUser datacenter.Datacenter)'
        )

    def handle(self, *args, **options):
        source = options['source']
        target = options['target']
        model_names = options['models']

        if source == target:
            self.stdout.write(self.style.ERROR('Source and target cannot be the same'))
            return

        source_alias = 'sqlite' if source == 'sqlite' else 'postgres'
        target_alias = 'postgres' if target == 'postgres' else 'sqlite'

        # Get all models
        all_models = []
        for model in apps.get_models():
            if not model._meta.auto_created:
                all_models.append(model)

        if model_names:
            models_to_sync = []
            for m in model_names:
                try:
                    app_label, model_name = m.split('.')
                    model = apps.get_model(app_label, model_name)
                    models_to_sync.append(model)
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'Skipping invalid model: {m} ({e})'))
        else:
            models_to_sync = all_models

        self.stdout.write(f'Syncing from {source} to {target}...')
        self.stdout.write(f'Models to sync: {len(models_to_sync)}')

        for model in models_to_sync:
            self.sync_model(model, source_alias, target_alias)

        self.stdout.write(self.style.SUCCESS('Sync completed!'))

    def sync_model(self, model, source_alias, target_alias):
        source_db = connections[source_alias]
        target_db = connections[target_alias]

        # Use the appropriate database manager for source
        source_manager = model.objects.using(source_alias)
        target_manager = model.objects.using(target_alias)

        # Get all objects from source
        objects = source_manager.all()
        count = objects.count()

        if count == 0:
            self.stdout.write(f'  {model._meta.label}: No data to sync')
            return

        self.stdout.write(f'  {model._meta.label}: Syncing {count} objects...')

        # Get all field names excluding auto fields
        field_names = [f.name for f in model._meta.concrete_fields if not f.auto_created]

        synced = 0
        skipped = 0

        for obj in objects:
            try:
                # Build kwargs for get_or_create
                kwargs = {}
                for field_name in field_names:
                    field = model._meta.get_field(field_name)
                    if field.primary_key:
                        continue
                    if field.is_relation and field.many_to_one:
                        # Handle foreign keys
                        related_obj = getattr(obj, field_name)
                        if related_obj is not None:
                            kwargs[field_name] = related_obj.pk
                        else:
                            kwargs[field_name] = None
                    else:
                        kwargs[field_name] = getattr(obj, field_name)

                # Use update_or_create with the primary key
                pk_field = model._meta.pk.name
                target_manager.update_or_create(
                    **{pk_field: getattr(obj, pk_field)},
                    defaults=kwargs
                )
                synced += 1
            except Exception as e:
                skipped += 1
                self.stdout.write(self.style.WARNING(f'    Error syncing {model._meta.label} pk={getattr(obj, pk_field, "?")}: {e}'))

        self.stdout.write(f'    Synced: {synced}, Skipped: {skipped}')

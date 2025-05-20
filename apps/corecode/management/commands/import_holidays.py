import datetime
import holidays
from django.core.management.base import BaseCommand
from apps.corecode.models import Holiday  # adjust based on your app name


class Command(BaseCommand):
    help = "Fetches public holidays for the current year using the holidays library and saves them to the database."

    def add_arguments(self, parser):
        parser.add_argument(
            "--country", type=str, default="IN", help="Country code (default: IN)"
        )

    def handle(self, *args, **options):
        current_year = datetime.date.today().year
        country_code = options["country"]

        self.stdout.write(f"Fetching holidays for {country_code} - {current_year}")

        try:
            public_holidays = holidays.CountryHoliday(country_code, years=[current_year])
        except NotImplementedError:
            self.stdout.write(self.style.ERROR(f"Holidays not available for country: {country_code}"))
            return

        created = 0
        skipped = 0

        for date, name in sorted(public_holidays.items()):
            obj, created_flag = Holiday.objects.get_or_create(date=date, defaults={"name": name})
            if created_flag:
                self.stdout.write(self.style.SUCCESS(f"✔ Added: {name} - {date}"))
                created += 1
            else:
                self.stdout.write(self.style.WARNING(f"⏩ Skipped (already exists): {name} - {date}"))
                skipped += 1

        self.stdout.write(
            self.style.SUCCESS(f"\n✅ Done! {created} holidays added, {skipped} skipped.")
        )

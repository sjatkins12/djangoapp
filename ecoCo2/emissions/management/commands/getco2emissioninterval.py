from django.core.management.base import BaseCommand, CommandError
import requests
import datetime
from emissions.models import Co2Timestamp


class Command(BaseCommand):
    help = "Fetch Co2 timestamps from API and insert into the database"

    def add_arguments(self, parser):
        parser.add_argument(
            "--start",
            required=True,
            type=int,
            help="Time from POSIX epoc in seconds to be the start of interval",
        )
        parser.add_argument(
            "--end",
            required=True,
            type=int,
            help="Time from POSIX epoc in seconds to be the end of interval",
        )

    def handle(self, *args, **options):
        start = options["start"]
        end = options["end"]

        response = requests.get(
            f"https://api-recrutement.ecoco2.com/v1/data/",
            params={"end": end, "start": start},
        )

        if response.status_code != 200:
            self.stderr.write(self.style.ERROR("Failed to GET Co2 Timestamps"))
            return

        timestamps = response.json()
        for timestamp in timestamps:
            dt = datetime.datetime.strptime(timestamp["datetime"], "%Y-%m-%dT%H:%M:%S")
            co2_ts, created = Co2Timestamp.objects.get_or_create(
                datetime=dt, defaults={"value": timestamp["co2_rate"]}
            )
            if not created:
                co2_ts.value = timestamp["co2_rate"]
                co2_ts.save()

        self.stdout.write(self.style.SUCCESS(f"Successfully put Co2 data"))

"""
Django command to wait for the database to be available.
"""
import time

from typing import Any, Optional
from django.core.management.base import BaseCommand
from django.db.utils import OperationalError

from psycopg2 import OperationalError as Psycopg2Error


class Command(BaseCommand):
    """Django command to wait for database"""

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        """Entrypoint for command"""
        self.stdout.write(self.style.WARNING('데이터베이스 기다리는중...'))
        db_up = False

        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2Error, OperationalError):
                self.stdout.write(self.style.WARNING('데이터베이스 없음 1초 대기'))
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("데이터베이스 연결됨!"))
                
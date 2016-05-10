import os
import signal
import subprocess
from django.core.management import call_command
from django.core.management.base import BaseCommand
from mapstory import settings
from optparse import make_option


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            "-f", 
            "--file", 
            dest = "filename",
            help = "specify import file", 
            default='mapstory'
        ),
    )


    def collect_static(self):
        self.collectstatic_process = subprocess.Popen(
            ['python manage.py collectstatic --noinput -i node_modules'],
            shell=True,
            stdin=subprocess.PIPE,
            stdout=self.stdout,
            stderr=self.stderr,
        )
        self.collectstatic_process.wait()


    def start_grunt(self):
        self.stdout.write('>>> Starting grunt')
        file_path = os.path.join(settings.LOCAL_ROOT, 'static', 'gruntfile.js')

        self.grunt_process = subprocess.Popen(
            ['grunt --gruntfile=%s --project storyscapes' % (file_path)],
            shell=True,
            stdin=subprocess.PIPE,
            stdout=self.stdout,
            stderr=self.stderr,
        )
        self.stdout.write('>>> Grunt process on pid {0}'.format(self.grunt_process.pid))
        self.grunt_process.wait()

        self.stdout.write('>>> Closing grunt process')


    def run_server(self):
        self.runserver_process = subprocess.Popen(
            ['python manage.py runserver 0.0.0.0:8500'],
            shell=True,
            stdin=subprocess.PIPE,
            stdout=self.stdout,
            stderr=self.stderr,
        )
        self.runserver_process.wait()


    def handle(self, *args, **options):
        self.start_grunt()
        self.collect_static()
        self.run_server()

        # call_command('runserver', '0.0.0.0:8500')
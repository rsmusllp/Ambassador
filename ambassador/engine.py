import collections
import csv
import subprocess

from . import its
from . import spy


class Engine:
    def __init__(self):
        if not its.py_v3:
            print('[-] the Python version is too old (minimum required is 3.5)')
            return

    @property
    def android_apps(self):
        pass

    @property
    def ios_apps(self):
        return

    def install_android_apps(self, apps_path):
        for path in apps_path:
            self.execute_command([f'{spy.ambassador_path}\\data\\bins\\adb.exe', 'install', path])

    def install_frida_server(self):
        self.execute_command()

    def install_ios_apps(self):
        pass

    @staticmethod
    def execute_command(command):
        process = subprocess.run(command, capture_output=True, shell=True)
        return process.returncode


class AppManager:
    def __init__(self):
        self.AppInformation = collections.namedtuple('AppInformation', ['app_name', 'app_type', 'app_filename', 'app_url'])
        if its.on_windows:
            self.app_path = f'{spy.ambassador_path}\\data\\docs\\apps-information.csv'

    @property
    def apps_information(self):
        """
        Returns a list of named tuple objects containing app information in the format app_name, app_type, app_paths, app_urls.
        """
        with open(self.app_path, 'r') as app_csv_file:
            csv_reader = csv.reader(app_csv_file)
            apps = [self.AppInformation(app[0], app[1], app[2], app[3]) for app in csv_reader]
        return apps

    @property
    def android_apps_absolute_path(self):
        return [f'{spy.ambassador_path}\\data\\apps\\android\\{app.app_filename}' for app in self.apps_information if app.app_type == 'android']
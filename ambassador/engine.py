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

    def install_android_apps(self):
        pass

    def install_frida_server(self):
        self.execute_command()

    def install_ios_apps(self):
        pass

    @staticmethod
    def execute_command(command):
        process = subprocess.run(command, capture_output=True)
        return process.returncode


class AppManager:
    def __init__(self):
        self.app_path = ''
        if its.on_windows:
            self.app_path = f'{spy.absolute_path}\\data\\docs\\apps-information.csv'

    @property
    def android_apps(self):
        """
        Returns a list of absolute paths to the apk(s) to be installed onto the Android device.
        """
        with open(self.app_path, 'r') as app_csv_file:
            csv_reader = csv.reader(app_csv_file)
            app_paths = [f'{spy.absolute_path}\\data\\apps\\android\\{app[2]}' for app in csv_reader if app[1] == 'android']
        return app_paths

    def ios_apps(self):
        return

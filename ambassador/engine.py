import collections
import csv
import shutil
import subprocess

from os import path
from urllib import request

from . import its
from . import spy


class Engine:
    def __init__(self):
        if not its.py_v3:
            print('[-] the Python version is too old (minimum required is 3.5)')
            return

    def install_android_apps(self, apps_path):
        print('[?] Installing android applications onto the device.')
        for path in apps_path:
            returncode, stdout, stderr = self.execute_command(f'{spy.ambassador_path}\\data\\bins\\adb\\windows\\adb.exe install {path}')
            if returncode:
                print(f'[-] Command [ {spy.ambassador_path}\\data\\bins\\adb\\windows\\adb.exe install {path} ] failed to run')
                #todo: print stdout and stderr when a command fails
                return
            print(f'[+] Command [ {spy.ambassador_path}\\data\\bins\\adb\\windows\\adb.exe install {path} ] ran successfully.')

    def install_frida_server(self):
        # todo: Need to figure out how to install frida as no APK is offered.
        self.execute_command()

    def install_ios_apps(self, apps_path):
        print('[?] Installing ios applications onto the device.')
        for path in apps_path:
            returncode, stdout, stderr = self.execute_command(f'{spy.ambassador_path}\\data\\bins\\ideviceinstaller\\windows\\ideviceinstaller.exe -i {path}')
            if returncode:
                print(f'[-] Command [ {spy.ambassador_path}\\data\\bins\\ideviceinstaller\\windows\\ideviceinstaller.exe -i {path} ] failed to run')
                # todo: print stdout and stderr when a command fails
                return
            print(f'[+] Command [ {spy.ambassador_path}\\data\\bins\\ideviceinstaller\\windows\\ideviceinstaller.exe -i {path} ] ran successfully.')

    @staticmethod
    def execute_command(command):
        process = subprocess.run(command, capture_output=True, shell=True)
        return process.returncode, process.stdout.decode('utf-8').rstrip(), process.stderr.decode('utf-8').rstrip()


class AppManager:
    def __init__(self):
        self.AppInformation = collections.namedtuple('AppInformation', ['app_name', 'app_type', 'app_filename', 'app_url', 'app_description'])
        if its.on_windows:
            self.app_data_path = f'{spy.ambassador_path}\\data\\docs\\apps-information.csv'
            self.android_app_paths = [f'{spy.ambassador_path}\\data\\apps\\android\\{app.app_filename}' for app in self.apps_information if app.app_type == 'android']
            self.ios_app_paths = [f'{spy.ambassador_path}\\data\\apps\\ios\\{app.app_filename}' for app in self.apps_information if app.app_type == 'ios']

    @property
    def apps_information(self):
        """
        Returns a list of named tuple objects containing app information in the format app_name, app_type, app_paths, app_urls.
        """
        with open(self.app_data_path, 'r') as app_csv_file:
            csv_reader = csv.reader(app_csv_file)
            apps = [self.AppInformation(app[0], app[1], app[2], app[3], app[4]) for app in csv_reader]
        return apps

    @property
    def installed(self):
        print('[?] Checking for missing applications.')
        app_paths = self.ios_app_paths + self.android_app_paths
        not_installed = []
        for app_path in app_paths:
            if not path.exists(app_path):
                print(f'[-] {app_path} not installed.')
                not_installed.append(app_path)
        return not_installed

    def updated(self):
        #todo: add logic to check if all apps are updated
        pass

    def install_apps(self, app_paths):
        """
        Accepts absolute path(s) to the (apk(s)/ipa(s)) that are currently not installed and updates the apps folder respectively.
        """
        print('[?] Installing applications.')
        app_installers = [(app.app_url, app_path) for app_path in app_paths for app in self.apps_information if app.app_filename in app_path]
        for app_installer in app_installers:
            with request.urlopen(app_installer[0]) as response, open(app_installer[1], 'wb') as out_app_file:
                if response.getcode() != 200:
                    print(f'[-] Failed to install {app_installer[1]}.')
                    return
                print(f'[+] Successfully installed {app_installer[1]}.')
                shutil.copyfileobj(response, out_app_file)

    def update_apps(self, apps):
        #todo: add logic to update apps that were found to be not updated.
        pass

import collections
import csv
import shutil

from os import path
from urllib import request

from . import db
from . import its
from . import spy


def dependency_check(self):
    #todo: check to see if dependencies are installed.
    pass


def install_android_apps(apps_path):
    android_db = db.AndroidDB()
    for app_path in apps_path:
        android_db.install_app_from_file(app_path)


# def install_frida_server(self):
#     # todo: Need to figure out how to install frida as no APK is offered.
#     self.execute_command('lmao')


def install_ios_apps(file_installer_information, package_installer_information):
    print('[?] Installing ios applications onto the apple device.')
    ip_addr = input('IP Adress to establish the IOS Debugging Bridge with: ')
    ios_device_bridge = db.IosDB(ip_addr)
    for installer in file_installer_information:
        ios_device_bridge.install_app_from_file(installer[0])
    for installer in package_installer_information:
        ios_device_bridge.install_app_from_package(installer)


class AppManager:
    def __init__(self):
        self.AppInformation = collections.namedtuple('AppInformation', ['app_name', 'app_platform', 'app_type', 'app_installer', 'app_url', 'app_description'])
        if its.on_windows:
            self.app_data_path = f'{spy.ambassador_path}\\data\\docs\\apps-information.csv'
            self.android_file_installer_information = [(f'{spy.ambassador_path}\\data\\apps\\android\\{app.app_installer}', app.app_url) for app in self.apps_information if app.app_platform == 'android' and app.app_type == 'file']
            self.ios_file_installer_information = [(f'{spy.ambassador_path}\\data\\apps\\ios\\{app.app_installer}', app.app_url) for app in self.apps_information if app.app_platform == 'ios' and app.app_type == 'file']
            self.ios_package_installer_information = [f'{app.app_installer}' for app in self.apps_information if app.app_platform == 'ios' and app.app_type == 'package']

    @property
    def apps_information(self):
        """
        Returns a list of named tuple objects containing app information in the format app_name, app_platform, app_type, app_url, app_description.
        """
        with open(self.app_data_path, 'r') as app_csv_file:
            csv_reader = csv.reader(app_csv_file)
            apps = [self.AppInformation(app[0], app[1], app[2], app[3], app[4], app[5]) for app in csv_reader]
        return apps

    @property
    def installed(self):
        print('[?] Checking for missing APK(s) and IPA(s).')
        app_installers = self.android_file_installer_information + self.ios_file_installer_information
        not_installed = []
        for app_path, app_url in app_installers:
            if not path.exists(app_path):
                print(f'[-] {app_path} not installed.')
                not_installed.append((app_path, app_url))
        return not_installed

    # def updated(self):
    #     #todo: add logic to check if all apps are updated
    #     pass

    def install_apps(self, app_installers):
        """
        Accepts absolute path(s) to the (apk(s)/ipa(s)) that are currently not installed and updates the apps folder respectively.
        """
        print('[?] Installing missing APK(s) and IPA(s).')
        for app_installer in app_installers:
            with request.urlopen(app_installer[1]) as response, open(app_installer[0], 'wb') as out_app_file:
                if response.getcode() != 200:
                    print(f'[-] Failed to install {app_installer[1]}.')
                    return
                print(f'[+] Successfully installed {app_installer[1]}.')
                shutil.copyfileobj(response, out_app_file)

    # def update_apps(self, apps):
    #     #todo: add logic to update apps that were found to be not updated.
    #     pass


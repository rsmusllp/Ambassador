import argparse
import sys

import ambassador


def print_app_descriptions(app_manager):
    print('All applications loaded to be installed on the mobile device.\n')
    for app in app_manager.apps_information:
        print(f'[-] {app.app_name} : {app.app_type} : {app.app_description}')

def main():
    parser = argparse.ArgumentParser(description='Ambassador is a tool for rooting and provisioning mobile devices for use in mobile security services. ', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--android', action='store_true', help='Setting up an android device.')
    parser.add_argument('--ios', action='store_true', help='Setting up an ios device.')
    parser.add_argument('--help-apps', action='store_true', help='List the current apps and their details.')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s Version: ' + ambassador.__version__)
    args = parser.parse_args()

    engine = ambassador.Engine()
    app_manager = ambassador.AppManager()

    if args.help_apps:
        print_app_descriptions(app_manager)
        return 0

    not_installed = app_manager.installed
    if not_installed:
        app_manager.install_apps(not_installed)
    if args.android:
        engine.install_android_apps(app_manager.android_app_paths)
    if args.ios:
        engine.install_ios_apps(app_manager.ios_app_paths)


if __name__ == '__main__':
    sys.exit(main())

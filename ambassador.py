import argparse
import sys

import ambassador


def print_tool_descriptions():
    pass


def main():
    parser = argparse.ArgumentParser(description='Ambassador')
    parser.add_argument('--android', action='store_true', help='Setting up an android device.')
    parser.add_argument('--ios', action='store_true', help='Setting up an ios device.')
    parser.add_argument('--help-apps', action='store_true', help='List the current apps and their details.')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s Version: ' + ambassador.__version__)
    args = parser.parse_args()

    engine = ambassador.Engine()
    apps = ambassador.AppManager()

    for line in apps.android_apps:
        print(line)
    return

    if args.help_apps:
        print_tool_descriptions(apps)
        return 0
    if args.android:
        engine.install_android_apps()
    if args.ios:
        engine.install_ios_apps()


if __name__ == '__main__':
    sys.exit(main())

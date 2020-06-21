import paramiko
import subprocess

from . import its
from . import spy


def local_execute(command):
    process = subprocess.run(command, capture_output=True, shell=True)
    return process.returncode, process.stdout.decode('utf-8').rstrip(), process.stderr.decode('utf-8').rstrip()


class IosDB:
    def __init__(self, ip_addr):
        print('[?] Connecting to the device via SSH.')
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh_client.connect(ip_addr, 22, 'root', 'alpine')
        print('[?] Successfully connected to the device via SSH.')

    def _ssh_execute(self, command):
        print(f'[?] Executing [{command}] via SSH.')
        stdin, stdout, stderr = self.ssh_client.exec_command(command)
        if stdout.channel.recv_exit_status() != 0:
            print(f'[-] [{command}] failed to run.')
            return
        print(f'[+] [{command}] successfully ran.')

    def install_app_from_file(self, app_path):
        local_execute(app_path)

    def install_app_from_package(self, app_package):
        self._ssh_execute(f'apt-get install -y {app_package}')


class AndroidDB:
    def __init__(self):
        if its.on_windows:
            self.android_installer = f'{spy.ambassador_path}\\data\\bins\\adb\\windows\\adb.exe'

    def install_app_from_file(self, app_path):
        returncode, stdout, stderr = local_execute(self.android_installer + f' install {app_path}')
        if returncode:
            print(f'[-] Command [ ' + self.android_installer + f' install {app_path} ] failed to run')
            # todo: print stdout and stderr when a command fails
            return
        print(f'[+] Command [ ' + self.android_installer + f' install {app_path} ] ran successfully.')

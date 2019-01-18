import io
import re
import os
import six
import sys
import json
import errno
import ctypes
import logging
import datetime
import argparse
import platform
# Conda depends on requests, so safe to assume this will be present,
# also it will probably handle proxy on windows for us
import requests
import subprocess
from shutil import copyfile
from distutils.version import LooseVersion

# We need to know whether the host OS is 64 bit
is_os_64bit = platform.machine().endswith('64')

# We need to know if the python interpreter is 64 bit
is_py_64bit = sys.maxsize > 2**32

LOG_FILE = os.path.join(sys.prefix, 'vscode_inst.py.log')
logging.basicConfig(
    filename=LOG_FILE,
    filemode='w',
    level=logging.INFO
)
log = logging.getLogger('vscode_inst')

PKGS_DIR = os.path.join(sys.prefix, 'pkgs')
PY3 = (sys.version_info >= (3, 0))
PLAT = platform.system()
CMD_REQ_SHELL = False

DISTRO_MAP = {
    'rhel': '7',
    'sles': '12',
    'centos': '7',
    'debian': '8',
    'fedora': '23',
    'suse': '42.1',
    'ubuntu': '14.04'
}
DISTRO_NAME = ''
DISTRO_VER = ''

VSCODE_HOMEPATH = os.path.expanduser('~')

if PLAT == 'Windows':
    from knownfolders import get_folder_path, FOLDERID
    _kernel32 = ctypes.windll.kernel32
    _windir = ctypes.create_unicode_buffer(1024)
    _kernel32.GetWindowsDirectoryW(_windir, 1024)
    _windrive = _windir.value[:3]
    _fallback = os.path.join(_windrive, 'Program Files (x86)')
    PROGRAM_FILES = get_folder_path(FOLDERID.ProgramFilesX86)[0]
    LOCAL_APP_DATA = get_folder_path(FOLDERID.LocalAppData)[0]
    VSCODE_SUBDIR = 'win32-user'
    VSCODE_INST_EXT = 'exe'
    if is_py_64bit:
        VSCODE_SUBDIR = 'win32-x64-user'
        _fallback = os.path.join(_windrive, 'Program Files')
        PROGRAM_FILES = get_folder_path(FOLDERID.ProgramFilesX64)[0]
    if PROGRAM_FILES is None:
        PROGRAM_FILES = os.environ.get('ProgramFiles', _fallback)
    if  os.path.exists(os.path.join(PROGRAM_FILES, 'Microsoft VS Code')):
        VSCODE_INST_DIR = os.path.join(PROGRAM_FILES, 'Microsoft VS Code')
    else:
        VSCODE_INST_DIR = os.path.join(LOCAL_APP_DATA, 'Programs', 'Microsoft VS Code')
    VSCODE_EXE = os.path.join(VSCODE_INST_DIR, 'bin', 'code')
    CMD_REQ_SHELL = True
    VSCODE_APPDIR = get_folder_path(FOLDERID.RoamingAppData)[0]
    if VSCODE_APPDIR is None:
        VSCODE_APPDIR = os.path.join(VSCODE_HOMEPATH, 'AppData', 'Roaming')
elif PLAT == 'Darwin':
    VSCODE_SUBDIR = 'darwin'
    VSCODE_INST_EXT = 'zip'
    VSCODE_INST_DIR = os.path.join(os.path.expanduser('~'), 'Applications')
    VSCODE_EXE = os.path.join(
            VSCODE_INST_DIR,
            'Visual Studio Code.app', 'Contents/Resources/app/bin/code')
    VSCODE_APPDIR = os.path.join(VSCODE_HOMEPATH,
                                 'Library', 'Application Support')
elif PLAT == 'Linux':
    # platform.distribution() is not reliable on rolling distros like opensuse
    # tubleweed. Also, don't want to call conda's internal API directly
    _conda_info_args = [os.path.join(sys.prefix, 'bin', 'conda'),
                        "info", "--json"]
    _conda_info = subprocess.check_output(_conda_info_args,
                                          shell=CMD_REQ_SHELL)
    for distro in DISTRO_MAP.keys():
        _distro_regex = ".*{}/([^ ]*)".format(distro)
        m = re.match(_distro_regex,
                     json.loads(_conda_info)['user_agent'].lower())
        if m:
            DISTRO_NAME = distro
            DISTRO_VER = m.group(1)
            break
    if DISTRO_NAME in ['ubuntu', 'debian']:
        _pkg_type = 'deb'
    else:
        _pkg_type = 'rpm'
    _os_arch = 'x64' if is_os_64bit else 'ia32'
    VSCODE_SUBDIR = 'linux-{}-{}'.format(_pkg_type, _os_arch)
    VSCODE_INST_EXT = _pkg_type
    VSCODE_INST_DIR = '/usr/share/code'
    VSCODE_EXE = os.path.join(VSCODE_INST_DIR, 'bin', 'code')
    VSCODE_APPDIR = os.path.join(VSCODE_HOMEPATH, '.config')

VSCODE_ENDPOINT = 'https://vscode-update.azurewebsites.net/api/update/{}/stable/version'.format(VSCODE_SUBDIR) # NOQA
VSCODE_INSTFILE = os.path.join(PKGS_DIR, 'vscodetmp.%s' % VSCODE_INST_EXT)
VSCODE_PKGKEY_URL = "https://packages.microsoft.com/keys/microsoft.asc"

ERR_NO_VSCODE = 5
ERR_NO_INTERNET = 1
ERR_INSTALL_FAIL = 3
ERR_DOWNLOAD_FAIL = 2
ERR_NOT_SUPPORTED = 7
ERR_CONFIG_UPDATE_FAIL = 6
ERR_EXTENSION_INST_FAIL = 4


def isSupported():
    try:
        if PLAT == 'Windows':
            # Not checking XP, let their installer cry
            return True
        elif PLAT == 'Darwin':
            return LooseVersion(platform.mac_ver()[0]) >= LooseVersion('10.9')
        elif PLAT == 'Linux':
            _distro_min_ver = DISTRO_MAP[DISTRO_NAME]
            return ((len(DISTRO_NAME) > 0) and (len(DISTRO_VER) > 0) and
                    (LooseVersion(DISTRO_VER) >= LooseVersion(_distro_min_ver)))  # NOQA
    except Exception as e:
        log.exception('isSupported')
        return False
    return False


def haveInternet():
    try:
        requests.head(VSCODE_ENDPOINT, timeout=5)
        return True
    except Exception as e:
        log.exception('haveInternet')
        return False


def downloadVSCode():
    try:
        _vscode_url = requests.get(VSCODE_ENDPOINT).json()['url']
        r = requests.get(_vscode_url, stream=True)
        with open(VSCODE_INSTFILE, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
        return (os.path.exists(VSCODE_INSTFILE) and
                (os.path.getsize(VSCODE_INSTFILE) > 0))
    except Exception as e:
        log.exception('downloadVSCode')
        return False


def installVSCode():
    try:
        if PLAT == 'Windows':
            _vscode_install_args = [
                VSCODE_INSTFILE,
                '/VERYSILENT',
                '/MERGETASKS=!runcode',
                '/SUPRESSMSGBOXES',
                '/NORESTART',
                '/LOG={}'.format(os.path.join(sys.prefix, 'vscode_inst.log'))
            ]
            subprocess.check_call(_vscode_install_args, shell=CMD_REQ_SHELL)
        elif PLAT == 'Darwin':
            try:
                os.makedirs(VSCODE_INST_DIR)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    log.exception('installVSCode')
                    return False
            _vscode_install_args = [
                    '/usr/bin/unzip',
                    '-qo', VSCODE_INSTFILE, '-d', VSCODE_INST_DIR]
            subprocess.check_call(_vscode_install_args, shell=CMD_REQ_SHELL)
        elif PLAT == 'Linux':
            # rpm --import <http url> failed on suse with import read failed(2)
            _msft_key = requests.get(VSCODE_PKGKEY_URL)
            _msft_key_file = os.path.join(sys.prefix, 'pkgs', 'microsoft.asc')
            _msft_repo_file = os.path.join(sys.prefix, 'pkgs', 'vscode.repo')
            with open(_msft_key_file, 'wb') as f:
                f.write(_msft_key.content)

            if os.getuid() != 0:
                _sudo_cmd = ["sudo", "-ES"]
            else:
                _sudo_cmd = []

            def _write_repo_data(fpath, data):
                if fpath and data:
                    path = os.path.dirname(fpath)
                    subprocess.check_call(_sudo_cmd + ["mkdir", "-p", path])
                    with open(_msft_repo_file, 'w') as fh:
                        fh.write(data)
                    subprocess.check_call(_sudo_cmd + ["cp", _msft_repo_file, fpath])

            if DISTRO_NAME in ['ubuntu', 'debian']:
                subprocess.check_call(_sudo_cmd + ["apt-key", "add", _msft_key_file])
                # This can be non-zero if 404s are thrown. Continue anyway
                subprocess.call(_sudo_cmd + ["apt-get", "update"])
                subprocess.call(_sudo_cmd + ["apt-get", "install", "-y", "--force-yes",
                                             "apt-transport-https", "ca-certificates"])
                fpath = '/etc/apt/sources.list.d/vscode.list'
                data = """
deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main"""
                if is_os_64bit:
                    _write_repo_data(fpath, data)
                # This can be non-zero if 404s are thrown. Continue anyway
                subprocess.call(_sudo_cmd + ["apt-get", "update"])
                # This can be non-zero for missing deps
                if is_os_64bit:
                    subprocess.check_call(_sudo_cmd + ["apt-get", "install", "-y", "code"])
                else:
                    subprocess.call(_sudo_cmd + ["dpkg", "-i", VSCODE_INSTFILE])
                    subprocess.call(_sudo_cmd + ["apt-get", "install", "-yf"])
                # https://github.com/Microsoft/vscode/issues/13089
                # This can be non-zero if deps have changed in future releases
                subprocess.call(_sudo_cmd + ["apt-get", "install", "-y", "libgtk2.0",
                                             "libxss1", "libasound2", "libx11-xcb1"])
            elif DISTRO_NAME in ['centos', 'rhel', 'fedora']:
                fpath = '/etc/yum.repos.d/vscode.repo'
                data = """[code]
name=Visual Studio Code
baseurl=https://packages.microsoft.com/yumrepos/vscode
enabled=1
gpgcheck=1
gpgkey=https://packages.microsoft.com/keys/microsoft.asc"""
                if is_os_64bit:
                    _write_repo_data(fpath, data)
                subprocess.check_call(_sudo_cmd + ["rpm", "--import", _msft_key_file])
                _pkg_mgr = 'dnf' if DISTRO_NAME == 'fedora' else 'yum'
                subprocess.call(_sudo_cmd + [_pkg_mgr, "check-update"])
                if is_os_64bit:
                    subprocess.check_call(_sudo_cmd + [_pkg_mgr, "--assumeyes",
                                                       "install", "code"])
                else:
                    subprocess.check_call(_sudo_cmd + [_pkg_mgr, "--assumeyes",
                                                       "install", VSCODE_INSTFILE])
            elif DISTRO_NAME in ['suse', 'sles']:
                fpath = '/etc/zypp/repos.d/vscode.repo'
                data = """[code]
name=Visual Studio Code
baseurl=https://packages.microsoft.com/yumrepos/vscode
enabled=1
type=rpm-md
gpgcheck=1
gpgkey=https://packages.microsoft.com/keys/microsoft.asc"""
                _write_repo_data(fpath, data)
                subprocess.check_call(_sudo_cmd + ["rpm", "--import", _msft_key_file])
                subprocess.check_call(_sudo_cmd + ["zypper", "refresh"])
                if is_os_64bit:
                    subprocess.check_call(_sudo_cmd + ["zypper", "--non-interactive",
                                          "install", "code"])
                else:
                    subprocess.check_call(_sudo_cmd + ["zypper", "--non-interactive",
                                          "install", VSCODE_INSTFILE])
    except Exception as e:
        log.exception('installVSCode')
        return False
    return os.path.exists(VSCODE_EXE)


def installVSCodeExtenstions(extensions):
    _vscode_ext_args = [VSCODE_EXE, '--install-extension'] + extensions
    if PLAT == 'Linux':
        _vscode_ext_args += ["--user-data-dir=",
                             os.path.join(VSCODE_APPDIR, 'Code')]
    try:
        subprocess.check_call(_vscode_ext_args, shell=CMD_REQ_SHELL)
    except Exception as e:
        log.exception('installVSCodeExtenstions')
        return False
    return True


def haveVSCode():
    try:
        if PLAT == 'Windows':
            return (os.path.exists(VSCODE_EXE) or
                    os.path.exists(VSCODE_EXE.replace(' (x86)', '')))
        return os.path.exists(VSCODE_EXE)
    except Exception as e:
        log.exception('haveVSCode')
        return False
    return True


def updateVSCodeConfig():
    try:
        _vscode_config = os.path.join(VSCODE_APPDIR,
                                      'Code', 'User', 'settings.json')
        _vscode_config_dir = os.path.dirname(_vscode_config)

        try:
            if not os.path.isdir(_vscode_config_dir):
                os.makedirs(_vscode_config_dir)
        except Exception as e:
            log.exception('updateVSCodeConfig')
            pass

        config_update = {'python.pythonPath': sys.executable}

        if os.path.isfile(_vscode_config):
            try:
                # File already exists, so create a backup first
                date = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                _vscode_config_bak = os.path.join(
                  _vscode_config_dir,
                  _vscode_config.replace('.json',
                                         '.bak.{date}.json'.format(date=date)),
                )
                copyfile(_vscode_config, _vscode_config_bak)
                with io.open(_vscode_config, 'r', encoding='utf-8') as f:
                    data = f.read()
                    config_data = json.loads(data)
                    for key, val in config_update.items():
                        config_data[key] = val
            except Exception:
                config_data = config_update.copy()
        else:
            config_data = config_update.copy()

        mode = 'w' if PY3 else 'wb'
        with io.open(_vscode_config, mode) as f:
            json.dump(
              config_data,
              f,
              sort_keys=True,
              indent=4,
            )

    except Exception as e:
        log.exception('updateVSCodeConfig')
        return False

    _vscode_ext_args = [VSCODE_EXE, '--install-source', 'Anaconda-Installer']

    if PLAT == 'Linux':
        _vscode_ext_args += ["--user-data-dir=",
                             os.path.join(VSCODE_APPDIR, 'Code')]

    try:
        subprocess.check_call(_vscode_ext_args, shell=CMD_REQ_SHELL)
    except Exception as e:
        log.exception('updateInstallSource')
        return False

    return True


def abortRetryExecWait(msg, error_msg, error_code, func, *func_args):
    ret = False
    indent = ' '*3
    while not ret:
        print(msg)
        ret = func(*func_args)
        if ret is True:
            break
        print("%s%s" % (indent, error_msg))
        print("%sCheck %s for more info" % (indent, LOG_FILE))
        resp = ''
        while resp.lower() not in ['yes', 'no']:
            input_msg = "%sDo you wish to retry? [yes|no]\n[no] >>> " % indent
            resp = six.moves.input(input_msg)
            if resp.lower() == 'no':
                sys.exit(error_code)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description="vscode installation helper")

    p.add_argument(
            '--is-supported',
            action="store_true",
            help="check if vscode is supported")

    p.add_argument(
            '--check-existence',
            action="store_true",
            help="check if vscode is already installed")

    p.add_argument(
            '--check-connectivity',
            action="store_true",
            help="check network connectivity")

    p.add_argument(
            '--download-vscode',
            action="store_true",
            help="download latest vscode")

    p.add_argument(
            '--install-vscode',
            action="store_true",
            help="install vscode")

    p.add_argument(
            '--install-extensions',
            action="store",
            default=None,
            help="comma separated list of extensions to install")

    p.add_argument(
            '--update-vscode-config',
            action="store_true",
            help="update vscode config to point to python by AD")

    p.add_argument(
            '--handle-all-steps',
            action="store_true",
            help="perform the installation steps from start->end")

    args = p.parse_args()

    if args.is_supported:
        if not isSupported():
            sys.exit(ERR_NOT_SUPPORTED)

    if args.check_existence:
        if not haveVSCode():
            sys.exit(ERR_NO_VSCODE)

    if args.check_connectivity:
        if not haveInternet():
            sys.exit(ERR_NO_INTERNET)

    if args.download_vscode:
        if not downloadVSCode():
            sys.exit(ERR_DOWNLOAD_FAIL)

    if args.install_vscode:
        if not installVSCode():
            sys.exit(ERR_INSTALL_FAIL)

    if args.install_extensions:
        extensions = args.install_extensions.split(',')
        if not installVSCodeExtenstions(extensions):
            sys.exit(ERR_EXTENSION_INST_FAIL)

    if args.update_vscode_config:
        if not updateVSCodeConfig():
            sys.exit(ERR_CONFIG_UPDATE_FAIL)

    if args.handle_all_steps:
        if haveVSCode():
            print("VSCode is already installed!")
            sys.exit(0)
        abortRetryExecWait(
                "Checking Internet connectivity ...",
                "Please make sure you are connected to the internet!",
                ERR_NO_INTERNET,
                haveInternet)
        if not is_os_64bit or PLAT == 'Darwin':
            abortRetryExecWait(
                    "Downloading Visual Studio Code ...",
                    "Unable to download VSCode!",
                    ERR_DOWNLOAD_FAIL,
                    downloadVSCode)
        abortRetryExecWait(
                "Installing Visual Studio Code ...",
                "Unable to install VSCode!",
                ERR_INSTALL_FAIL,
                installVSCode)
        abortRetryExecWait(
                "Updating VSCode Config ...",
                "Unable to update VSCode config!",
                ERR_CONFIG_UPDATE_FAIL,
                updateVSCodeConfig)
        abortRetryExecWait(
                "Installing Extensions ...",
                "Unable to install python extensions for VSCode!",
                ERR_EXTENSION_INST_FAIL,
                installVSCodeExtenstions, ["ms-python.anaconda-extension-pack"])
        print("VSCode successfully installed in %s !\n" % VSCODE_INST_DIR)

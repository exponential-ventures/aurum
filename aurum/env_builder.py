#!/usr/bin/env python3
##
## Authors: Adriano Marques
##          Nathan Martins
##          Thales Ribeiro
##
## Copyright (C) 2019 Exponential Ventures LLC
##
##    This library is free software; you can redistribute it and/or
##    modify it under the terms of the GNU Library General Public
##    License as published by the Free Software Foundation; either
##    version 2 of the License, or (at your option) any later version.
##
##    This library is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
##    Library General Public License for more details.
##
##    You should have received a copy of the GNU Library General Public
##    License along with this library; if not, write to the Free Software
##    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
##


import logging
import os
import os.path
import subprocess
import sys
import tempfile
import venv
from subprocess import Popen, PIPE
from threading import Thread
from urllib.parse import urlparse
from urllib.request import urlretrieve


class ExtendedEnvBuilder(venv.EnvBuilder):
    """
    This builder installs setuptools and pip so that you can pip or
    easy_install other packages into the created virtual environment.

    :param progress: If setuptools or pip are installed, the progress of the
                     installation can be monitored by passing a progress
                     callable. If specified, it is called with two
                     arguments: a string indicating some progress, and a
                     context indicating where the string is coming from.
                     The context argument can have one of three values:
                     'main', indicating that it is called from virtualize()
                     itself, and 'stdout' and 'stderr', which are obtained
                     by reading lines from the output streams of a subprocess
                     which is used to install the app.

                     If a callable is not specified, default progress
                     information is output to sys.stderr.
    """

    def post_setup(self, context):
        """
        Set up any packages which need to be pre-installed into the
        virtual environment being created.

        :param context: The information for the virtual environment
                        creation request being processed.
        """
        os.environ['VIRTUAL_ENV'] = context.env_dir

        self.install_setuptools(context)

        # Can't install pip without setuptools
        self.install_pip(context)

    def reader(self, stream, context):
        """
        Read lines from a subprocess' output stream and either pass to a progress
        callable (if specified) or write progress information to sys.stderr.
        """

        while True:
            s = stream.readline()
            if not s:
                break

            sys.stdout.write(s.decode('utf-8'))
            sys.stdout.flush()
        stream.close()

    def install_script(self, context, name, url):
        _, _, path, _, _, _ = urlparse(url)
        fn = os.path.split(path)[-1]
        binpath = context.bin_path
        distpath = os.path.join(binpath, fn)
        # Download script into the virtual environment's binaries folder
        urlretrieve(url, distpath)

        term = '\n'

        sys.stdout.write(f'Installing {name}| ...%{term}')

        # Install in the virtual environment
        args = [context.env_exe, fn]
        p = Popen(args, stdout=PIPE, stderr=PIPE, cwd=binpath)
        t1 = Thread(target=self.reader, args=(p.stdout, 'stdout'))
        t1.start()
        t2 = Thread(target=self.reader, args=(p.stderr, 'stderr'))
        t2.start()
        p.wait()
        t1.join()
        t2.join()

        sys.stdout.write('done.\n')
        # Clean up - no longer needed
        os.unlink(distpath)

    def install_setuptools(self, context):
        """
        Install setuptools in the virtual environment.

        :param context: The information for the virtual environment
                        creation request being processed.
        """
        url = 'https://bitbucket.org/pypa/setuptools/downloads/ez_setup.py'
        self.install_script(context, 'setuptools', url)
        # clear up the setuptools archive which gets downloaded
        pred = lambda o: o.startswith('setuptools-') and o.endswith('.tar.gz')
        files = filter(pred, os.listdir(context.bin_path))
        for f in files:
            f = os.path.join(context.bin_path, f)
            os.unlink(f)

    def install_pip(self, context):
        """
        Install pip in the virtual environment.

        :param context: The information for the virtual environment
                        creation request being processed.
        """
        url = 'https://raw.github.com/pypa/pip/master/contrib/get-pip.py'
        self.install_script(context, 'pip', url)


def create_temporary_env(name: str):
    compatible = True
    if sys.version_info < (3, 3):
        compatible = False
    elif not hasattr(sys, 'base_prefix'):
        compatible = False
    if not compatible:
        raise ValueError('This script is only for use with '
                         'Python 3.3 or later')

    if os.name == 'nt':
        use_symlinks = False
    else:
        use_symlinks = True

    dir_name = os.path.join(tempfile.gettempdir(), name)

    clear = False

    if os.path.exists(dir_name):
        clear = True
    else:
        os.makedirs(dir_name)

    builder = venv.EnvBuilder(symlinks=use_symlinks, clear=clear, with_pip=True)
    builder.create(dir_name)

    return dir_name


def install_packages(env_dir, pip_file_contents: list):
    python_location = get_py_exe(env_dir)

    logging.debug(f"Running install_packages with python_location: {python_location}")

    update_pip(env_dir)

    logging.debug(f"Installing: {pip_file_contents}")

    proc = subprocess.Popen(
        [python_location, "-m", "pip", "install", *pip_file_contents],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    result, err = proc.communicate()

    if proc.returncode != 0:
        raise Exception(f"Failed to run pip install({proc.returncode}): {err}")

    return result.decode()


def get_py_exe(env_dir):
    executable = getattr(sys, '_base_executable', sys.executable)
    dirname, exe_name = os.path.split(os.path.abspath(executable))

    if sys.platform == 'win32':
        bin_name = 'Scripts'
    else:
        bin_name = 'bin'

    bin_path = os.path.join(env_dir, bin_name)

    return os.path.join(bin_path, exe_name)


def update_pip(env_dir):
    python_location = get_py_exe(env_dir)

    logging.debug(f"Running update_pip with python_location: {python_location}")

    proc = subprocess.Popen(
        [python_location, "-m", "pip", "install", "--upgrade", "pio"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    result, err = proc.communicate()

    if proc.returncode != 0:
        raise Exception(f"Failed to run pip upgrade: {err}")

    return result.decode()

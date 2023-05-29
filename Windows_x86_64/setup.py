import os
import shutil
import sys
from pathlib import Path
from setuptools import setup
from setuptools import Extension as BaseExtension
from distutils.command.build_ext import build_ext as build_ext

def cleanup():
    # Remove temporary directories created by this script
    shutil.rmtree(path="build", ignore_errors=True)
    shutil.rmtree(path="dist", ignore_errors=True)
    shutil.rmtree(path="PVRTexLibPy.egg-info", ignore_errors=True)

class CustomExtBuilder(build_ext):
    def build_extension(self, ext):
        if (isinstance(ext, Precompiled)):
            return ext.copy_precompiled(self)
        return super().build_extension(ext)

class Precompiled(BaseExtension):
    def __init__(self, name, precompiled, *args, **kwargs):
        super().__init__(name, [], *args, **kwargs)
        self.precompiled = os.path.abspath(precompiled)

    def copy_precompiled(self, builder):
        if (os.path.exists(self.precompiled)):
            path = Path(builder.get_ext_fullpath(self.name))
            path.parent.mkdir(parents=True)
            shutil.copyfile(
                self.precompiled,
                builder.get_ext_fullpath(self.name))
        else:
            print("Error: specified file %s not found!"%self.precompiled)
            cleanup()
            sys.exit()

if (not (sys.version_info.major == 3 and sys.version_info.minor == 9)):
    print('Please use Python version 3.9 to use this module')
    sys.exit()

setup(name='PVRTexLibPy',
    version='5.5.0',
    description='Python wrapper for PVRTexLib',
    author='Imagination Technologies',
    author_email='img-pvrdeveltechteam@imgtec.com',
    url='https://developer.imaginationtech.com/',
    script_args = ['install', '--user', '--prefix='],
    ext_modules=[
        Precompiled(
            "PVRTexLibPy",
            precompiled="PVRTexLibPy.cp39-win_amd64.pyd"),
        ],
    cmdclass={"build_ext": CustomExtBuilder})

cleanup()

interp_path = sys.executable
python_exe_name = "python"

if (interp_path != None and len(interp_path) > 0):
    python_exe_name = os.path.basename(os.path.abspath(sys.executable))

print("\n****To uninstall execute '%s -m pip uninstall PVRTexLibPy'\n"%python_exe_name)

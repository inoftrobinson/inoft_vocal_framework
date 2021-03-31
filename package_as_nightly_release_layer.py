import gzip
import os
import shutil
import subprocess
import sys
import tarfile

from serverlesspack.packages_lock_client import PackagesLockClient

version: str = subprocess.check_output('python setup.py --version').decode().replace('\n', '').replace('\r', '')

current_dirpath = os.path.dirname(os.path.abspath(__file__))
dist_dirpath = os.path.join(current_dirpath, 'dist')

setup_result = subprocess.run(f'python setup.py sdist')
print(f"setup result : {setup_result}")

p = PackagesLockClient()
p.open_requirements('requirements.txt')
print(p.requirements_modules)


def members(tf):
    l = len(f'inoftvocal-{version}/')
    mem
    for member in tf.getmembers():
        if member.path.startswith("subfolder/"):
            member.path = member.path[l:]
            yield member

tar = tarfile.open(f'dist/inoftvocal-{version}.tar.gz', 'r:gz')
tar.extractall(path='dist/packages', members=tar.getmembers())
subdir_and_files = [
    tarinfo for tarinfo in tar.getmembers()
    if tarinfo.name.startswith(f'inoftvocal-{version}/')
]
tar.extractall(path='dist/python/lib/python3.8/site-packages/inoft_vocal_framework', members=members(tar))

# python setup.py install --install-base ../dist/nightly

"""abs_path = os.path.abspath('dist/nightly')
if abs_path not in sys.path:
    sys.path.append(abs_path)
site_packages = os.path.join(abs_path, 'Lib/site-packages')
if not os.path.exists(site_packages):
    os.makedirs(site_packages)

e = os.path.join(site_packages, 'inoft_vocal_framework')
install_result = subprocess.run(f'python dist/packages/inoftvocal-{version}/setup.py install --prefix {abs_path} --install-lib=F:/Inoft/anvers_1944_project/inoft_vocal_framework/dist')  # --root=/')"""
# We use the setup.py file instead of pip in order to install the created package, because as of writing this, pip has
# a bug, where if we try to install a tar.gz file, with the --target attribute, the different folders of the tar.gz
# library will be installed in the same root as its library, instead of having its own reserved folder like we would
# have if we were installing the library without specifying a --target dirpath.

# install_result = subprocess.run(f'pip install dist/inoftvocal-{version}.tar.gz --target dist/nightly-release')

requirements_expression = " ".join([f'{item.module_name}{item.version_selector}{item.version}' for item in p.requirements_modules.values()])
requirements_result = subprocess.run(f'pip install {requirements_expression} --target dist/nightly/lib/site-packages')

tar_filepath = os.path.join(dist_dirpath, f'inoftvocal-{version}.tar.gz')
target_dirpath = os.path.join(dist_dirpath, 'nightly-release')

# package_layer_api(packages_names={tar_filepath}, target_dirpath=target_dirpath)

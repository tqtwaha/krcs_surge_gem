from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

from krcs_surge import __version__ as version

setup(
	name='krcs_surge',
	version=version,
	description='OneRC - VMMS for Kenya Red Cross Society',
	author='KRCS',
	author_email='admin@redcross.or.ke',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='daemons',
    version='1.3.0',
    url='https://github.com/kevinconway/daemons',
    license=license,
    description='Well behaved unix daemons for every occasion.',
    author='Kevin Conway',
    author_email='kevinjacobconway@gmail.com',
    long_description=readme,
    classifiers=[],
    packages=find_packages(exclude=['tests', 'build', 'dist', 'docs']),
    requires=[],
)

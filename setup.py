from setuptools import setup, find_packages


with open("README.rst") as f:
    readme = f.read()

setup(
    name="daemons",
    version="1.3.2",
    url="https://github.com/kevinconway/daemons",
    license="'Apache License 2.0",
    description="Well behaved unix daemons for every occasion.",
    author="Kevin Conway",
    author_email="kevinjacobconway@gmail.com",
    long_description=readme,
    classifiers=[],
    packages=find_packages(exclude=["tests", "build", "dist", "docs"]),
    install_requires=[],
)

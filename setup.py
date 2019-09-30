import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='frenchholidays',
    version='1.0.0-SNAPSHOT',
    scripts=['main.py'],
    author="Francois Valadier",
    author_email="francois.valadier@openvalue.fr",
    description="Toolbox about french holidays",
    long_description="Dataset for french general/public holidays + util functions",
    long_description_content_type="text/markdown",
    url="https://github.com/OpenValue/frenchholidays.git",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests',
        'numpy',
        'pandas',
        'python-dateutil'],
    classifiers=[
        "Development Status :: 2 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "License :: TF1 :: All rights reserved"
    ],
)

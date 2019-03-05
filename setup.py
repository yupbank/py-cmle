import setuptools

setuptools.setup(
    name='py_cmle',
    version='0.1.0',
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'start = py_cmle.start:main',
        ]
    }
)

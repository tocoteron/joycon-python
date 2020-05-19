from setuptools import setup, find_packages

version = "0.2.4"

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='joycon-python',
    version=version,
    description='Python driver for Nintendo Switch Joy-Con',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='tokoroten-lab, atsukoba, pbsds',
    author_email=', '.join([
        'tokoroten.lab@gmail.com',
        'atsuya_kobayashi@yahoo.co.jp',
        'pbsds@hotmail.com',
    ]),
    url='https://github.com/tokoroten-lab/joycon-python',
    license=license,
    packages=find_packages(),
    # install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3.7'
    ]
)

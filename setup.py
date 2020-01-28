from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='joycon-python',
    version='0.1.2',
    description='Python driver for Nintendo Switch Joy-Con',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='tokoroten-lab, atsukoba',
    author_email='tokoroten.lab@gmail.com, atsuya_kobayashi@yahoo.co.jp',
    url='https://github.com/tokoroten-lab/joycon-python',
    license=license,
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3.7'
    ]
)

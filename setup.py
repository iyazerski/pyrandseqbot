import setuptools

with open('README.md', 'r', encoding='utf-8') as fp:
    long_description = fp.read()

with open('requirements.txt', encoding='utf-8') as fp:
    requirements = fp.read().splitlines()

setuptools.setup(
    name='pyrandseqbot',
    version='0.0.1',
    author='Igor Ezersky',
    author_email='igor.ezersky.private@gmail.com',
    description='',
    include_package_data=True,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)

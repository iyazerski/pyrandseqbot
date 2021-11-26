import setuptools

from pyrandseqbot import __version__

with open('README.md', 'r', encoding='utf-8') as fp:
    long_description = fp.read()

requirements = []
for file in ['common', 'prod']:
    with open(f'requirements/{file}.txt', encoding='utf-8') as fp:
        for line in fp:
            if line.startswith('git'):  # handle private repositories
                requirements.append(f'{line.split("/")[-1].split(".git")[0]} @ {line}')
            elif line.startswith('-'):
                continue  # ignore other files including
            else:
                requirements.append(line)

setuptools.setup(
    name='pyrandseqbot',
    version=__version__,
    author='Ihar Yazerski',
    author_email='ihar.yazerski@outlook.com',
    description='Telegram bot that creates random sequences',
    include_package_data=True,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://t.me/pyRandSeqBot',
    packages=setuptools.find_packages(exclude=('tests*',)),
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)

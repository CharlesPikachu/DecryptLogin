'''
Function:
    setup
Author:
    Charles
微信公众号:
    Charles的皮卡丘
GitHub:
    https://github.com/CharlesPikachu
更新日期:
    2020-11-22
'''
import DecryptLogin
from setuptools import setup, find_packages


'''readme'''
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()


'''setup'''
setup(
    name=DecryptLogin.__title__,
    version=DecryptLogin.__version__,
    description=DecryptLogin.__description__,
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent'
    ],
    author=DecryptLogin.__author__,
    url=DecryptLogin.__url__,
    author_email=DecryptLogin.__email__,
    license=DecryptLogin.__license__,
    include_package_data=True,
    install_requires=['rsa >= 4.0', 'qrcode >= 6.1', 'pillow >= 6.0.0', 'PyExecJS >= 1.5.1', 'requests >= 2.22.0', 'pycryptodome >= 3.8.1', 'requests_toolbelt >= 0.9.1'],
    zip_safe=True,
    packages=find_packages()
)
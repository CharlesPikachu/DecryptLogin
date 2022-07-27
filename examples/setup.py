'''
Function:
    setup
Author:
    Charles
微信公众号:
    Charles的皮卡丘
GitHub:
    https://github.com/CharlesPikachu
'''
import DecryptLoginExamples
from setuptools import setup, find_packages


'''readme'''
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()


'''package data'''
package_data = {}
package_data.update({
    'DecryptLoginExamples.crawlers.qqreports': ['resources/*'] 
})


'''setup'''
setup(
    name=DecryptLoginExamples.__title__,
    version=DecryptLoginExamples.__version__,
    description=DecryptLoginExamples.__description__,
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent'
    ],
    author=DecryptLoginExamples.__author__,
    url=DecryptLoginExamples.__url__,
    author_email=DecryptLoginExamples.__email__,
    license=DecryptLoginExamples.__license__,
    include_package_data=True,
    package_data=package_data,
    install_requires=[lab.strip('\n') for lab in list(open('requirements.txt', 'r').readlines())],
    zip_safe=True,
    packages=find_packages()
)
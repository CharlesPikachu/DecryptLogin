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
	2020-04-12
'''
import DecryptLogin
from setuptools import setup, find_packages


'''readme'''
with open('README.md', 'r', encoding='utf-8') as f:
	long_description = f.read()


'''setup'''
setup(
	name='DecryptLogin',
	version=DecryptLogin.__version__,
	description='Login some website using requests.',
	long_description=long_description,
	long_description_content_type='text/markdown',
	classifiers=[
			'License :: OSI Approved :: MIT License',
			'Programming Language :: Python :: 3',
			'Intended Audience :: Developers',
			'Operating System :: OS Independent'],
	author='Charles',
	url='https://github.com/CharlesPikachu/DecryptLogin',
	author_email='charlesjzc@qq.com',
	license='MIT',
	include_package_data=True,
	install_requires=['rsa >= 4.0', 'qrcode >= 6.1', 'pillow >= 6.0.0', 'PyExecJS >= 1.5.1', 'requests >= 2.22.0', 'pycryptodome >= 3.8.1', 'requests_toolbelt >= 0.9.1'],
	zip_safe=True,
	packages=find_packages()
)
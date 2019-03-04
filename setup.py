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
	2019-03-04
'''
from setuptools import setup, find_packages


setup(
	name='DecryptLogin',
	version='0.1.0',
	description='Login some website using requests.',
	classifiers=[
			'License :: OSI Approved :: MIT License',
			'Programming Language :: Python',
			'Intended Audience :: Developers',
			'Operating System :: OS Independent'],
	author='Charles',
	url='https://github.com/CharlesPikachu/DecryptLogin',
	author_email='charlesjzc@qq.com',
	license='MIT',
	include_package_data=False,
	zip_safe=True,
	packages=find_packages()
)
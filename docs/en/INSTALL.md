# Install


#### Environment

Here is the basic environment information:

- OS: Win10 / Mac OS / Linux
- Python: 3.6~3.8


#### Dependency Package 

Dependencies requirement:

- rsa >= 4.0
- qrcode >= 6.1
- pillow >= 6.0.0
- requests >= 2.22.0
- pycryptodome >= 3.8.1
- requests_toolbelt >= 0.9.1
- gmssl >= 3.2.1
- PyExecJS >= 1.5.1 (the version of Node.js is v10.15.3 for my personal environment)


#### Pip Install

Run the following command in your terminal (Python should be in the develop environment):

```sh
pip install DecryptLogin
```


#### Source Code Install

**1.Online**

Run the following command in your terminal (Python and git should be in the develop environment):

```sh
pip install git+https://github.com/CharlesPikachu/DecryptLogin.git@master
```

**2.Offline**

First, you should clone the project in your computer:

```sh
git clone https://github.com/CharlesPikachu/DecryptLogin.git
```

Then, you should enter the project directory by running the following command:

```sh
cd DecryptLogin
```

Finally, you should run the following command in your terminal (Python should be in the develop environment) to install DecryptLogin:

```sh
python setup.py install
```
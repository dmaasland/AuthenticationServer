# AuthenticationServer
The [ESET Authentication Server](http://support.eset.com/kb2501/) implemented in python

## Introduction
This project aims to implement the ESET Authentication Server in python so that it can run on the ESET Security Management Center Appliance (or any other platform running python 3)

## Installation on ESMC appliance
Before you begin, open up a connection to the ESMC appliance and install the needed dependencies:
```shell
yum install git-core python36 python36-pip python36-devel gcc nginx
```

Then, go to the ESET folder and clone this repository:
```shell
cd /opt/eset
git clone https://github.com/dmaasland/AuthenticationServer.git
cd AuthenticationServer
```

Install the needed python dependencies:
```shell
pip3 install -r requirements.txt
```

Generate the RSA key:
```shell
python3 generate_key.py

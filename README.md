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
```

## Configuring nginx
Copy the example config over to the nginx 'conf.d' directory:
```shell
cp example_configs/authserver.conf /etc/nginx/conf.d/authserver.conf
```

Add port 3537 to the selinux policy:
```shell
semanage port -a -t http_port_t -p tcp 3537
```

Comment out the default server block in '/etc/nginx/nginx.conf' so that it looks like this:
```shell
[..]
    include /etc/nginx/conf.d/*.conf;

#    server {
#        listen       80 default_server;
#        listen       [::]:80 default_server;
#        server_name  _;
#        root         /usr/share/nginx/html;
#
#        # Load configuration files for the default server block.
#        include /etc/nginx/default.d/*.conf;
#
#        location / {
#        }
#
#        error_page 404 /404.html;
#            location = /40x.html {
#        }
#
#        error_page 500 502 503 504 /50x.html;
#            location = /50x.html {
#        }
#    }

# Settings for a TLS enabled server.

[..]
```

## Configure Authentication Server
Copy the systemd service file:
```shell
cp example_configs/authserver.service /etc/systemd/system/authserver.service
```

Change the network name to match your network in:
```
authserver.conf
```

This can be any name you like, just make sure to use the same name everywhere when setting up network authentication.

## Enable and start services
Enable and start the services:
```shell
systemctl enable nginx
systemctl enable authserver
systemctl start authserver
systemctl start nginx
```

## Open firwall ports
Create persistent iptables rules:
```shell
iptables -A INPUT -m conntrack --ctstate NEW -p tcp --dport 3537 -j ACCEPT
ip6tables -A INPUT -m conntrack --ctstate NEW -p tcp --dport 3537 -j ACCEPT
service iptables save
service ip6tables save
```

## Test
To test if everything is working, open your browser and go to:
```
http://<esmc>:3537
```

If everything is working, you should see the public key you can use to configure network authentication!
# AsteroidOSLinux
AsteroidOS Linux control application

## Prerequisites
  - pydbus
  - mpd
  - pyowm

Get the necessary modules with:

```    
pip3 install pydbus python-mpd2 pyowm
```

## Setup

Get the files:

```
git clone https://github.com/atx/AsteroidOSLinux.git
```

Switch to the directory:

```
cd AsteroidOSLinux/
```

Make sure your watch is already connected via bluetooth and run the example script:

```
./example.py
```

##Fork Additions
This repo has been forked from https://github.com/atx/AsteroidOSLinux.

### MQTT
Added mqtt publish to the notification.

message in the form of escaped JSON will be accepted.

e.g. 

`
mosquitto_pub -h 192.168.1.10 -m "{\"summary\":\"Alert from Server 1\",\"body\":\"CPU is toasty\"}" -t house/smartwatch`

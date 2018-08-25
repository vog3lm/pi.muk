### Quickstart

```
git clone https://github.com/vog3lm/pi.muk.git
cd pi.muk
python install.py
```

To start the application enter `muk start` into your CLI. This will start all tier processes at once. To kill them all enter `muk kill`. 

### Command Line

```
 Usage: muk [command] [options]
 
 Commands:

  help [arguments]..........: shows the application/a service help 
  kill [arguments]..........: kills the application/a service
  restart [arguments].......: restarts the application/a service
  start [arguments].........: starts the application/a service
  state [arguments].........: show the current application/service state
 
 Shell Options:

  [    | --only ]...........: reduces command scope to a single service
                              available services are : app and web
```

```
 Application Options:

  [ -h | --host ]..............: sets a custom socket url,
                                 default is 'localhost'
  [ -p | --port ]..............: sets a custom socket port,
                                 default is '9001'
  [    | --logfile ]...........: creates a log file in 'pi.muk/logs/'
  [    | --noshell ]...........: hides shell outputs
  [    | --verbose ]...........: selects a log detail level 
                                 available levels: 0,10.20,30,40,50
```

```
 Common Gateway Interface Options:

  [ -h | --gateway ]............: sets a webserver socket url,
                                 default is 'localhost:5000'
  [ -s | --socket ]............: sets a custom socket url,
                                 default is 'localhost:9002'

  [    | --logfile ]...........: creates a log file in the logfiles directory
  [    | --noshell ]...........: hides shell outputs
  [    | --verbose ]...........: selects a log detail level 
                                 available levels: 0,10.20,30,40,50
```

### Features

* auto install script
* object decorator pattern
* event driven programmflow
* null state pattern
* dynamic shell arg detection
* dynamic dependency injection
* three tier architecture
  * web interface (realtime)
  * device logics
  * database
* tls/ssl connections (external)
* custom ssl certificates
* web user interface
* user authentication
* login required watchdogs
* usb device control options
  * gamepad controller
  * keyboard controller
* remote device contorl options
  * web interface controller
  * gamepad controller
  * keyboard controller
* realtime video streaming
* multiple camera support

###### road map

* autonomous driver
* tls/ssl connections (internal)
* device sensor phalanx
* penetration testing toolkit
* WhatsApp implementation ?
* unit tests

### Hardware Setup

* [Sinoning SN700 Tank Chassis](https://www.sinoning.com/collections/cheap-tank-chassis/products/cheap-small-smart-robot-tank-chassis-tracking-car-diy-for-arduino-scm-2)
* [Cewaal Hot 2,4G Wireless Gamepad](https://de.aliexpress.com/item/Cewaal-Hot-2-4G-Wireless-Gamepad-PC-For-PS3-TV-Box-Joystick-2-4G-Joypad-Game/32834602683.html?spm=a2g0x.search0104.3.113.745b6181lTYe8Z&ws_ab_test=searchweb0_0,searchweb201602_4_10320_10152_10321_10151_10065_10344_10068_10342_10547_10343_10322_10340_10548_10341_10696_10084_5723616_10083_10618_10304_10307_10820_10821_10302_5011415_10843_10059_5011315_100031_10319_10103_10624_10623_10622_10621_10620,searchweb201603_2,ppcSwitch_4&algo_expid=571a2274-fe7d-4aca-a583-1adbccb89b15-17&algo_pvid=571a2274-fe7d-4aca-a583-1adbccb89b15&priceBeautifyAB=0)
* [Raspberry Pi Zero W (soldered)](https://shop.pimoroni.de/products/raspberry-pi-zero-w)
* [Class 10 SD Card](https://www.ebay.de/itm/32GB-64GB-128GB-256GB-Samsung-EVO-Micro-SD-SDHC-SDXC-CLASS-10-Ori-Sye-/263637314053?var=)

###### road map

* internal raspberry power supply
* night vision camera kit
* device sensor phalanx
* 360 degree tower


### Software Dependencies

### The Project

[Showcase Video 1](https://www.youtube.com/watch?v=mdP7mmwJS-4)


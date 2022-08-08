# Inventory-Pi
Simple inventory management software.

## The idea
To build a simple inventory management software on a small Raspberry Pi. The device would be installed near the access point to the inventory. Barcodes would be used to enter commands to minimize keyboard inputs.

An API call is made to [openfoodfacts.org](https://world.openfoodfacts.org/) to make adding new items is faster and easier.
This makes the present implementation more about groceries inventory management.

## The goal
Just a simple project to learn more about
* Python and JSON,
* API calls,
* SQLite, SQLalchemy and ORMs,
* Raspberry Pi,
* git and GitHub.

## Installation and user instructions
* Clone the repo locally on your device.
* Print the bar codes and keep near the scanning device.
* Run the script and scan the appropriate bar code.
* Scan your items.
* Type "exit" to quit the program.

### Packages / Requirements
* SQLalchemy
* Requests

``` shell
> pip install virtualenv
> cd .../Inventory-Pi
> virtualenv env
> source env/bin/activate
> pip install sqlalchemy requests
```

## TODO
* Web app to consult DB on phone, ask for low or out of stock items, etc.
* Add more DB/APIs to widen the range of products for automatic product name finding.

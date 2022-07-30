# Analyze F1
For all the F1 nerds. Compare and visualize telemetry data between drivers.

## Quick start

### Software requirements

- [Python >= 3.8](http://docs.python-guide.org/en/latest/starting/installation/)
- [pip](https://pip.pypa.io/en/stable/installing/)
- [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- [virtualenv](https://virtualenv.pypa.io/en/stable/installation.html) (Recommended)
It is recommended to install a python version 3.8 or 3.9 since *Analyze F1* relies on the python package [FastF1](https://github.com/theOehrly/Fast-F1) to gather data, where full functionalities are only avaiable on those python versions.

### Installation
A setup script is provided for easy installation. It is a easy as running
```
# Download `develop` branch of analyzef1 repository
git clone https://github.com/erdieee/analyzef1.git

# Enter downloaded directory
cd analyzef1

# --install, Install analyzef1 from scratch
./setup.sh -i
```
To update to new changes in the futures run
```
# --update
./setup.sh -u
```

### Run the script
Whenever you want to run the script you need to activate the virtual enviroment first.
```
# activate your virtual enviroment
source .env/bin/activate
# run it
python3 analyzef1
```
# Installing Software
Installation instructions for Python, HEAsoft, SNooPy, ds9 on GalliumOS Chromebook

**The following guide is assuming you have a fresh install of GalliumOS and proper sudo permissions**
___
## Installing Python 3.7
We'll be using Python 3.7 as it's one of the more recent, stable versions. You're free to use whichever version you want after 3.7.0, but the tutorial will cover 3.7.2. All the steps should be the same for any later version.

**Note, there are two versions of Python that ship with your computer. Do not delete these or your operating system will not work, as a lot of things depend on those versions.** For this reason, we are installing a separate version and using virtual env

### Installation Guide:
Go to [this website](https://tecadmin.net/install-python-3-7-on-ubuntu-linuxmint/) and follow the steps listed.
### Pip:
Pip is a package manager for Python. The Pip that ships with Python won't be up to date, so you'll need to update it. Since we are using Python3 instead of Python2, we only care about Pip3. 

To install Pip3, type: 
```
> sudo apt-get install pip3
```
You're all set to go with Pip3. We'll revisit this later.

### Setting up a Virtual Environment
Venv is a package that comes preinstalled with Python3. The purpose of a virtual environment is to create a separate workspace for you to install supporting packages that won't get in the way of your system-wide packages. It's also helpful when you need to know exactly which packages support a project, helping others jump right in and use your project.

To create a new virtual environment, type:
```
> python3.7 -m venv path/to/directory
```
This will create a new virtual environment in the directory you chose and install it with Python 3.7 as its default version of Python. To activate your virtual environment, type:
```
> source /path/to/directory/bin/activate
```
You should see the name of the directory in parenthesis to the left of your terminal prompt. Type `python --version` and you should see Python 3.7 returned.

Now type:
```
> pip3 install pip --upgrade
```
in your terminal to update your pip to the newest version. From here you can use `pip install [package name]` to install a package directly to your virtual environment. As long as you're in this environment, you will be able to install and use python packages that your scripts depend on without affecting your system-wide packages. If you need to start over, just delete your virtual environment and you're good to go.

**From here on out we'll be using this virtual env when we're installing programs**

When you need to deactivate your directory, just type `deactivate`.

### Installing Astropy
With your virtual environment active, type `pip install astropy`.
That's all!
### Installing HEAsoft
You'll want to download from [here](https://heasarc.gsfc.nasa.gov/lheasoft/download.html) and pick 'Linux - Ubuntu' from the list. Don't pick a pre-installed binary. In step 2, choose 'Swift' from the list and hit submit to download your file. Untar it with `tar -xvf [file_name.tar]. After this, I followed the installation instructions on [this site](https://heasarc.gsfc.nasa.gov/lheasoft/ubuntu.html). I chose to keep all the untar-ed folders in a separate directory to keep things organized, but you can do as you please.

### Installing ds9
We can download ds9 from [this link](http://ds9.si.edu/site/Download.html). What's important to note is that while our OS is based on Ubuntu, it is only based on Ubuntu 16. So make sure you pick that option from the download. If for some reason you have a different version of Ubuntu powering your OS, you'll want to download that version. You can check this by typing `lsb_release -a` in your terminal and noting what is returned under `Release:`. I'm pretty sure it's pre-compiled, so there shouldn't be much to do as long as you have X11 installed (a requirement of the HEAsoft installation)

### Installig SNooPy
Once again, installation instructions for SNooPy are [here](https://csp.obs.carnegiescience.edu/data/snpy/installing_snoopy2) in case you these instructions don't work. To install, type:
```
> git clone https://github.com/obscode/snpy.git snpy
```
while in a directory of your choosing. With your virtual environment activated, install the following Python packages:
* Numpy
* SciPy
* Matplotlib
* ipython
* pyfits
* pymc
* astropy

You should now be able to type:
```
> cd snpy
> python setup.py install
```
After it installs, you should be able to run it with 
```
> snpy
```
**Note this will only work if you have the virtual environment activated**

If for some reason this doesn't work, you can try:
```
pip install snpy
```
___
That's it for the installation of the software! Email tatewalker@tamu.edu if you have any questions.
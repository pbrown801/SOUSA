# Setting up Git and Github
Easy commands to setup a development environment on a fresh install of GalliumOS on a Chromebook.
___
## Check if Git is Installed on your Computer
Type `git` into your shell. If it returns:
```
bash: git: command not found
```
you don't have git installed. This is easy to fix! Just type:
```
sudo apt-get install git
```
and enter the sudo password when prompted. After downloading, type `git` and you should see a list of available commands.
## RSA Keys
### What is an RSA Key?
An RSA key is used to authenticate your computer with the GitHub server. An RSA key consists of a public and a private key. The public key tells the server what computer is accessing it, while the private key is used to ensure that it's actually you accessing the server. The private key is your digital fingerprint and therefore should be kept private. If it is leaked or someone else accesses it, they can pretend to be you in anything your public key is linked to. For our purposes, we'll assume our system is safe in our hands and leave it untouched.
### Check for Existing RSA Keys
To check for an existing RSA key, navigate to the .ssh folder under your home directory.
```
cd ~/.ssh
ls
```
You should see either an empty folder or a file called `known_hosts`. If you see files called `id_rsa` and `id_rsa.pub` then you already have RSA keys generated and can skip the next step.
### Generate a New RSA Key
To generate a new RSA key, type (quotes included):
```
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```
Press Enter at the next command to accept the default file location to save under.

When asked for a password, press Enter twice. This prevents you from having to enter your password with every push to GitHub.
### Adding your RSA Key to your GitHub Account
First create a GitHub account if you don't have one.

After signing in to GitHub, click on your icon in the top right corner to bring up a drop-down menu. Click on *Settings* then *SSH and GPG Keys* from the menu on the left.

Here you'll see all SSH keys associated with your GitHub account. Click the green button at the top that reads ***New SSH Key***.

Enter a title for your key (something to identify your computer should you need to delete this key later)

Back in your shell, navigate to your .ssh folder:
```
cd ~/.ssh
ls
```
Type:
```
cat id_rsa.pub
```
and copy the output to your clipboard.

Returning to GitHub, paste your key to the field marked *Key* and click the green button reading ***Add SSH key***
## Cloning a Git Repository from GitHub
To clone a Git repository from GitHub, you'll need to browse GitHub for the one you want. For our example, we'll use the SOUSA repository by Dr. Peter Brown from Texas A&M University. Click [here](https://github.com/pbrown801/SOUSA) to view the repository.

You'll see a green button in the top right that reads ***Clone or download*** click this and click *Use SSH* in the top of the drop-down. We are now given an address to put into our shell prompt. Copy this address to your clipboard.

Open up your shell and navigate to a directory where you want to clone the repository into. We are using a directory on our desktop.
```
cd ~/Desktop/Astro
```
Once inside, type:
```
git clone [paste address here]
```
If you followed the previous steps correctly, you should see a local copy of the repository in your chosen directory. From here, you can develop and interact with Git like usual. You will automatically have a remote established with the repository online called `origin`.
___
##### Last edited 2019-01-02 by Tate Walker
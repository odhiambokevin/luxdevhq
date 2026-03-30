# How To Install Microsoft Power Bi On VirtualBox In Ubuntu

Installing Microsoft Power Bi on Ubuntu is a fairly beginner-friendly process. We first start by spinning a virtual machine on our Ubuntu. VirtualBox is chosen for this case for its prominent use in the linux community.

#### 1. Download Virtualbox
Go to the download page of virtualbox linux download page [here](https://www.virtualbox.org/wiki/Linux_Downloads) and download the deb package for your Ubuntu distribution. To know the version of Ubuntu you are running open a terminal and type:
```bash
lsb_release -a
```
First ensure to update your package manager by typing `sudo apt update` on your terminal.

Install the .deb file you have downloaded. To do this, open the .deb download location and install it using `sudo dpkg -i your_virtualbox_download.deb` eg
```bash
sudo dpkg -i virtualbox-7.2_7.2.6-172322~Ubuntu~noble_amd64.deb
```

#### 2. Download the Windows .iso image
Next, we need to download an iso image which we will use to run the windows environment on Virtualbox. Go to [this link](https://www.microsoft.com/en-ca/software-download/windows10iso) and download an iso image for Windows.

#### 3. Create a virtual machine
With the Windows .iso image downloaded, launch the Virtualbox app from the app launcher. Click on **New** from the home dashbord.
![virtual box home dashboard](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ooe6lrs8vxzc7yh4ml6h.png)

Follow the series of prompts filling out the necessary details such as the name of the virtual machine. Select the .iso file you downloaded from the ISO Image dropdown.
![ISO Image select](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/nxkxwh7fhgilrkddnwgp.png)

Follow the prompts and enter all the necessary details. Remember your username and password as we will need them to log in to our Windows virtual machine. Assign a minimum of 4GB Ram in the Base Memory section. 6GB Ram is assigned here.
![Assigning RAM](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/oczjldp0moahp512rvph.png)

Click on `Finish` and allow it some time to install all the necessary requirements for your Windows environment.

#### 4. Open the Windows Virtual Machine
After the Windows installation, enter your username and password when prompted. You now have access to the Windows virtual machine.
![Windows environment](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/7s2uakud9gjpjaxxe5ck.png)

#### 5. Install Power BI
Launch the Microsoft Store, search for Power BI and proceed with guided steps on the installation.
![Power Bi MS Store](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/0g4q072p86opnmkllf74.png)

Alternatively, launch the `Edge` browser and search for Power Bi installation.
![Edge power bi](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/lnh6ndkfqru9aq4cwpwg.png)

Open the application after installation. Congratulations, you now have Power BI on your Ubuntu system.
![open powerbi](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/549p0lpqxw6n0xs9sc0c.png)
![Blank power bi](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/nxvc2bqipco0otdeaah7.png)


#### Tips
1. Always assign sufficient RAM to allow the resources to be well served.
2. Remember to keep your username and password secure.
3. Shut down the virtual machine from the Virtualbox window after use. Click on `File` then `Close` and select the `Power off the machine`
![Power off](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ezf9g0o3yqrl2ifmixi6.png)




# How Linux is Used in Real-World Data Engineering (For Beginners)

####Prerequisites
_1. A working public IP address to an Ubuntu server on the cloud_
_2. Access to admin user credentials (password or private key for key-based authentication)_

#### Linux For The Cloud
Data engineering is increasingly seeing the uptake of cloud infrastructure as essential in how firms manage their data. From storage, automation, and analysis, many tools and resources are now deployed in the cloud.

Working on Linux environments is an unspoken necessary skill for data engineers. There are tools and processes you will come across in the data engineering lifecycle for which you need to have skills on Linux. Linux servers are almost an intrinsic choice for cloud servers. Their ubiquity on the cloud is because they are lightweight and highly optimized for the cloud.

As such, navigating and running commands from the Linux terminal is the focus of this article. It gives you a beginner friendly feel to working from the terminal interface.

####Accessing the server
You need to be able to access the server remotely to do routine management and maintenance tasks. Open a terminal and type the following command:
```bash
ssh root@143.110.225.134
```
replace the IP address after the **@** sign with the actual server public IP address. The first time you log in to the server, your computer will prompt you to add the host to your local machine addresses of known hosts. Click `yes` to accept this step.

```bash
root@143.110.225.134's password: 
Welcome to Ubuntu 24.04.4 LTS (GNU/Linux 6.8.0-71-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/pro

 System information as of Wed Mar 25 14:54:56 UTC 2026

  System load:  0.0               Processes:             137
  Usage of /:   4.8% of 47.39GB   Users logged in:       4
  Memory usage: 20%               IPv4 address for eth0:143.110.225.134
  Swap usage:   0%                IPv4 address for eth0: 10.48.0.5

Expanded Security Maintenance for Applications is not enabled.

0 updates can be applied immediately.

Enable ESM Apps to receive additional future security updates.
See https://ubuntu.com/esm or run: sudo pro status


*** System restart required ***
Last login: Wed Mar 25 14:35:08 2026 from 41.99.105.22
root@ubuntu:~#
```

`_NOTE:` The numbers are fictional for demo only.
The line `root@ubuntu` indicates that we are logged in as user root and the name of the host/server machine is ubuntu. If you run the `pwd` command, you should see that you are inside the root folder as shown below.

```bash
root@ubuntu:~# pwd
/root
root@ubuntu:~# 
```
#### Creating a user
Now let us create a user called _odhiambo_ on this system. We use the `_adduser_` command as shown below.
```bash
root@ubuntu:~# sudo adduser odhiambo
```
You will get a prompt to set and confirm the password of the user. You will also get several optional prompts including to enter the full name and phone details. We skip these optional steps by just pressing _Enter_ at each prompt.

####Giving the user administrative privileges
The user _odhiambo_ does not have permission to run administrative tasks on the system. We then grant these privileges by adding the user _odhiambo_ to the `sudo` group with the following command:
```bash
root@ubuntu:~# sudo usermod -aG sudo odhiambo
```
The first `sudo` is to allow us to run the command without running into permission denied issues

The `usermod` command is for modifying system user settings

The ` -a ` instructs the system to _append_ the user with the ` G ` specifying the append is to a `group`. So the command is _appending to a group_

The group the user is being appended to is called _sudo_, which is the superuser group. This will give the user full access to all the privileges. However, they should invoke the `_sudo_` keyword before running these commands

The username being modified is _odhiambo_

####Logging in with our user account
We are now able to log on to the server using our user.
```bash
ssh odhiambo@143.110.225.134
```
We should see that the terminal should now indicate that we are logged in as _odhiambo_.
```bash
odhiambo@ubuntu:~$
```
#### A glimpse into the Linux file structure

For new Linux users, one of the most important things to have a fundamental understanding on  is the Linux file structure. The top-most level folder structure typically looks as shown below:
```bash
odhiambo@ubuntu:~$ ls /
bin                home               mnt   sbin.usr-is-merged  usr
bin.usr-is-merged  lib                opt   snap                var
boot               lib64              proc  srv
cdrom              lib.usr-is-merged  root  swap.img
dev                lost+found         run   sys
etc                media              sbin  tmp
odhiambo@ubuntu:~$ 
```
Here we have used the `ls` command that lists all the files in a folder. The `/` sign indicates that we want to view the files in the`root` ie _top most level_folder.While this file structure is not the focus of this article, I want to talk about the ``home folder``.

Notice that our path on the terminal when we logged in as _odhiambo_ included a tilde `~` ie `odhiambo@ubuntu:~$`. This is a shorthand to show that we are in our user's home folder, in this case, _odhiambo_'s home folder.

User's _home_ folder is different from the _home_ folder at the root level. All user accounts created on the system will have a folder with their name inside the root level home folder eg. _/home/odhiambo_. So in actuality, the path `odhiambo@ubuntu:~$` corresponds to `odhiambo@ubuntu:~$/home/odhiambo`

#### Handling files
A data engineer works a lot with files on the terminal. This includes making edits to configuration files, or making creating script from the terminal. Knowing the basics of file handling in data engineering in Linux server environment is important.

######1. Creating files
The most basic way to create a file is using the `touch` command with the file name.
```bash
touch orders.txt
```
This will create a file called _orders.txt_
```bash
touch orders.txt Manual.md suppliers.txt
```
This will create multiple files

######2. Deleting files
use `rm` to remove a file
```bash
rm orders.txt
```

######3. Listing files
We have already hinted at this before. The `ls` command lists files and folders
```bash
ls
```
This will list all files and folders on a path. File and folders are distinguished based on the colors. Files also may have an extension.
```bash
ls -a
```
This lists all files and folders, including hidden files and folders.

######4. Moving files
Moving a file does not leave a copy behind. We use the `mv` command followed with the _source file_ followed by the _destination path_.
```bash
mv orders.txt completed/
```
This moves the orders.txt to a folder called completed inside the current path. If the folder does not exist, the command will fail.

######5. Copying files
The `cp` command is used to copy files.
```bash
cp orders.txt completed/
```
This will copy the _orders.txt_ file into a folder called _completed_ in the current path. If the folder does not exist, the command fails.
```bash
scp orders.txt odhiambo@143.110.225.134:/home/odhiambo/orders/
```
This will copy the _orders.txt_ file from our _local machine_ to the server inside the _orders folder_ on the path shown. *Note:* You will be prompted to enter the server password. The `scp` allows to securely copy files over the internet.

#### File permissions
The last thing we will look at is a brief overview of file permissions in Linux. Use the `ls -l` command to view file permissions.
```bash
odhiambo@ubuntu:~/$ ls -l
total 0
-rw-rw-r-- 1 odhiambo odhiambo 0 Mar 27 13:04 orders.txt
odhiambo@ubuntu:~/$ 
```
Permissions in Linux are _*read*_, _*write*_ and _*execute*_ with their corresponding values as _4_, _2_ and _1_. So a value of _*7*_ means a user has all the three permissions (4+2+1).

In addition, the `ls -l` commands lists permissions in a 3 part string, _user_, _group_ and _other_. _r_, _w_ and _x_ correspond to the _read_, _write_ and _execute_ permissions.

The image below shows a summary of this.

![Permissions in Linux](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/tzycaqdwoo03jhp728k9.png)
<h6>photo from bytebytego.com</h6>

######cover photo by _pressfoto_ on _freepik_
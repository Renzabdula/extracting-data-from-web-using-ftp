EXTRACTING DATA FROM WEB TO FTP

Setting up wsl

1. setting-up WSL and installing vsftpd ("very secured file transfer protocold daemon")
	wsl --install -d Ubuntu 	==> installing Ubuntu
	-- creating username and password --
	sudo su ==> for you not to type your password every single time

	apt install vsftpd 	==> installing vsftpd
	ls /etc/ 	==> to check the vsftpd installed in the directory

2. adjusting vsftpd config
	cp /etc/vsftpd.conf /etc/vsftpd.conf_original	==> creating a copy of vsftpd
	nano /etc/vsftpd.conf	==> edit some setting in the vsftpd
	
	-- Update vsftpd.conf --
	local_enable=YES
	write_enable=YES
	chroot_local_user=YES
	chroot_list_enable=YES
	chroot_list_file=/etc/vsftpd.chrootlist
	ssl_enable=YES
	require_ssl_reuse=NO # add to the bottom of file

	systemctl restart vsftpd  ==> restarting the vsfptd after editing the config
	touch /etc/vsftpd.chroot_list  ==> creating a blank file using touch command for vsftpd.chroot_list

3. Create FTP user
	adduser <ftpuser>  ==> creating your choice user - i use ftpuser
	-- password  ==> password

	mkdir/home/ftpuser/ftp  ==> create a folder
	chown nobody:nogroup /home/ftpuser/ftp  ==> changing ownership
	chmod a-w /home/ftpuser/ftp  ==> revoking of other user to our folder
	sudo tee -a /etc/vsftpd.chroot_list  ==> add a new user to vsftpd.chroot_list

	ip address  ==> to get the ftphost
	

4. testing connection in python

from ftplib import FTP_TLS

ftphost = "172.24.203.113"
ftpuser = "ftpuser"
ftppass = "password"
ftpport = 21

ftp = FTP_TLS()
ftp.connect(ftphost, ftpport)
ftp.login(ftpuser, ftppass)
ftp.prot_p()



Using git

1. git init .  ==> initialize git

2. python -m venv env  ==> creating virtual env as env

3. .\env\Scripts\Activate.ps1  ==> activating environment in powershell

4. requirements.txt  ==> listing packages for installation in venv ex. pandas, pyarrow

5. (env)  pip install -r .\requirements.txt  ==> installint the packages listed in requirements

6. .gitignore  ==> create gitignore  file then paste the /env

7. in the env folder. Go to Activate.ps1 then save the credentials below 

# Add the venv to the PATH
Copy-Item -Path Env:PATH -Destination Env:_OLD_VIRTUAL_PATH
$Env:PATH = "$VenvExecDir$([System.IO.Path]::PathSeparator)$Env:PATH"

	# FTP Environment Variables
	$Env:FTPHOST = "172.24.203.113"
	$Env:FTPUSER = "ftpuser"
	$Env:FTPPASS = "password"
	$Env:FTPPORT = 21


OR

save it to the systems environment variables in start menu


8. ls /home/ftpuser/ -l		==> to check the content of the directory




#Something Whaley#
##CSeC{4nd_n0w_y0u_d0n7}##
##CSeC{qu1t3_4n_3y3_y0u_g07_7h3r3}##
##CSeC{n0w_y0u_s33_m3}##

I somehow found this challenge to be the easiest of all 4 (probably luck).

On opening the docker image, I started rummaging around the file system to get a rough idea of its setup.

```bash
	root@7eaecef7fdb1:/# ls
	bin  boot  dev  etc  home  lib  lib32  lib64  libx32  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
	root@7eaecef7fdb1:/# cd home/
	root@7eaecef7fdb1:/home# ls
	flag
	root@7eaecef7fdb1:/home# cd flag/
	root@7eaecef7fdb1:/home/flag# ls
	root@7eaecef7fdb1:/home/flag# ls -la
	total 20
	drwxr-x--- 2 CSeC{4nd_n0w_y0u_d0n7} flag 4096 May  4 17:35 .
	drwxr-xr-x 1 root                   root 4096 May  4 17:35 ..
	-rw-r--r-- 1 CSeC{4nd_n0w_y0u_d0n7} flag  220 May  4 17:35 .bash_logout
	-rw-r--r-- 1 CSeC{4nd_n0w_y0u_d0n7} flag 3771 May  4 17:35 .bashrc
	-rw-r--r-- 1 CSeC{4nd_n0w_y0u_d0n7} flag  807 May  4 17:35 .profile
```

Found the first flag in the `home` folder as one of the users.

I then went back to explore `root`.

```bash
	root@7eaecef7fdb1:/# cd root/
	root@7eaecef7fdb1:~# ls
	root@7eaecef7fdb1:~# ls -la
	total 24
	drwx------ 1 root root 4096 May  4 17:38 .
	drwxr-xr-x 1 root root 4096 May  5 19:58 ..
	-rw------- 1 root root   43 May  4 17:38 .bash_history
	-rw-r--r-- 1 root root 3142 May  4 17:34 .bashrc
	-rw-r--r-- 1 root root  161 Jul  9  2019 .profile
	-rw------- 1 root root 1293 May  4 17:37 .viminfo
	root@7eaecef7fdb1:~# cat .bash_history 
	echo CSeC{qu1t3_4n_3y3_y0u_g07_7h3r3}
	exit
	root@7eaecef7fdb1:~# 
```

Found the 2nd flag. Should've probably checked the `history` command at the start.

I was randomly looking at more files.

```bash
	root@7eaecef7fdb1:~# tail .bashrc 

	# enable programmable completion features (you don't need to enable
	# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
	# sources /etc/bash.bashrc).
	#if [ -f /etc/bash_completion ] && ! shopt -oq posix; then
	#    . /etc/bash_completion
	#fi


	export CTM="CSeC{n0w_y0u_s33_m3}"
```

Got the 3rd flag too!

I was probably gonna do a system wide `grep` or explore stuff more using `tree`/`find` but didn't get to that point.
import subprocess

output = subprocess.run(["ls", "-all"], capture_output=True)

print (output.stdout)

//b'total 12\ndrwxr-xr-x 1 root root 4096 Jan  5 06:15 .\ndrwxr-xr-x 1 root root 4096 Jan  6 02:26 ..\n-rw-r--r-- 1 root root  119 Jan  5 06:12 headlines.py\n'

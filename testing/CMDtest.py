import subprocess
import os
import sys

cwd = os.getcwd()


# p = subprocess.Popen("python "+cwd+"/tesFlask.py", stdout=subprocess.PIPE, shell=True)
# (output, err) = p.communicate()
# print "Today is", output

cmdping = "python "+cwd+"/tesFlask.py"
p = subprocess.Popen(cmdping, shell=True, stderr=subprocess.PIPE)

while True:
    out = p.stderr.read(1)
    if out == '' and p.poll() != None:
        break
    if out != '':
        sys.stdout.write(out)
        sys.stdout.flush()

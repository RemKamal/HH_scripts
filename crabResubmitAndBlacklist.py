import glob
import subprocess

dires = glob.glob('*')
for d in dires:
    cmd = "crab resubmit -d %s --siteblacklist=T2_US_UCSD" % d
    print 'cmd=', cmd
    subprocess.call(cmd, shell=True)



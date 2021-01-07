import os
import sys
 
TEST_CONF="""messagescan=no
hd=default,vdbench=/root/vdbench,user=root,shell=ssh
hd=hd1,system=inspur01
fsd=fsd1,anchor=/mnt/nfs01,depth=2,width=10,files=100,size=25k
fwd=format,threads=50,xfersize=4k
fwd=fwd1,fsd=fsd1,host=hd1,operation=read,fileio=random,fileselect=random,xfersize=4k,threads=50
rd=rd1,fwd=fwd*,fwdrate=max,elapsed=3,interval=1,format=yes
"""

def gen_test_file(file_name):
    '''
    description: generate the test script for vdbench tool
    param {*} file_name
    return {*} 
    '''
    with open(file_name, 'w') as fw:
        fw.write(TEST_CONF)
        fw.close()
    return
 
def run_vdbench():
    '''
    description: run the test tools: vdbench
    param {*}
    return {*}
    '''
    fileName = 'test'
    gen_test_file('./{}'.format(fileName))
 
    cmd='/root/vdbench/vdbench -f {}'.format(fileName) + ' -o /root/test_result/'
    os.system(cmd)

def read_file():
    '''
    description: read the output file of vdbench and get the metrics
    param {*}
    return {*} Metrics
    '''
    lines = []
    with open("/root/test_result/totals.html", 'r') as f:
        lines = f.readlines()
        metrics_list = lines[-1].split()
    metrics = []
    metrics.append(metrics_list[2])
    metrics.append(metrics_list[3])
    return [float(metrics_list[2]), float(metrics_list[3])]


if __name__ == '__main__':
    run_vdbench()
    read_file()
    sys.exit(0)

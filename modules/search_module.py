import os

# находим версию ядра
def get_kernel_version():
    os.system('uname -a > /tmp/kernal_version.txt')
    with open('/tmp/kernal_version.txt', 'r') as f:
        kernal_version = f.read()

        return kernal_version
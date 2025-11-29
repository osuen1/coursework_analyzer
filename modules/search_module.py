import os
import tempfile

# создаем временный файл
def create_temp_file():
    return tempfile.NamedTemporaryFile(mode='w+', delete=False)

# находим версию ядра
def get_kernel_version(target_os):
    kernal_version = ''

    if target_os == 'linux':
        with create_temp_file() as f:
            tmp_path = f.name
            os.system(f'cat /proc/version > {tmp_path}')

            with open(tmp_path, 'r') as f1:
                kernal_version = f1.read()
        
    elif target_os == 'macOS':
        with create_temp_file() as f:
            tmp_path = f.name
            os.system(f'uname -a > {tmp_path}')

            with open(tmp_path, 'r') as f1:
                kernal_version = f1.read()
    
    os.unlink(tmp_path)
    return kernal_version

# получаем историю команд bash
def get_bash_history():
    bash_history = ''
    with create_temp_file() as f:
        tmp_path = f.name
        os.system(f'cat ~/.bash_history > {tmp_path}')

        with open(tmp_path, 'r') as f:
            bash_history = f.read()

    os.unlink(tmp_path)
    return bash_history

# получаем SUID биты
def get_suid_bit():
    with create_temp_file() as f:
        tmp_path = f.name
        os.system(f'find / -type f -user root -perm -4000 > {tmp_path}')
        with open(tmp_path, 'r') as f:
            binaries = [line.strip() for line in f.readlines() if line.strip()]
        
        # Удаляем временный файл
        os.unlink(tmp_path)
        return binaries
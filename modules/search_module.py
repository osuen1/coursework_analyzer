import os
import tempfile
import subprocess

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
    try:
        result = subprocess.run (
            'find / -type f -user root -perm -4000 2>/dev/null',
            shell=True,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 1:
            binaries = [line.strip() for line in result.stdout.split('\n') if line.strip()]
            return binaries
        
        else:
            print(f'Ошибка выполнения команды: {result.stderr}')
        
    except subprocess.TimeoutExpired:
        print('Таймаут поиска SUID файлов')
        return []
    
    except Exception as e:
        print(f'Ошибка при поиске SUID файлов: {e}')
        return []
    
# получение root процессов
def get_root_process():
    try:
        result = subprocess.run(
            'ps -u root',
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            bin = [line.strip() for line in result.stdout.split('\n') if line.strip()]
            return bin
        else:
            print(f'Ошибка выполнения команды: {result.stderr}')
        
    except subprocess.TimeoutExpired:
        print('Таймаут поиска процессов')
        return []
    except Exception as e:
        print(f'Ошибка при поиске процессов: {e}')
        return []
    
# получаем SGID биты 
def get_sgid_bit():
    try:
        result = subprocess.run(
            'find / -type f -perm -2000 2>/dev/null', 
            shell=True,
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            binaries = [line.strip() for line in result.stdout.split('\n') if line.strip()]
            return binaries
        else:
            print(f'Ошибка выполнения команды: {result.stderr}')
    
    except subprocess.TimeoutExpired:
        print('Таймаут поиска SGID файлов')
        return []
    
    except Exception as e:
        print(f'Ошибка при поиске SGID файлов: {e}')
        return []
    
def get_word_writable_files():
    try:
        result = subprocess.run(
            'find / -perm -0002 -type f 2>/dev/null',
            shell=True,
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            binaries = [line.strip() for line in result.stdout.split('\n') if line.strip()]
            return binaries
        else:
            print(f'Ошибка выполнения команды: {result.stderr}')
            return []

    except subprocess.TimeoutExpired:
        print('Таймаут поиска world-writable файлов')
        return []
    except Exception as e:
        print(f'Ошибка при поиске world-writable файлов: {e}')
        return []

    
def get_word_writable_dirs():
    try:
        result = subprocess.run(
            'find / -perm -0002 -type d 2>/dev/null',
            shell=True,
            capture_output=True,
            text=True,
            timeout=60
        )

        if result.returncode == 0:
            dirs = [line.strip() for line in result.stdout.split('\n') if line.strip()]
            return dirs
        else:
            print(f'Ошибка выполнения команды: {result.stderr}')
            return []

    except subprocess.TimeoutExpired:
        print('Таймаут поиска world-writable директорий')
        return []
    except Exception as e:
        print(f'Ошибка при поиске world-writable директорий: {e}')
        return []
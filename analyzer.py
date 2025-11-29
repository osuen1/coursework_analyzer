from modules.search_module import get_kernel_version, get_suid_bit, get_root_process, get_bash_history

def summary():
    print('=============FOUND=============')
    print('==========KERNEL INFO==========')
    print(get_kernel_version('macOS'))

    print('===========SUID BITS===========')
    print(get_suid_bit())

    print('==========ROOT PROCESS=========')
    print(get_root_process())

def main():
    summary()

if __name__ == '__main__':
    main()
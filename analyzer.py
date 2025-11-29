from modules.search_module import get_kernel_version, get_suid_bit

def summary():
    print('=============FOUND=============')
    print('==========KERNEL INFO==========')
    print(get_kernel_version('macOS'))

    print('===========SUID BITS===========')
    print(get_suid_bit())

def main():
    summary()

if __name__ == '__main__':
    main()
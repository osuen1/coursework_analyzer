from modules.search_module import get_kernel_version, get_suid_bit 

def summary():
    print('=============FOUND=============')
    print('==========KERNEL INFO==========')
    print(get_kernel_version('linux'))

    print('==========SUID FILES==========')
    suid_bits_array = get_suid_bit()
    for i in suid_bits_array:
        print(i)

def main():
    summary()

if __name__ == '__main__':
    main()

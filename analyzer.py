from modules.search_module import get_kernel_version

def summary():
    print('=============FOUND=============')
    print('=============KERNEL INFO=============')
    print(get_kernel_version())


def main():
    summary()

if __name__ == '__main__':
    main()
import modules.search_module as sm

def summary():
    print('=============FOUND=============')
    print('==========KERNEL INFO==========')
    print(sm.get_kernel_version('macOS'))

    print('==========SUID FILES==========')
    suid_bits_array = sm.get_suid_bit()
    for i in suid_bits_array:
        print(i)

    print('==========SGID FILES==========')
    sgid_bits_array = sm.get_sgid_bit()
    for i in sgid_bits_array:
        print(i)

    print('==========ROOT PROCESS=========')
    root_processes = sm.get_root_process()
    for i in root_processes:
        print(i)

    print('======WORD-WRITABLE DIRS======')
    word_writable_dirs = sm.get_word_writable_dirs()
    for i in word_writable_dirs:
        print(i)
    
    print('=====WORD-WRITABLE FILES=====')
    word_writable_files = sm.get_word_writable_files()
    for i in word_writable_files:
        print(i)

    print('=====CRON JOBS=====')
    cron_jobs = sm.get_cron_jobs()
    print(cron_jobs)
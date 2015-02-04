from distutils.spawn import find_executable

compilers = ['g++', 'clang++', 'icc']
flags_dictionary = {
        'g++': ['-fPIC', '-shared'],
        'clang++': ['-fPIC', '-shared'],
        'icc': [],
        }

def compiler_and_flags():
    detected = next((comp for comp in compilers if find_executable(comp)), None)
    executable = find_executable(detected)
    return executable, flags_dictionary[detected]

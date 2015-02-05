from distutils.spawn import find_executable

compilers = ['g++', 'clang++', 'icc']
flags_dictionary = {
        'g++': ['-O2', '-g', '-fPIC', '-shared'],
        'clang++': ['-O2', '-g', '-fPIC', '-shared'],
        'icc': [], # to be defined
        }

def compiler_and_flags():
    detected = next((comp for comp in compilers if find_executable(comp)), None)
    executable = find_executable(detected)
    return executable, flags_dictionary[detected]

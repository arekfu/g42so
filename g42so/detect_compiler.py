from distutils.spawn import find_executable

COMPILERS = ['g++', 'clang++', 'icc']
FLAGS_DICTIONARY = {
    'g++': ['-O2', '-g', '-fPIC', '-shared'],
    'clang++': ['-O2', '-g', '-fPIC', '-shared'],
    'icc': [],  # to be defined
    }


def compiler_and_flags():
    detected = next((comp for comp in COMPILERS if find_executable(comp)),
                    None)
    executable = find_executable(detected)
    return executable, FLAGS_DICTIONARY[detected]

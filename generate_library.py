import detect_compiler
from distutils.spawn import find_executable
import subprocess
import shlex
import logging
import inspect
import os.path
import sys
import tempfile

def get_t4g4_wrapper_functions(d_wh):
    current_module = sys.modules[__name__]
    module_dir = os.path.dirname(inspect.getfile(current_module))
    template_fname = os.path.join(module_dir, 'wrapper.cc.in')
    with open(template_fname) as template_f: template = template_f.read()

    include_directives = ['#include "' + d_wh[1] + '"']
    includes = '\n'.join(include_directives)

    varname = 'a_detector'

    detector_class_name=d_wh[0]
    detector_params=''

    return template.format(includes=includes,
            varname=varname,
            detector_class_name=detector_class_name,
            detector_params=detector_params)

def compile(sources, includes, d_wh, output=None, other_flags=None, g4config_path=None):
    compiler, flags = detect_compiler.compiler_and_flags()

    # determine the Geant4-specific compilation flags
    if g4config_path:
        g4config = g4config_path
    else:
        g4config = find_executable('geant4-config')
        if not g4config:
            raise RuntimeError('cannot find the geant4-config executable. Please specify its location on the command line.')
    g4cli = [g4config, '--cflags', '--libs']
    g4process = subprocess.Popen(g4cli, stdout=subprocess.PIPE)
    g4flags_str = g4process.communicate()[0]
    g4flags = shlex.split(g4flags_str)

    # other flags if present
    if not other_flags: other_flags = []

    # include dirs
    include_flags = [ item for include in includes for item in ['-I', include] ]

    # output file
    if not output:
        output = 'lib' + d_wh[0] + '.so'
    logging.info('Will produce the following output file: ' + output)
    output_flags = ['-o', output]

    wrapper = get_t4g4_wrapper_functions(d_wh)
    logging.debug('wrapper code: ' + wrapper)

    with tempfile.NamedTemporaryFile(suffix='.cc', mode='w+') as wrapper_file:

        wrapper_file.write(wrapper)
        wrapper_file.flush()
        wrapper_file.seek(0)

        wrapper_file_name = wrapper_file.name

        # the CLI to execute
        compiler_cli = [compiler] + \
                flags + \
                g4flags + \
                other_flags + \
                include_flags + \
                sources + \
                [wrapper_file_name] + \
                output_flags

        logging.info('Running compilation...')
        logging.debug(' ... compiler CLI: ' + ' '.join(compiler_cli))
        subprocess.check_call(compiler_cli)

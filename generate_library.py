import detect_compiler
from distutils.spawn import find_executable
import subprocess
import shlex
import logging

def compile(sources, includes, d_wh, par_wh, output=None, other_flags=None, g4config_path=None):
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

    # the CLI to execute
    compiler_cli = [compiler] + flags + g4flags + other_flags + include_flags + sources + output_flags

    logging.info('Running compilation...')
    logging.debug(' ... compiler CLI: ' + ' '.join(compiler_cli))
    subprocess.check_call(compiler_cli)

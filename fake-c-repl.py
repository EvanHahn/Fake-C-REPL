#!/usr/bin/env python

import os

pounds = []
in_main = []

print 'Fake C REPL'

while True:

    try:
        command = raw_input('> ')
    except EOFError:
        exit(1)

    if command.startswith('//'):
        continue

    elif command.startswith('#'):
        add_command_to = pounds

    else:
        while not command.endswith(';'):
            command += '\n' + raw_input('')
        add_command_to = in_main

    add_command_to.append(command)

    pound_code = '\n'.join(pounds)
    main_code = ''.join((
        'int main(int argc, char** argv) {',
        ''.join(in_main),
        '}'
    ))

    source_file = os.tempnam() + '.c'
    exe_file = os.tempnam() + '.o'
    with open(source_file, 'w') as f:
        f.write('\n'.join((pound_code, main_code)))

    compile_command = ' '.join(('g++', source_file, '-o', exe_file))
    compile_status = os.system(compile_command)
    run_status = -1

    if compile_status == 0:
        run_status = os.system(exe_file)

    if (compile_status != 0) or (run_status != 0):
        add_command_to.pop()

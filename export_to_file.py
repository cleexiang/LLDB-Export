#!/usr/bin/python

import lldb
import subprocess
import optparse
import shlex
import sys

def create_save_options():
    usage = "usage: %prog <options> -- <expr>"
    parser = optparse.OptionParser()
    parser.add_option("-o", "--object", dest="objectName", help="input object")
    parser.add_option("-f", "--file", dest="filename", help="path to store variable", metavar="FILE")
    return parser

def export_command(debugger, command, result, internal_dict):
    """
    Overview:

    A command export NSString, NSDictionary, NSData, UIImage to a file on a location of Desktop.

    Example:
        export -o dic -f ~/Desktop/myDic.json
    """
    target = debugger.GetSelectedTarget()
    process = target.GetProcess()
    thread = process.GetSelectedThread()
    frame = thread.GetSelectedFrame()

    command_args = shlex.split(command)
    parser = create_save_options()
    (options, args) = parser.parse_args(command_args)
    objectToPrint = options.objectName
    path = options.filename

    if frame.IsValid():
        data = frame.EvaluateExpression('[NSJSONSerialization dataWithJSONObject:{} options:0 error:nil]'.format(objectToPrint))
        lengthCommand = "(NSUInteger)[({0!s}) length]".format(data.path)
        length = target.EvaluateExpression(lengthCommand).GetValueAsUnsigned()

        bytesCommand = "(const void *)[({0!s}) bytes]".format(data.path)
        bytes = target.EvaluateExpression(bytesCommand).GetValueAsUnsigned()

        error = lldb.SBError()
        memoryBuffer = process.ReadMemory(bytes, length, error)
        path='/Users/clee/Desktop/lala.txt'
        with open(path, "w") as dataFile:
            dataFile.write(memoryBuffer)

def __lldb_init_module(debugger, internal_dict):
    parser = create_save_options()
    # save_command.__doc__ = save_command.__doc__ + parser.format_help()
    debugger.HandleCommand('command script add -f export_to_file.export_command export')
    print 'The "export" python command has been installed and is ready for use'

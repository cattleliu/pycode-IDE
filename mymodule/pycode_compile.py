import py_compile,sys,pathlib

py_compile.compile(pathlib.Path(sys.argv[1]))
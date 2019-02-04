#!/usr/bin/env python3

import sys, os, secrets

def create_otp(length, path):
    bts = secrets.token_bytes(length)
    open(path, "wb+").write(bts)
    return bts

if len(sys.argv) == 2:
    indata = sys.stdin.buffer.read()
    otpdata = None

    if not os.path.exists(sys.argv[1]):
        otpdata = create_otp(len(indata), sys.argv[1])
    else:
        otpdata = open(sys.argv[1], "rb").read()
        #empty file
        if len(otpdata) == 0:
            otpdata = create_otp(len(indata), sys.argv[1])

    if len(otpdata) != len(indata):
        print("data lengths dont match", file=sys.stderr)
        sys.exit(1)

    os.write(1, bytes(b ^ otpdata[i] for i,b in enumerate(indata)))
elif len(sys.argv) == 3:
    otpdata = None
    indata = None

    use_stdout = False
    if os.path.exists(sys.argv[2]):
        #files real
        indata = open(sys.argv[2], "rb").read()
        if len(indata) == 0:
            #its empty
            indata = sys.stdin.buffer.read()
            use_stdout = False
        else:
            use_stdout = True
    else:
        indata = sys.stdin.buffer.read()
        use_stdout = False

    if not os.path.exists(sys.argv[1]):
        otpdata = create_otp(len(indata), sys.argv[1])
    else:
        otpdata = open(sys.argv[1], "rb").read()
        #empty file
        if len(otpdata) == 0:
            otpdata = create_otp(len(indata), sys.argv[1])

    if len(otpdata) != len(indata):
        print("data lengths dont match", file=sys.stderr)
        sys.exit(1)

    if use_stdout:
        os.write(1, bytes(b ^ otpdata[i] for i,b in enumerate(indata)))
    else:
        open(sys.argv[2], "wb+").write(bytes(b ^ otpdata[i] for i,b in enumerate(indata)))
elif len(sys.argv) == 4:
    otpdata = None
    indata = None

    if os.path.exists(sys.argv[2]):
        #files real
        indata = open(sys.argv[2], "rb").read()
        if len(indata) == 0:
            #its empty
            print("input file empty", file=sys.stderr)
            sys.exit(1)
    else:
        indata = sys.stdin.buffer.read()

    if not os.path.exists(sys.argv[1]):
        otpdata = create_otp(len(indata), sys.argv[1])
    else:
        otpdata = open(sys.argv[1], "rb").read()
        #empty file
        if len(otpdata) == 0:
            otpdata = create_otp(len(indata), sys.argv[1])

    if len(otpdata) != len(indata):
        print("data lengths dont match", file=sys.stderr)
        sys.exit(1)

    open(sys.argv[3], "wb+").write(bytes(b ^ otpdata[i] for i,b in enumerate(indata)))
else:
    print("if /path/to/otp doesnt exist it will be created, otherwise it will be used as is")
    print("if any file is empty it will be treated as non existant")
    print("usage: ./otp.py /path/to/otp")
    print("\tif no additional files are specified stdin and stdout will be used")
    print("usage: ./otp.py /path/to/otp /operation/file")
    print("\tif /operation/file doesnt exist stdin is assumed as input and the output will be written to /operation/file")
    print("\tif /operation/file exists it will be used as input and output will be written to stdout")
    print("usage: ./otp.py /path/to/otp /path/to/input /path/to/output")
    print("\t/path/to/input will be written to /path/to/output")
    sys.exit(1)

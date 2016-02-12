#!/usr/bin/python

import base64
import hashlib
import sys


#GLOBAL OPTIONS
OPT_NO_SPACE = False
OPT_NO_SPACE_NAME = '--no-spaces'



# DECODE/ENCODE FUNCS
def identity(s):
    return s


def hexdecode(s):
    if not OPT_NO_SPACE:
        s = s.replace(' ','')
    return s.decode('hex')

def hexencode(s):
    ret = s.encode('hex')
    if not OPT_NO_SPACE:
        ret = ' '.join(ret[i:i+2] for i in range(0, len(ret),2))

    return ret


def decdecode(s):
    if OPT_NO_SPACE:
        raise RuntimeError('Option %s is not supported with decimal decoding' % OPT_NO_SPACE_NAME)

    return ''.join(map(chr, map(int, s.split(' '))))

def decencode(s):
    return ' '.join(map(str, map(ord, [s[i] for i in range(0, len(s))])))


def bindecode(s):
    if not OPT_NO_SPACE:
        s = s.replace(' ','')

    return ''.join([chr(int(s[i:i+8], 2)) for i in range(0, len(s), 8)])

def binencode(s):
    j = '' if OPT_NO_SPACE else ' '
    return j.join([bin(ord(s[i]))[2:].zfill(8) for i in range(0, len(s))])



# ONE WAY FUNCS
def md5(s):
    return hashlib.md5(s).hexdigest()

def sha1(s):
    return hashlib.sha1(s).hexdigest()

def sha224(s):
    return hashlib.sha224(s).hexdigest()

def sha256(s):
    return hashlib.sha256(s).hexdigest()

def sha384(s):
    return hashlib.sha384(s).hexdigest()

def sha512(s):
    return hashlib.sha512(s).hexdigest()


# DEFAULTS
DEFAULT_DECODE = 'ascii'
DEFAULT_DECODE_FUNCTION = identity


# INPUT AND OUTPUT FORMATS
FORMATS = [
        ([DEFAULT_DECODE], identity, identity),
        (['base64', 'b64'], base64.b64decode, base64.b64encode),
        (['hex'], hexdecode, hexencode),
        (['dec'], decdecode, decencode),
        (['bin'], bindecode, binencode),
        ]

ONE_WAY_FUNCS = [
        (['md5'], None, md5),
        (['sha1'], None, sha1),
        (['sha224'], None, sha224),
        (['sha256'], None, sha256),
        (['sha384'], None, sha384),
        (['sha512'], None, sha512),
        ]

EXT_FORMATS = FORMATS + ONE_WAY_FUNCS

if __name__ == '__main__':

    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', '-l', '--list']:
        print 'Usage: %s [%s] [input-format=%s]' % (sys.argv[0], OPT_NO_SPACE_NAME, DEFAULT_DECODE)
        print 'Available input formats:'
        print '\n'.join(' %s' % ('/'.join(e[0])) for e in FORMATS)
        sys.exit(1)

    inputData = sys.stdin.read()
    decodeFunction = DEFAULT_DECODE_FUNCTION

    if len(sys.argv)>1:
        inputFormat = sys.argv[1]
        if sys.argv[1]==OPT_NO_SPACE_NAME:
            OPT_NO_SPACE = True
            inputFormat = DEFAULT_DECODE if len(sys.argv)<3 else sys.argv[2]

        for names, dfun, efun in FORMATS:
            if inputFormat in names:
                decodeFunction = dfun
                break

    try:
        rawData = decodeFunction(inputData)
    except Exception, e:
        print 'Error: invalid input (%s)' % repr(e)
        sys.exit(2)

    for names, dfun, efun in EXT_FORMATS:
        print '%s: %s' % (names[0], efun(rawData))

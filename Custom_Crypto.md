#Custom Crypto#
##CSeC{g18_m1r_37w4s_g31s7y420}##
####claw = 7233####

The code was slightly modified after I'd solved it, hence my solution is slightly unoptimized wrt the current code.

I first had a look at the `chall.py` code.

A few things were obviously popping out - 

1. The `secret` module was missing which included 2 variables claw and THREAT (to be figured out)
2. The `spooky_fn` function **was trying to be** a prime checker
3. The constraints on `claw` and `len(THREAT)` were important

Upon further inspection, I realised that -

1. `jack_o_lantern` is basically an array of binary representation of `claw`
2. `epitaph` on Line 32 is basically `THREAT*len(THREAT)`
3. `epitaph` on Line 34 is a subset of characters of original `epitaph` selected using repeated bin rep of `claw`
4. The last line was encrypting the `eptiaph` on Line 34 by `base64` and writing it to `chocolate.txt`

Hence, my first step was to decode the string given in `chocolate.txt`. It now read - 
`CSe1_37wg420}Cm1r_4s7y4C18_m3g31s2C{g114s_g7CSeC837w4320}C{1r_3s7y42S8_m1731s70{g18rs_g3ySeC{_7w4s10}CSgr_37_y420e_m1rw1s7y}g18___g314eC{gmw4s_s}`

This seemt like a bunch of repeated `CSeC{...}` flags with characters missing, making it seem I was on the right path.

Before bruteforcing anything, I wanted to bound my flag length using some heuristics.

Firstly, the binary rep of `claw` can have at the most 13 `1s` due to the constraints. Assuming the flag is of length > 13 (decent assumption), the total number of `1s` in `jack_o_lantern*len(THREAT)` is `<=` number of characters in `THREAT*len(THREAT)`. Hence, due to the implementation of `itertools.compress`, the length of final `base64` string will be a multiple of `len(THREAT)`. 

Now, the length of `base64` string was `145 = 5 x 29` which was great for me since it essentially fixed `len(THREAT) = 29` for obvious reasons.

I could now assume my `THREAT` (or flag) was `CSeC\{[.]{23}\}` (RegEx).

I converted the given code into a functional form for better utility.

```python
	def gen(claw, THREAT):
	    #convert claw to binary
	    jack_o_lantern = list(map(int, list(bin(claw)[-len(bin(claw))+2:len(bin(claw))])))

	    # print(("0b"+"".join([str(x) for x in jack_o_lantern]))==bin(claw))

	    #epitaph = threat * len(threat)
	    epitaph = []
	    for cobweb in range(len(THREAT)):
	        epitaph.extend(THREAT)
	    epitaph = "".join(epitaph)

	    # print(epitaph == THREAT*len(THREAT))
	    epitaph = "".join(list(compress(epitaph, jack_o_lantern*len(THREAT))))
	    return epitaph
```

I also wrote a compare function to see whether `gen(my_claw, my_threat)` fits the given output.

```python
	def compare(generated, given):
	    if len(s) != len(sn):
	        return False

	    for i in range(len(s)):
	        if generated[i] != given[i] and generated[i] != ".":
	            return False
	    return True
```

And I finally ran the bruteforce,

```python
	myTHREAT = "CSeC{.......................}"
	for claw in range(int(1e+0), int(1e+4)):
	    if compare(gen(claw, myTHREAT), given):
	        print(claw, gen(claw, myTHREAT), sep="\n")
```

This gives only 1 value of `claw = 7233` and we are basically done.

To get the final flag,

```python
	claw = 7233
	jack = list(map(int, list(bin(claw)[-len(bin(claw))+2:len(bin(claw))])))
	binarr = jack*29
	c = 0
	ans = ["."]*29
	for i in range(145):
		if binarr[i] == 1:
			ans[i%29] = given[c]
			c += 1
	print("".join(ans))
```

Phew!

```bash
	satyankar@Satyankars-MacBook-Air Custom_Crypto % python3 test.py
	CSeC{g18_m1r_37w4s_g31s7y420}	
```

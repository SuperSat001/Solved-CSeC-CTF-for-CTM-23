from itertools import *
from secret import claw, THREAT
from math import sqrt as will_o_the_wisp
from base64 import b64encode as hauntify
import sys
from secret import possible

# claw = int(sys.argv[1])

# prime checker
def spooky_fn(ghost):
    casper = 0
    if(ghost > 1):
        for lady_love in range(2, int(will_o_the_wisp(ghost)) + 1):
            if (ghost % lady_love == 0):
                casper = 1
            break
        if (casper == 0):
            return True
        else:
            return False
    else:
        return False


assert claw in range(int(1e+0), int(1e+4))
assert len(THREAT) <= 30
assert spooky_fn(len(THREAT)) #2, 3, 5, 7, 11, 13, 17, 19, 23, 29

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

# print(epitaph, epitaph.encode(), hauntify(epitaph.encode()), sep="\n")

# with open("chocolate.txt", 'w') as f:
#     f.write(hauntify(epitaph.encode()).decode())

# print(epitaph)

def compare(s, sn):
    if len(s) != len(sn):
        return False

    for i in range(len(s)):
        if s[i] != sn[i] and s[i] != ".":
            return False
    return True

to_get = "CSe1_37wg420}Cm1r_4s7y4C18_m3g31s2C{g114s_g7CSeC837w4320}C{1r_3s7y42S8_m1731s70{g18rs_g3ySeC{_7w4s10}CSgr_37_y420e_m1rw1s7y}g18___g314eC{gmw4s_s}"

print(len(to_get))

for THREAT in possible:
    for claw in range(int(1e+0), int(1e+4)):
        if compare(gen(claw, THREAT), to_get):
            print(claw, gen(claw, THREAT), sep="\n")
            jack_o_lantern = list(map(int, list(bin(claw)[-len(bin(claw))+2:len(bin(claw))])))
            print(jack_o_lantern*len(THREAT))




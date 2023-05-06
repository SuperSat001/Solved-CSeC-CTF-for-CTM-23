from itertools import compress
from secret import claw, THREAT
import sys

s = "CSe1_37wg420}Cm1r_4s7y4C18_m3g31s2C{g114s_g7CSeC837w4320}C{1r_3s7y42S8_m1731s70{g18rs_g3ySeC{_7w4s10}CSgr_37_y420e_m1rw1s7y}g18___g314eC{gmw4s_s}"

#print(len(s))

primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

alists = ["a"*p for p in primes]

def makebin(n):
	return [int(k) for k in bin(n)[2:]]

def func(s, n):
	return list(compress(s*len(s), makebin(n)*len(s)))

def make2darr(arr, n):
	return [arr[i:min(i+n, len(arr))] for i in range(0, len(arr), n)]


# for strs in alists:
# 	for num in range(int(1e+0), int(1e+4)):
# 		if len(func(strs, num)) == 145:
# 			print(len(strs), num)
# 			arrx = make2darr(makebin(num)*len(strs), len(strs))
# 			for arr in arrx:
# 				print(arr, sum(arr))

binarr = makebin(7233)*29
arrx = make2darr(binarr, 29)


def compare(sn):
	if len(s) != len(sn):
		return False

	for i in range(len(s)):
		if s[i] != sn[i] and sn[i] != ".":
			return False
	return True

# sn = sys.argv[1]
# print(compare(sn))
c = 0
ans = ["."]*29
for i in range(145):
	if binarr[i] == 1:
		ans[i%29] = s[c]
		c += 1
print("".join(ans))


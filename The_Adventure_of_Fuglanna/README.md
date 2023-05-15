# The Adventure of Fuglanna

## `IITB{\x41rDuiN0_1$_f0r_Dumm13zZ}`

#### key = `{3,6,2,1,0,5,4,7}`
#### iv (First) = 69
#### iv (Second) = 0

This was a very hard problem. I had to make several guesses while solving, and was only able to obtain the flag because the first encryption was rather weak (by design).

Unlike the other problems, this took me over 3 days to solve. I'll write down my experience day-wise.

<span style="color:blue; font-size:25px">Day 1</span>

I was quite surprised to see a `.ino` Arduino source code file in the problem, and started analysing it as the statement hinted.

Immediate observations -
- The flag string is being encrypted character by character
- Part of code looks like a shuffling of 8 bits (which is also the size of `char` variable)
- `output` array is being printed by character to the `Serial Monitor`, this will reflect in the `.pcapng` file
- All this is inside `void loop(){}` which means `.pcapng` file will have multiple repeating strings (the doubly encrypted flag)

I started looking at the code line by line now, to understand it and write a decryption scheme.

I had a few more observations -
- The `len = 32` statement was present in the code, which meant the `enc_flag` was actually of 32 length. 
(If the `"[REDACTED one time encrypted flag]"` string was also 32 characters long, the `len` variable might have been tampered too).
- The `char iv = digitalRead(8)` was either `\0 (NUL)` or `\x01 (SOH)`.
It was being used to `XOR x` , which means either `x` was not being changed `(^0)` or the last bit was being flipped `(^1)`.
- The code `int b = (x >> j) & 1;` gives the `j`th bit of `x` and `acc |= (b << key[j]);` adds this bit to the `key[j]`th position of `acc`.
This was a crucial observation and helped very much later.
- `iv` kept changing, for the `i >= 1`th character, it was the encoded value of the `i-1`th character.

I wrote the decrypting code in C++ to avoid any `char <-> int` conversion errors.

```cpp
    void reverseKeys(int keys[], int rkeys[]){
        rep(i,8)rkeys[keys[i]] = i;
    }

    void decode(char arr[], char decoded[], int n, int rkeys[], int iv){
        int acc;
        for(int i = n-1; i > 0; i--){
            acc = 0;
            for( int j = 0; j < 8; j++){
            int b = (arr[i] >> j) & 1;
            acc |= (b << rkeys[j]);
            }
            acc ^= arr[i-1];
            decoded[i] = acc;
        }

        acc = 0;
        for( int j = 0; j < 8; j++){
        int b = (arr[0] >> j) & 1;
        acc |= (b << rkeys[j]);
        }
        acc ^= iv;
        decoded[0] = acc;
    }
```

Now, I was ready to start exploring the `.pcapng` file.

<hr>

Obviously, Arduino was on the `1.14` series as it (mostly `1.14.3`) had a lot of transfers to `host`.

I had never worked on a `USB` protocol file, and had to Google where the communicated data is.

A quick search showed that the `leftover capture data` is the actual data transmitted by the device. I extracted this data to a text file for further analysis.

```bash
tshark -r data.pcapng -Y 'usb.capdata && usb.src == "1.14.3"'  -T fields -e usb.capdata > usbdata.txt
```

I performed a basic frequency analysis on the lines of the `usbdata.txt` file.

```py
    freq = dict()

    with open("usbdata.txt") as file:
        for line in file.readlines():
            line = line.strip()
            if line not in freq:
                freq[line] = 1
            else:
                freq[line] += 1

    for line in freq:
        if freq[line] > 10:
            print(freq[line], line)
```

The output is something like -

```
    .....
    48 000d0a44
    47 0a444308
    46 023b5d13
    47 63300a2d
    46 7f052a2e
    47 2f5e5202
    46 2c385d37
    47 6d165d65
    46 16480d0a
    47 4308023b
    47 5d136330
    46 0a2d7f05
    47 2a2e2f5e
    47 52022c38
    47 5d374a11
    47 366d165d
    46 6516480d
    47 0a000d0a
    47 44430802
    .....
```

which was showing many repeated elements showing that I was on the right path.

I concatenated the lines and opened them in a text editor. By searching for some of these patterns I realised that the 74 length string `000d0a444308023b5d1363300a2d7f052a2e2f5e52022c385d374a11366d165d6516480d0a` had nearly 150 repeats.

![Repeats](https://i.imgur.com/V7IIiiP.png)

Now, this string has 3 parts -

`000d0a` + `444308023b5d1363300a2d7f052a2e2f5e52022c385d374a11366d165d6516480d` + `0d0a`

The first part is `00 = digitalRead(8)` + `0d0a` (enter + newline from `Serial.println()`).
The second part is `output` which I'll call the `double_enc_flag`.
The third part is `0d0a` again from `Serial.println()`.

**At this point, I got stuck.**

I assumed that the Arduino is set up something like 

![Wokai sim](https://i.imgur.com/r9iFI7r.png)

and I knew that `digitalRead(8)` will output `LOW (0)` or `HIGH (1)` depending on the button being pressed.

Hence, I expected other than the `000d0a[output1]0d0a`, the `usbdata.txt` will consist of repeated strings `010d0a[output2]0d0a` when `iv = 1`.

`output1` and `output2` should be very different strings (which I confirmed after running the code and pressing/releasing button) as the difference in 1st encoded character will cause changes in every following character.

However, this was not the case in `usbdata.txt`. The text other than `000d0a[output1]0d0a` was very similar to it.

Initially, I thought that this was due to a special `key` array, and this itself was a **hint** to finding the `key`.

*Couldn't have been more wrong tbh.*


<span style="color:blue; font-size:25px">Day 2</span>

I started with my previous progress, to try find some keys (using brute force) which give similar outputs at `iv = 0 and 1` but was not able to find any. So I left this aside for a while, and started looking at the `.pcapng` file for the key again.

I had a new observation, whenever there was a break in the repeating `000d0a[output1]0d0a` units, the `Info` column of WireShark showed `USB_BULK In, Rcvd AT Command : DC` instead of the usual `USB_BULK In`. And then the Arduino sent data similar to the repeating string, but with few missing characters (generally at the start).

I tried Googling about this `Info` but got very sparse results. From what I understood, the Arduino periodically received `AT = Attenuation` command from the `host` to check if it was functioning properly, and during this command, there was some packet/data loss between the Arduino and host.

This was causing some strings with few missing characters from the `double_enc_flag`.

I was still put off by the fact that I was still seeing only 1 flag whereas 2 very different flags are expected.

I started searching for the 2nd flag in the earlier part of `usbdata.txt` as well but with no avail (there were so few `01` strings in the whole file).

After much searching, I assumed that the person never pressed the button and there was only 1 flag in the `.pcapng` file.

<hr>

The next problem was finding the `key`.

I had a strong feeling that the `key` was supposed to be extracted from the complied code being transferred from `host` to `1.14.4` at the start, but had no idea how to extract/make sense of it.

As usual, I started bruteforcing the key.

```
The code `int b = (x >> j) & 1;` gives the `j`th bit of `x` and `acc |= (b << key[j]);` adds this bit to the `key[j]`th position of `acc`.
This was a crucial observation and helped very much later.
```

It's pretty impossible to bruteforce a random key (8^8 and maybe even more choices) so some restrictions were required.

After some thinking, I made a good assumption that `key` array is a permutation of `0..7` (in any of the 8! ways).

There are some issues otherwise - 
1. If $\text{key}[i] >= 8$ for some $i$
The `char` datatype is 8-bit and stores numbers $\mod {256}$. Hence the number $(1 << \text{key}[i]) \geq 2^8$ will overflow `char` and will be removed. The bit at `i`th position of `x` will be lost.
2. If $\text{key}[i] = \text{key}[j] = k$ for some $i \neq j$
This time, the `k`th bit of `acc` will be (`i`th bit | `j` th bit) of `x` which leads to loss of information when the bits are different (we can't distinguish between 01, 10 and 11).

From my understanding, our encoding should be one-to-one, otherwise the intended receiver itself will not be able to decode it.

This is only possible (for all strings to be encoded) when `keys` is a permutation and hence the operation we are performing is a one-one binary shuffle.

I wrote the bruteforce

```cpp
    rep(i, fact(8)){
        reverseKeys(keys, rkeys);
        decode(arr, decoded, n, rkeys, 0);

        vout(keys);
        cout<<" "<<k<<" ";
        vout(decoded);
        cout<<"\n";

        next_permutation(keys, keys+8);
    }
```

What I *wrongly* assumed was, since the `enc_flag` string was written in the `evil.ino` file using a keyboard, the correct encoded string would only contain printable ASCII characters (HEX > `\x20`).

I piped the output of my bruteforce to a file, and started looking for such strings.

It was very sad to see that almost all of the strings had some sort of non-printable characters, those which didn't have them had other obscure characters instead due to which there was no way I could identify the correct one.

I explored the strings for some more time before giving up.

There had virtually been no progress this day, and I was even more confused if I was on the right path.

Since the deadline was fast approaching, I submitted the google form with the other 4 problems, and my incomplete progress on this one.

<span style="color:blue; font-size:25px">Day 3</span>

The ITC deadline was un**expectedly** extended and I had a couple of hours more at this problem.

I made a new git branch and started afresh. At this point, I was no longer trying to find the `key` buried in complied code.

I had a nagging doubt from the start of this problem. Even if I were to find the correct `key`, I would have no idea on decoding the `enc_flag` to get the actual cleartext.

Due to the nature of other problem in this CTF, I assumed that the authors would not give some arbitary encoding scheme for the first encryption, and trying to use the same scheme once again might be a good idea.

However, now I not only didn't have the `key`, but also the `iv` was missing.

I assumed that the `iv` would be either `0` or `1` (as it was in the 2nd encryption). There was still a problem of choosing the `key`, since a bruteforce of $\mathrm{O} (8! \times 8!)$ would practically not work. 

Since I had no workaround to this, the only sensible option was to run the decryption with the same key as before.

```cpp
    rep(i, fact(8)){
        reverseKeys(keys, rkeys);
        decode(arr, decoded1, n, rkeys, 0);

        decode(decoded1, decoded2, n, rkeys, 0);
        vout(keys);
        cout<<" "<<k<<" ";
        vout(decoded2);
        cout<<"\n";

        decode(decoded1, decoded2, n, rkeys, 1);
        vout(keys);
        cout<<" "<<k<<" ";
        vout(decoded2);
        cout<<"\n";

        next_permutation(keys, keys+8);
    }
```

I ran this and searched for `IITB\{[.]+\}` in the output, but there was none.

At this point, I was pretty exhausted from this problem, and was going to sleep, hoping to see the solution later.

But I realised that I had made a misassumption while decoding the `enc_flag` in assuming the values of `iv`. It was not set to the `digitalRead()` anymore, and could actually take any 8-bit value.

With much less hopes, I ran this code again and piped the output.

```cpp
	rep(i, fact(8)){
		reverseKeys(keys, rkeys);
		decode(arr, decoded1, n, rkeys, 0);
		rep(k, 256){
			decode(decoded1, decoded2, n, rkeys, k);
			vout(keys);
			cout<<" "<<k<<" ";
			vout(decoded2);
			cout<<"\n";
		}

		next_permutation(keys, keys+8);
	}
```

On running,

```bash
satyankar@Satyankars-MacBook-Air The_Adventure_of_Fuglanna % cat firstflag.txt | grep -a "IITB{"
36210547 69 IITB{\x41rDuiN0_1$_f0r_Dumm13zZ}
36210745 69 IITB{\x41rDuiN0_1$_f0r_Dumm13zZ}
36510247 69 IITB{\x41rDuiN0_1$_f0r_Dumm13zZ}
36710542 69 IITB{\x41rDuiN0_1$_f0r_Dumm13zZ}
```

surprisingly gives the correct flag. **WOW!**

This was a pretty weak first encryption. 








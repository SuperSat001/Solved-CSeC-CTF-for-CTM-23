# Black Flag
## CSeC{if_you_had_fought_like_a_man_you_need_not_have_been_hang'd_like_a_dog}

On seeing a `.pcap` file, my immediate reaction was to pull up Wireshark.

However, I first tried using `binwalk` on it, just in case I could directly grab some files and voila!

```bash
	satyankar@Satyankars-MacBook-Air Black_Flag % binwalk comm.pcap 

	DECIMAL       HEXADECIMAL     DESCRIPTION
	--------------------------------------------------------------------------------
	0             0x0             Libpcap capture file, little-endian, version 2.4, Ethernet, snaplen: 262144
	368           0x170           JPEG image data, JFIF standard 1.01
	398           0x18E           TIFF image data, little-endian offset of first image directory: 8
	684           0x2AC           JPEG image data, JFIF standard 1.01
```

To extract these files, I just had to use

```bash
	satyankar@Satyankars-MacBook-Air Black_Flag % binwalk --dd='.*' comm.pcap 
```

And then,

```bash
	satyankar@Satyankars-MacBook-Air Black_Flag % cd _comm.pcap.extracted 
	satyankar@Satyankars-MacBook-Air _comm.pcap.extracted % mv 170 170.jpeg        
	satyankar@Satyankars-MacBook-Air _comm.pcap.extracted % open 170.jpeg 
```
![170.jpeg](https://i.imgur.com/ObCjldU.jpeg)  


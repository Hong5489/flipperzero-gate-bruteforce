import math
import os

# Refer from https://github.com/tobiabocchi/flipperzero-bruteforce
def key_bin_str_to_sub(bin_str):
	sub = ""
	line_len = 0  # keep lines under 2500 chars
	for bit in bin_str:
		if line_len > 2500:
			sub += "\nRAW_Data: "
			line_len = 0
		sub += transposition_table[bit]
		line_len += len(transposition_table[bit])
	sub += stop_bit
	return sub

file_header = (
	"Filetype: Flipper SubGhz RAW File\n"
	+ "Version: 1\n"
	+ "Frequency: %s\n"
	+ "Preset: FuriHalSubGhzPresetOok650Async\n"
	+ "Protocol: RAW\n"
)

transposition_table = {
	'0':'150 -650 ',
	'1':'550 -250 '
}

stop_bit = "150 -5600 "


# Generate .sub files for Brute force UNILARM
sub_file = []
lut = [0b00, 0b10, 0b11]
gate1 = 3 << 7
gate2 = 3 << 5
for dip in range(3**8):
	total = 0
	for j in range(8):
		total |= lut[dip % 3] << (2 * j)
		dip //= 3
	total <<= 9
	total |= gate1
	# Play the signal 3 times
	sub_file.append("RAW_Data: " + key_bin_str_to_sub(bin(total)[2:])*3)

# Create directory from 6561 to 9
n_files = 7
splits = [
    int(pow(3, 8) / _) for _ in [pow(3, _) for _ in range(n_files)]
]

for s in splits:
	os.makedirs(f"UNILARM_330/{s}", exist_ok=True)
	os.makedirs(f"UNILARM_433/{s}", exist_ok=True)

for frequency in ["330000000","433920000"]:
	i = 1
	while i != 3**n_files:
		n = 3**8 // i
		for j in range(i):
			open(f"UNILARM_{frequency[:3]}/{n}/{math.floor((j*n)/(n*3))}_{j}.sub",'w').write(file_header%(frequency)+'\n'.join(sub_file[j*n:(j*n)+n]))
		i*=3

# Generate .sub files for Brute force SMC5326

transposition_table = {
	'0':'300 -900 ',
	'1':'900 -300 '
}

stop_bit = "900 -7500 "

sub_file = []
lut = [0b00, 0b10, 0b11]
gate1 = 0b111010101
gate2 = 0b101110101


for dip in range(3**8):
	total = 0
	for j in range(8):
		total |= lut[dip % 3] << (2 * j)
		dip //= 3
	total <<= 9
	total |= gate1
	# Play the signal 5 times
	sub_file.append("RAW_Data: " + key_bin_str_to_sub(bin(total)[2:])*5)

# Create directory from 6561 to 7
for s in splits:
	os.makedirs(f"SMC5326_330/{s}", exist_ok=True)
	os.makedirs(f"SMC5326_433/{s}", exist_ok=True)

for frequency in ["330000000","433920000"]:
	i = 1
	while i != 3**n_files:
		n = 3**8 // i
		for j in range(i):
			open(f"SMC5326_{frequency[:3]}/{n}/{math.floor((j*n)/(n*3))}_{j}.sub",'w').write(file_header%(frequency)+'\n'.join(sub_file[j*n:(j*n)+n]))
		i*=3

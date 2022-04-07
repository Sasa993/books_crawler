from datetime import date

def convert_to_target_format(tmp_date: date) -> str:
	"""
	Convert date into target's date format.
	"31 Mart 2022"
	"""
	return f"{tmp_date.day} {get_month(tmp_date.month)} {tmp_date.year}"

def get_month(x: str) -> int:
	"""
	Custom switch-caes statement for months.
	Since the website that is being crawled uses month names on Serbian,
	this function is necessary.
	The 13th month is named 'danas' which means 'today'.
	"""
	return {
		1: 'Januar',
		2: 'Februar',
		3: 'Mart',
		4: 'April',
		5: 'Maj',
		6: 'Jun',
		7: 'Jul',
		8: 'Avgust',
		9: 'Septembar',
		10: 'Oktobar',
		11: 'Novembar',
		12: 'Decembar',
		13: 'danas'
	}[x]

from datetime import date, datetime


SERBIAN_MONTHS = {
    'Januar': 'January',
    'Februar': 'February',
    'Mart': 'March',
    'April': 'April',
    'Maj': 'May',
    'Jun': 'June',
    'Jul': 'July',
    'Avgust': 'August',
    'Septembar': 'September',
    'Oktobar': 'October',
    'Novembar': 'November',
    'Decembar': 'December'
}


def convert_to_target_format(tmp_date: date) -> str:
    """
    Convert date into target's date format.
    "31 Mart 2022"
    """
    return f"{tmp_date.day:02d} {get_month(tmp_date.month)} {tmp_date.year}"


def get_month(x: str) -> int:
    """
    Custom switch-case statement for months.
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


def parse_serbian_date(date_str: str):
    """
    todo
    """
    for serbian_month, english_month in SERBIAN_MONTHS.items():
        date_str = date_str.replace(serbian_month, english_month)
    return datetime.strptime(date_str, '%d %B %Y')

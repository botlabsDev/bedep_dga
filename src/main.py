# Copyright (c) 2015 Dennis Schwarz <dschwarz@arbor.net>
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
import argparse

from src.bedep_dga import calculate_bedep_domains
from src.common import date_start, date_end, next_thursday

BEDEP_CONFIGS = [
    # AML-18141460
    {
        "value1": 0x9be6851a,
        "value2": 0xd666e1f3,
        "value3": 0x2666ca48,
        "table": "table1.json",
        "max_currencies": 48,
    },
    # AML-19646835
    {
        "value1": 0x36a64c8a,
        "value2": 0x7cd02d69,
        "value3": 0x8cd006d2,
        "table": "table2.json",
        "max_currencies": 48,
    },
    # AML-20382547
    {
        "value1": 0x4cdff15c,
        "value2": 0x1bbae2d4,
        "value3": 0xebbac96f,
        "table": "table3.json",
        "max_currencies": 36,
    },
    # AML-20846035
    {
        "value1": 0x52eb3676,
        "value2": 0x7952538d,
        "value3": 0x89527836,
        "table": "table4.json",
        "max_currencies": 36,
    },
    # AML-27555089 / d2a977fa29acda0a7a272670f0706508
    {
        "value1": 0x8af8b34d,
        "value2": 0x2be8c4b0,
        "value3": 0xdbe8ef0b,
        "table": "table5.json",
        "max_currencies": 36,
    },
    # AML-27580367 / 9aad1b163fa550f7979d822b6f5078c9
    {
        "value1": 0xa28eafd8,
        "value2": 0x2edfdb46,
        "value3": 0xdedff0fd,
        "table": "table6.json",
        "max_currencies": 36,
    },
    # AML-28101739 / 3aa5d612889aeab6295752cdf95b5db0
    {
        "value1": 0xda9ce3f7,
        "value2": 0xd1cecf92,
        "value3": 0x21cee429,
        "table": "table7.json",
        "max_currencies": 36,
    },
]


def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=date_start, default=date_start(),
                        help="start; get domains for timerange; (utc-time)")
    parser.add_argument("--end", type=date_end, default=date_end(),
                        help="end; get domains for timerange; (utc-time)")
    parser.add_argument("--next-week", default=False, action='store_true',
                        help="get domains for comming week. New domains available on wednesday.")
    return parser.parse_args()


def main():
    args = parseArgs()

    start_date = args.start
    end_date = args.end

    if args.next_week:
        start_date = next_thursday()
        end_date = next_thursday()

    domains = calculate_bedep_domains(start_date, end_date, BEDEP_CONFIGS)

    print("seed,valid_from,valid_till,domain")
    for seed, validFrom, validTill, domain in domains:
        print(f"{seed},"
              f"{str(validFrom.isoformat())},"
              f"{str(validTill.isoformat())},"
              f"{domain}")


if __name__ == "__main__":
    main()

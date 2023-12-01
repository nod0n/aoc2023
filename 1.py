#!/usr/bin/env python

from typing import Callable

# naming explanation (name ends with):
# 1 -> only for part 1
# 2a -> variant 1 of part 2
# 2b -> variant 2 of part 2
# none of the above -> generic

type IsDigitFunc = Callable[[str], bool]
type DigitMapping = tuple[tuple[str, str], ...]
type ExtractDigitsFunc = Callable[[str], str]
type SumFileFunc = Callable[[str], int]


def is_digit_() -> IsDigitFunc:
    digits = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}

    def is_digit__(char: str) -> bool:
        return char in digits

    return is_digit__


def extract_digits1(str_: str) -> str:
    """Extract digits (excluding written out digits)"""
    return "".join(filter(is_digit, str_))


def extract_digits2a() -> ExtractDigitsFunc:
    def replace_digits(
        str_: str,
        digit_mapping: DigitMapping = (
            ("one", "o1e"),
            ("two", "t2o"),
            ("three", "t3e"),
            ("four", "4"),
            ("five", "5e"),
            ("six", "6"),
            ("seven", "7n"),
            ("eight", "e8t"),
            ("nine", "n9"),
        ),
    ) -> str:
        """Replace written out digits: "one" -> "1", "two" -> "2", ..."""
        if len(digit_mapping) == 1:
            return str_.lower().replace(*digit_mapping[0])  # fix last digits
        else:
            fixed_str: str = str_.lower().replace(
                *digit_mapping[0]
            )  # fix digits
            next_digit_mapping = digit_mapping[1:]  # shorten digits mapping
            return replace_digits(fixed_str, next_digit_mapping)

    def extract_digits2a_(str_: str) -> str:
        """Return digits (including written out digits)

        with using replacement "one" -> "o1e", "two" -> "t2o", ..."""
        fixed_str: str = replace_digits(str_)
        return "".join(filter(is_digit, fixed_str))

    return extract_digits2a_


def extract_digits2b() -> ExtractDigitsFunc:
    digit_mapping: DigitMapping = (
        ("one", "1"),
        ("two", "2"),
        ("three", "3"),
        ("four", "4"),
        ("five", "5"),
        ("six", "6"),
        ("seven", "7"),
        ("eight", "8"),
        ("nine", "9"),
    )

    def written_out_digit_at_index(str_: str, i: int) -> str | None:
        for digit in digit_mapping:
            if str_.startswith(digit[0], i):  # digit at index?
                return digit[1]

    def digit_at_index_(str_: str, i: int) -> str | None:
        """Return digit at location"""
        if is_digit(str_[i]):
            return str_[i]  # digit at index found
        return written_out_digit_at_index(str_, i)

    def extract_digits2b_(str_: str) -> str:
        """Return digits (including written out digits)

        with checking if each character is the beginning of a digit"""
        return "".join(
            filter(
                lambda x: x is not None,  # drop non-digit
                map(lambda i: digit_at_index_(str_, i), range(len(str_))),
            )
        )

    return extract_digits2b_


def sum_file(extract_digits: ExtractDigitsFunc) -> SumFileFunc:
    def parse_line(str_: str) -> int:
        """Return the first and last digits as number"""
        digits: str = extract_digits(str_)
        if not digits:
            raise ValueError(f"There needs to be at least one digit in str_")
        return int(digits[0] + digits[-1])

    def sum_file_(file: str) -> int:
        """Return the sum of extracted numbers from file"""
        with open(file) as f:
            return sum(map(parse_line, f))

    return sum_file_


is_digit: IsDigitFunc = is_digit_()  # enclosure


# part 1
sum_file1: SumFileFunc = sum_file(extract_digits1)
sum1: int = sum_file1("1a_input")
print(f"sum1: {sum1}")


# part 2 variant 1
sum_file2a: SumFileFunc = sum_file(extract_digits2a())
sum2a: int = sum_file2a("1b_input")
print(f"sum2a: {sum2a}")

# part 2 variant 2
sum_file2b: SumFileFunc = sum_file(extract_digits2b())
sum2b: int = sum_file2b("1b_input")
print(f"sum2b: {sum2b}")

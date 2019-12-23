#!/usr/bin/env python3
"""
Given an input string 'aaabbdddda', write a function such that the output becomes 'a3bbd4a'
Looking at the output, if the count of the character sequence is >= 3, the character is compressed and displayed in the
format "{character}{count}, otherwise it is displayed the number of times it appears - {character * count}
Author: Anthony Fadero
"""


def compress_string(string):
    output = ''
    count = 1
    string_size = len(string)
    for i, j in enumerate(string):
        if i + 1 < string_size:
            if j == string[i + 1]:
                count += 1
            else:
                output += format_char(j, count)
                count = 1
        else:
            output += format_char(j, count)

    return output


def format_char(xter, count):
    output = ''
    if count <= 2:
        a = xter * count
        output += a
    else:
        a = f"{xter}{count}"
        output += a
    return output


if __name__ == "__main__":
    i = "aabbbddddaooowuuurrrzbbf"
    print(compress_string(i))

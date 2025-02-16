import math

import pandas as pd

number = int(input(f'pleaes enter a number: '))
test_list = list(range(0, number))
division = 10
intervals = math.floor(number / division)

selection = int(input(f'please enter a number between 1 - 10: '))

print(intervals)

print(test_list[intervals * (selection - 1):intervals * selection])

# match(selection):
#     case 10:
#         print(test_list[:])
#     case 9:
#         pass
#     case 8:
#         pass
#     case 7:
#         pass
#     case 6:
#         pass
#     case 6:
#         pass
#     case 5:
#         pass
#     case 4:
#         pass
#     case 3:
#         pass
#     case 2:
#         print(test_list[intervals * (selection - 1):intervals * selection])
#     case 1:
#         print(test_list[0:intervals * selection])

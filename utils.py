import logging
from datetime import datetime

def setup_logging():
    log_filename = f"logs/mega_sena_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logging.basicConfig(
        filename=log_filename,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logging.info("Iniciando Mega-Sena Tools")

def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0: return False
    return True

def ends_with_0(n):
    return str(n).endswith("0")

def has_duplicated_digits(n):
    s = str(n)
    return len(s) == 2 and s[0] == s[1]

def even_odd_count(nums):
    evens = sum(1 for x in nums if x % 2 == 0)
    return evens, len(nums) - evens

def count_primes(nums, primes_set):
    return sum(1 for x in nums if x in primes_set)

def count_leq_30(nums):
    return sum(1 for x in nums if x <= 30)

def count_mult_3(nums):
    return sum(1 for x in nums if x % 3 == 0)

def count_fib(nums, fib_set):
    return sum(1 for x in nums if x in fib_set)

def count_ends0(nums):
    return sum(1 for x in nums if ends_with_0(x))

def count_dup_digits(nums):
    return sum(1 for x in nums if has_duplicated_digits(x))

def diff_max_min(nums):
    return max(nums) - min(nums)

def modo_dict(d):
    return max(d.items(), key=lambda kv: kv[1])[0]

def clear_screen():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    input('\n\033[1;90m[ENTER] para voltar ao menu principal…\033[0m')

def le_int(msg, mn, mx):
    while True:
        try:
            v = int(input(f'\033[1;93m{msg}\033[0m'))
            if mn <= v <= mx:
                return v
        except ValueError:
            pass
        print(f'\033[1;91m✖ Digite um inteiro entre {mn} e {mx}.\033[0m') 
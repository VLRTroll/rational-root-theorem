from selenium import webdriver
import sympy
from itertools import product
import re
from time import sleep


class DesmosBot:
    def __init__(self):
        self.__driver__ = webdriver.Chrome(executable_path="./chromedriver.exe")

    def open_graph(self):
        self.__driver__.get("https://www.desmos.com/calculator")

    def close_window(self):
        self.__driver__.close()

    def __get_divisors__(self, n):
        if n in [0, 1]:
            return [n]

        divisors, k = [n, 1], 2

        while k < n / divisors[-1]:
            if not n % k:
                divisors.append(k)
                if k != n / k:
                    divisors.insert(0, n / k)
            k += 1

        return sorted(divisors)

    def __get_possible_roots__(self, cubic_function):
        function_regex = (
            r"^(?:(\d+)\*)?x\*\*3(?:\s[+-]\s(?:\w+\*)?x(?:\*\*2)?)*(?:\s[+-]\s(\d+))?$"
        )
        a, d = re.match(function_regex, cubic_function).groups()

        a_divisors = self.__get_divisors__(int(a or 1))  # get a coef divisors
        d_divisors = self.__get_divisors__(int(d or 0))  # get d coef divisors

        return product(d_divisors, a_divisors)

    def __apply_style__(style):
        pass

    def __insert_function__(self, func_string, style=None):
        func_box = self.__driver__.find_element_by_class_name("dcg-selected")
        textarea = func_box.find_element_by_tag_name("textarea")

        func_box.click()  # activate function field

        if r"\b\b" in func_string:  # if has any power number
            parts = func_string.split(r"\b\b")
            last_part = parts.pop()

            for part in parts:
                textarea.send_keys(part)
                textarea.send_keys("\b\b")

            textarea.send_keys(last_part)  # preserve the last part
        else:
            textarea.send_keys(func_string)

        if style:
            self.__apply_style__(style)

        textarea.send_keys("\n")  # go to the next function box

    def insert_function_and_roots(self, cubic_function):
        self.__insert_function__(cubic_function.replace("**", r"¹\b\b"))

        # Calculate possible cubic function's roots
        possible_roots = self.__get_possible_roots__(cubic_function)

        # For each root, insert the line in the graph
        for numerator, denominator in possible_roots:
            self.__insert_function__(f"x = {numerator}/{denominator}")
            self.__insert_function__(f"x = -{numerator}/{denominator}")

        # Change root styles to black dashed (optional)


if __name__ == "__main__":
    function_regex = (
        r"^(?:(\d+)\*)?x\^3(?:\s*[+-]\s*(?:\w+\*)?x(?:\^2)?)*(?:\s*[+-]\s*(\d+))?$"
    )

    function_string = input("Insert a cubic expression: ") or "x^3-x^2+x-1"

    # check cubic expression format
    while not re.match(function_regex, function_string):
        print("Invalid expression format.")
        print("Try something like this: 2*x^3-x^2+5*x-1\n")

        function_string = input("Insert a cubic expression: ") or "x^3-x^2+x-1"

    cubic_function = str(sympy.sympify(function_string))

    print("\nComputed formula:")
    sympy.pprint(sympy.sympify(function_string))
    input("\nPress enter to continue...")

    bot = DesmosBot()

    bot.open_graph()
    sleep(1)
    bot.insert_function_and_roots(cubic_function)

import click
import time
import os
from colorama import Fore, Style

# Global debug level
debug_level = 0

def custom_pprint(string, array, input_pointer, pointer, output):
    """Prettify the debugging output with colorized pointers in the code and array."""
    os.system('cls' if os.name == 'nt' else 'clear')

    array_str = [str(i) for i in array]
    
    # Highlight the current character in the Brainfuck code
    input_str = (
        Fore.WHITE + string[:input_pointer].strip() +
        Fore.YELLOW + f"{string[input_pointer]}" +
        Fore.WHITE + string[input_pointer + 1:].strip()
    )

    if pointer == 0:
        array_snapshot = (
                Fore.GREEN + f"{array_str[pointer]} " +
            Fore.WHITE + ' '.join(array_str[pointer+1:]).strip()
        ).strip()
    else:
        array_snapshot = (
            (' '.join(array_str[:pointer])).strip() +
            Fore.GREEN + f" {array_str[pointer]} " +
            Fore.WHITE + ' '.join(array_str[pointer+1:]).strip()
        ).strip()

    print(f"Code: {input_str}")
    print(f"Memory: {array_snapshot}")
    print(f"Output: {output}")

def check_brackets(string):
    """Ensure matching brackets in the Brainfuck code."""
    stack = []
    for char in string:
        if char == '[':
            stack.append(char)
        elif char == ']':
            if not stack:
                return False
            stack.pop()
    return len(stack) == 0

def sim_overflow(number):
    """Simulate byte overflow (values wrap around between 0 and 255)."""
    return number % 256

def closest_opening_bracket(string, index):
    """Find the index of the closest unmatched opening bracket."""
    if string[index] != ']':
        return -1
    stack = []
    for i in range(index - 1, -1, -1):
        if string[i] == ']':
            stack.append(']')
        elif string[i] == '[':
            if stack:
                stack.pop()
            else:
                return i
    return -1

def closest_closing_bracket(string, index):
    """Find the index of the closest unmatched closing bracket."""
    if string[index] != '[':
        return -1
    stack = []
    for i in range(index + 1, len(string)):
        if string[i] == '[':
            stack.append('[')
        elif string[i] == ']':
            if not stack:
                return i
            stack.pop()
    return -1

def interpret_brainfuck(code, interval:float):
    """Runs Brainfuck code in the specified mode."""
    input_pointer = 0
    pointer = 0
    array = [0]
    output = ""

    while input_pointer < len(code):
        command = code[input_pointer]

        if command == ">":
            pointer += 1
            if len(array) <= pointer:
                array.append(0)

        elif command == "<":
            pointer = max(0, pointer - 1)

        elif command == "+":
            array[pointer] = sim_overflow(array[pointer] + 1)

        elif command == "-":
            array[pointer] = sim_overflow(array[pointer] - 1)

        elif command == "[":
            if array[pointer] == 0:
                input_pointer = closest_closing_bracket(code, input_pointer)
                if input_pointer == -1:
                    print("Error: Unmatched brackets.")
                    return

        elif command == "]":
            if array[pointer] != 0:
                input_pointer = closest_opening_bracket(code, input_pointer)
                if input_pointer == -1:
                    print("Error: Unmatched brackets.")
                    return

        elif command == ".":
            output += chr(array[pointer])

        if debug_level > 0:
            custom_pprint(code, array, input_pointer, pointer, output)

            if debug_level == 2:
                input("Press Enter to step...")

            time.sleep(interval)

        input_pointer += 1

    return output

@click.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('-d', '--debug', count=True, help='Enable debug mode (-d for auto, -dd for manual).')
@click.option('-i', '--interval', default=0.5, type=float, help='Time interval (in seconds) between each step in debug mode.')
def brainfuck_interpreter(file, debug, interval):
    """Run a Brainfuck interpreter on the given .bf file."""
    global debug_level
    debug_level = debug

    if debug_level > 2:
        print("Doin' "*debug_level + "your mom")
        exit(1)

    with open(file, 'r') as f:
        code = f.read().strip()

    if not check_brackets(code):
        print("Error: Brackets do not match.")
        return

    # Only print output in normal mode
    if debug_level == 0:
        result = interpret_brainfuck(code, 0)
        print(result)

    result = interpret_brainfuck(code, interval)

if __name__ == "__main__":
    brainfuck_interpreter()

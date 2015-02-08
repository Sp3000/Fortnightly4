from blockstructure import BlockStructure

structure = BlockStructure()

def parse_command(line):
    command, *args = line.split()

    try:
        if command == "place":
            x, y, colour = args
            structure.place(int(x), int(y), colour)
            
        elif command in ["remove", "connect", "disconnect",
                       "move", "rotate"]:

            func = getattr(structure, command)
            func(*map(int, args))

        elif command == "count":
            print(structure.count())
        
        elif command == "connected":
            print("ny"[structure.connected(*map(int, args))])

        elif command == "nearest":
            all_nearest = structure.nearest(*map(int, args))

            if all_nearest:
                print(*all_nearest[0])

            else:
                print("none")

        elif command == "colour":
            all_with_colour = structure.colour(*args)

            if all_with_colour:
                print(" ".join("({}, {})".format(int(block.real), int(block.imag))
                               for block in all_with_colour))

            else:
                print("none")

    except Exception:
        print("Error: {}".format(line))

if __name__ == '__main__':
    line = input()

    while line.strip() != "halt":
        parse_command(line)
        line = input()

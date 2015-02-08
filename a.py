with open("test.txt", "w") as outfile:
    for i in range(1000000):
        print("place 0 {} red".format(i), file=outfile)

    print("connected 0 0 0 999999", file=outfile)

    for i in range(1000000):
        print("remove 0 {}".format(i), file=outfile)
    
    print("halt", file=outfile)

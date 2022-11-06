from sys import argv

if (len(argv) == 3):
    line1 = True
    line2 = True
    with open(argv[1]) as file1:
        with open(argv[2]) as file2:
            while line1 and line1 == line2:
                line1 = file1.readline()
                line2 = file2.readline()
            if not line1:
                print('equal')
            else:
                print('error')


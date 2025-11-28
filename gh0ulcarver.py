import binascii
import pathlib
import sys
import os

signatures = [
    {
        "name": "PNG Image",
        "extension": ".png",
        "start": b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A',
        "end": b'\x60\x82',           
    },
    {
        "name": "JPG Image",
        "extension": ".jpg",
        "start": b'\xff\xd8\xff\xe0\x00\x10\x4a\x46',
        "end": b'\xff\xd9',
    },
    {
        "name": "PDF Document",
        "extension": ".pdf",
        "start": b'\x25\x50\x44\x46\x2d\x31\x2e\x37',             
        "end": b'\x46\x0a',              
    },
]

def readHexBlocks():
    firstByte = 8
    lastByte = 2
    fileTypePath = input("Gimme an example file to recover: ")
    with open(fileTypePath, "rb") as f:
        data = f.read()
    
    startByte = bytes(data[:firstByte])
    endByte   = bytes(data[-lastByte:])
    
    extensionType = "." + fileTypePath.split(".")[-1].lower() if "." in fileTypePath else ""
    fileType = extensionType[1:].upper() if extensionType else "Unknown"
    
    def bytes_to_literal(b):
        return "b'" + ''.join(f'\\x{b:02x}' for b in b) + "'"
    
    print(f"\nDetected: {fileType}")
    print(f'        "start": {bytes_to_literal(startByte)}')
    print(f'        "end": {bytes_to_literal(endByte)}')
    print()
    return fileType, extensionType, startByte, endByte   


def selectionMenu():  
    print("Select the filetype you wanna recover:\n")
    for i, signature in enumerate(signatures, 1):
        print(f"{i}. {signature['name']} ({signature['extension']})")
    print("\n" + "═" * 60)

    while True:
        try:
            choice = int(input("\nEnter your selection (1-3): "))
            if 1 <= choice <= len(signatures):
                selected = signatures[choice - 1]
                break
            else:
                print("Please choose a number between 1 and 3!")
        except ValueError:
            print("Only numbers are allowed!")

    return selected["name"], selected["extension"], selected["start"], selected["end"]


def dataRecover(fileType, extensionType, startByte, endByte):

    drivePath = input("Enter the drive or image path to scan: ")
    writePath = input("Enter the output folder (must end with /): ")
    print("\n")
    openDrive = open(drivePath, "rb")
    readSize = 512
    readFile = openDrive.read(readSize)
    offsetLocation = 0
    dataRecoveryMode = False
    recoveryVariable = 0

    while readFile:
        fileFound = readFile.find(startByte)
        if fileFound >= 0:
            dataRecoveryMode = True
            print('=============== Found ' + fileType + ' at location:' + str(hex(fileFound + (readSize * offsetLocation))) + ' ===============')
            openFile = open(writePath + str(recoveryVariable) + extensionType, "wb")
            openFile.write(readFile[fileFound:])

            # Now enter proper recovery mode
            while dataRecoveryMode:
                readFile = openDrive.read(readSize)        # ← MUST read new block
                if not readFile:                           # end of drive
                    openFile.close()
                    dataRecoveryMode = False
                    break

                byteFound = readFile.find(endByte)
                if byteFound >= 0:
                    openFile.write(readFile[:byteFound + len(endByte)])
                    print('=============== Wrote ' + fileType + ' to location: ' + str(recoveryVariable) + extensionType + ' ===============\n')
                    dataRecoveryMode = False
                    recoveryVariable += 1
                    openFile.close()
                    # Important: reposition to after the footer so next search starts clean
                    current_pos = openDrive.tell()
                    openDrive.seek(current_pos - len(readFile) + byteFound + len(endByte))
                else:
                    openFile.write(readFile)

        readFile = openDrive.read(readSize)
        offsetLocation += 1
    openDrive.close()
    print(f"Recovery complete! Found {recoveryVariable} file(s).")


def main():
    if len(sys.argv) == 1 or "--help" in sys.argv:
        print("Usage:")
        print(" python gh0ulcarver.py --select               # interactive menu")
        print(" python gh0ulcarver.py --demo                 # show signature and carve that filetype")
        print(" python gh0ulcarver.py --help                 # show this help")
        print("\nRecommended to run: python gh0ulcarver.py --demo")
        return

    if sys.argv[1] == "--demo":
        fileType, extensionType, startByte, endByte = readHexBlocks()
        dataRecover(fileType, extensionType, startByte, endByte)


    elif sys.argv[1] == "--select":
        fileType, extensionType, startByte, endByte = selectionMenu()
        dataRecover(fileType, extensionType, startByte, endByte)

if __name__ == "__main__":
    main()
from functions import s, change_prices_txt, lb,download_icons_files

download_icons_files()

from order import order
import time

version = "1.0.0"

def main():
    print(f"Welcome to the patent-pending TXAS software.")
    print(f"You are currently on version {version}.\n")
    quit = 0
    while quit != 1:
        while True:
            try:
                selection = s("What would you like to do?\n [1] File an order\n [2] Modify prices file\n [3] Quit")
                slist = [1,2,3]
                if selection not in slist:
                    raise ValueError
                break
            except:
                print("Invalid selection. Please try again.")
                lb()
        match selection:
            case 1:
                #try:
                order()
                #except:
                    #print("Ran into unexpected error.\n")
            case 2:
                try:
                    change_prices_txt()
                except:
                    print("Ran into unexpected error.\n")
            case 3:
                quit = 1
#while True:
    #try:
main()
        #break
    #except:
        #print("Ran into unexpected error. Restarting...\n")

print("Thank you for using TXAS certified software.")
lb()

time.sleep(1)
print("Closing in 3...")
time.sleep(1)
print("Closing in 2...")
time.sleep(1)
print("Closing in 1...")
time.sleep(1)
import os, requests

os_user = os.getlogin()

info_dir = fr"C:\\Users\\{os_user}\\Documents\\_TXAS Program Info"
price_list = fr"C:\\Users\\{os_user}\\Documents\\_TXAS Program Info\\prices.txt"
orders_dir = fr"C:\\Users\\{os_user}\\Documents\\_TXAS Orders"
temp_dir= fr"C:\\Users\\{os_user}\\Documents\\_TXAS Program Info\\temp"

def lb():
    print("")

def download_icon(url: str, directory: str, filename: str = None):
    os.makedirs(directory, exist_ok=True)
    if filename is None:
        filename = url.split("/")[-1].split("?")[0]
    file_path = os.path.join(directory, filename)
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(file_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    return file_path

def download_icon_check(icon_url, filename):
    try:
        f = open(info_dir + fr"\\{filename}")
    except FileNotFoundError:
        download_icon(icon_url, info_dir, filename)

def q(question):
    variable = input(f"{question}\n--> ")
    lb()
    return variable

def s(question):
    while True:
        variable = input(f"{question}\n--> ")
        lb()
        try:
            variable = int(variable)
            return variable    
        except:
            print("Input must be a number. Please try again.\n")

def download_icons_files():
    if not os.path.exists(info_dir):
        os.mkdir(info_dir)
    if not os.path.exists(orders_dir):
        os.mkdir(orders_dir)
    if not os.path.exists(temp_dir):
        os.mkdir(temp_dir)

    try:
        with open(price_list, "r") as f:
            f.read()
    except:
        with open(price_list, "w") as f:
            f.write(f"1,cleaves,190,Cocaine Leaves\n2,cpowder,216,Cocaine Powder\n3,cbags,260,Cocaine Bags")

    icon_url = "https://cdn.discordapp.com/attachments/1456614658416050362/1456672521779941437/TXAS_Program_Icon.ico?ex=695bda80&is=695a8900&hm=3c476807d9eeccae830dcd4c18b9d1bbadbc3813dc591a9a6fb136fabb0f6412&"
    download_icon_check(icon_url, "TXAS Program Icon.ico")

    icon_url = "https://cdn.discordapp.com/attachments/1456614658416050362/1457123922578509824/TXAS_Program_Icon.png?ex=695c2d67&is=695adbe7&hm=b61c957df8b2295d1081d30707ba25996fc16af03bd0dbe1bb0ca3755a415dc1&"
    download_icon_check(icon_url, "TXAS Program Icon.png")

    

def change_prices_txt():
    cptxtcontinue = 0
    while cptxtcontinue != 1:
        selection = s("What do you want to do?\n [1] Add item\n [2] Remove an item\n [3] Modify item info\n [4] View price list\n [5] Go back")
        match selection:
            case 1:
                selection_no = "0"
                item_id = q("Provide the item ID:")
                item_display = q("Provide the display name:")
                item_price = s("Provide the price of the item:")
                l1 = []
                with open(price_list, "r") as f:
                    for line in f:
                        l1.append(line.replace("\n", "").split(","))
                new_item = f"{selection_no},{item_id},{item_price},{item_display}"
                l1.append(new_item.split(","))
                j = 1
                for i in l1:
                    i[0] = j
                    j += 1
                print("Current items on file:")
                print("[Selection] [Item ID] [Price] [Item]")
                for i in l1:
                    print(f" [{i[0]}] {i[1]} {i[2]} {i[3]}")
                with open(price_list, "w") as f:
                    wtf = ""
                    j = 1
                    for i in l1:
                        wtf += f"{i[0]},{i[1]},{i[2]},{i[3]}"
                        if j < len(l1):
                            wtf += "\n"
                        j += 1
                    f.write(wtf)
                print("\nYour item has been added.\n")
            case 2:
                l1 = []
                with open(price_list, "r") as f:
                    for line in f:
                        l1.append(line.replace("\n", "").split(","))
                print("Current items on file:")
                print("[Selection] [Item ID] [Price] [Item]")
                for i in l1:
                    print(f" [{i[0]}] {i[1]} {i[2]} {i[3]}")
                lb()
                selection = s("What item would you like to remove?")
                l1.pop(selection-1)
                j = 1
                for i in l1:
                    i[0] = j
                    j += 1
                print("Current items on file:")
                print("[Selection] [Item ID] [Price] [Item]")
                for i in l1:
                    print(f" [{i[0]}] {i[1]} {i[2]} {i[3]}") 
                with open(price_list, "w") as f:
                    wtf = ""
                    j = 1
                    for i in l1:
                        wtf += f"{i[0]},{i[1]},{i[2]},{i[3]}"
                        if j < len(l1):
                            wtf += "\n"
                        j += 1
                    f.write(wtf)
                print("\nYour item has been removed.\n")
            case 3:
                l1 = []
                with open(price_list, "r") as f:
                    for line in f:
                        l1.append(line.replace("\n", "").split(","))
                print("Current items on file:")
                print("[Selection] [Item]")
                for i in l1:
                    print(f" [{i[0]}] {i[3]}")
                lb()
                selection1 = s("Which item would you like to modify?")
                print("Selected item:")
                print(f" [1] {l1[selection1-1][0]}\n [2] {l1[selection1-1][1]}\n [3] {l1[selection1-1][2]}\n [4] {l1[selection1-1][3]}")
                lb()
                selection2 = s("Which attribute do you want to modify?")
                print("Selected attribute:")
                print(f" [{selection2}] {l1[selection1-1][selection2-1]}")
                lb()
                if selection2 == 3:
                    new_attribute = s("What would you like to change it to?")
                else:
                    new_attribute = q("What would you like to change it to?")
                l1[selection1-1][selection2-1] = new_attribute
                print("New item information:")
                print(f" [1] {l1[selection1-1][0]}\n [2] {l1[selection1-1][1]}\n [3] {l1[selection1-1][2]}\n [4] {l1[selection1-1][3]}")
                with open(price_list, "w") as f:
                    wtf = ""
                    j = 1
                    for i in l1:
                        i[0] = j
                        wtf += f"{i[0]},{i[1]},{i[2]},{i[3]}"
                        if j < len(l1):
                            wtf += "\n"
                        j += 1
                    f.write(wtf)
                print("\nYour item has been modified.\n")
            case 4:
                l1 = []
                with open(price_list, "r") as f:
                    for line in f:
                        l1.append(line.replace("\n", "").split(","))
                print("Current items on file:")
                print("[Selection] [Item ID] [Price] [Item]")
                for i in l1:
                    print(f" [{i[0]}] {i[1]} {i[2]} {i[3]}")
                lb()
            case 5:
                cptxtcontinue = 1
                return None
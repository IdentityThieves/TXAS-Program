from PIL import Image, ImageDraw, ImageFont
import os, random
from datetime import datetime, date, timezone
from barcode import EAN13
from barcode.writer import ImageWriter
from functions import lb, q, s

os_user = os.getlogin()
info_dir = fr"C:\\Users\\{os_user}\\Documents\\_TXAS Program Info"
price_list = fr"C:\\Users\\{os_user}\\Documents\\_TXAS Program Info\\prices.txt"
orders_dir = fr"C:\\Users\\{os_user}\\Documents\\_TXAS Orders"
temp_dir= fr"C:\\Users\\{os_user}\\Documents\\_TXAS Program Info\\temp"

def order_num():
    od = random.choices("1234567890", k=5)
    odstr = ""
    for i in od:
        odstr += f"{i}"
    return odstr

def order():
    name = q("What is the customers name?")
    phone_number = q("What is the customers phone number?")
    l2 = []
    item_price_list = []
    item_count_list = []
    discount_total = []
    already_ordered_items = []
    continueordering = 0
    total_price = 0
    total_price_wd = 0
    while continueordering != 1:
        while True:
            try:
                l1 = []
                with open(price_list, "r") as f:
                    for line in f:
                        l1.append(line.replace("\n", "").split(","))
                print("Current items on file:")
                print("[Selection] [Item] [Price]")
                for i in l1:
                    print(f" [{i[0]}] {i[3]} {i[2]}")
                lb()
                order_item = s("What does the customer want to order?")
                try:
                    selected_product = f"{l1[order_item-1][3]}"
                    break
                except IndexError:
                    print("Item does not exist.\n")
            except:
                print("Invalid selection. Please try again.")
                lb()
        order_count = s("How many do you want to order?")
        discount = 1
        if selected_product not in already_ordered_items:
            already_ordered_items.append(selected_product)
            if order_count >= 1000:
                discount = 0.95
            if order_count < 1000:
                discount = 1
        
        discount_total.append(discount)
        order = f"{selected_product},{order_count}"
        l2.append(order.split(","))
        price_for_item = f"{l1[order_item-1][2]}"
        total_price += int(price_for_item) * order_count
        ipl_item = int(price_for_item) * order_count
        ipl_item = round(ipl_item)
        ipl_item = f"{ipl_item:,}".replace(",", " ")
        item_price_list.append(f"{ipl_item}")
        item_count_list.append(order_count)

        while True:
            continueq = q("Do you want to add to the order?")
            if continueq.lower() == "yes":
                break
            elif continueq.lower() == "no":
                continueordering = 1
                break
            else:
                print("Invalid response.")

    order = ""
    j = 0
    for i in l2:
        order += f"{i[0]},"
        j += 1
    order_list_final = order.split(",")
    order_list_final.pop()
    order_number = order_num()
    todays_date = date.today()
    utc_time = datetime.now(timezone.utc).strftime("%H:%M:%S UTC")
    order_file_dir = fr"C:\\Users\\{os_user}\\Documents\\_TXAS Orders\\TXAS_order_{order_number}.png"

    lolf = []
    licl = []
    lipl = []
    dup = []

    k = 0
    for i in order_list_final:
        if i in lolf:
            dup.append([i, item_count_list[k], int(item_price_list[k].replace(" ", ""))])
        if i not in lolf:
            lolf.append(i)
            licl.append(item_count_list[k])
            lipl.append(int(item_price_list[k].replace(" ", "")))
        k += 1
    k=0
    for i in dup:
        for j in lolf:
            if i[0] == j:
                licl[k] = licl[k] + i[1]
                lipl[k] = lipl[k] + i[2]
        k += 1

    order_list_final = lolf
    item_count_list = licl
    item_price_list = lipl
    item_price_list_str = []
    for i in item_price_list:
        item_price_list_str.append(f"{round(i):,}".replace(",", " "))
    item_price_list = item_price_list_str

    discount = 1
    for i in discount_total:
        discount = discount * i
    
    total_price_wd = total_price * discount
    discount_price = total_price - total_price_wd

    total_price = f"{round(total_price):,}".replace(",", " ")
    total_price_wd = f"{round(total_price_wd):,}".replace(",", " ")
    discount_price = f"{round(discount_price):,}".replace(",", " ")

    # Receipt dimensions
    width = 400
    height = 300  # Increased height to accommodate multi-line orders comfortably
    background_color = (255, 255, 255)
    text_color = (0, 0, 0)

    # Create image
    img = Image.new('RGB', (width, height), color=background_color)
    draw = ImageDraw.Draw(img)

    def draw_right_aligned(text, y, font, fill=(0,0,0)):
        # Get the bounding box of the text
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        
        # Calculate x position: receipt width - right_margin - text_width
        x = width - right_margin - text_width
        
        draw.text((x, y), text, fill=fill, font=font)

    def centered_text(text, font):
        bbox = draw.textbbox((0, 0), text, font)
        text_width = bbox[2] - bbox[0]
        draw.text((width//2 - text_width//2, y), text, fill=text_color, font=font)

    #logo path
    logo_path = r"C:\Users\m1inty\Documents\_TXAS Program Info\TXAS Program Icon.png"
    bardcode_path = r"C:\Users\m1inty\Documents\_TXAS Program Info\Barcode.png"

    # Fonts - small and receipt-like
    try:
        font_body  = ImageFont.truetype("consola.ttf", 12)     # Main text
        font_bbody = ImageFont.truetype("consolab.ttf", 12)     # Footer
        font_bsmall = ImageFont.truetype("consolab.ttf", 10)     # Footer
    except IOError:
        font_body = ImageFont.load_default()
        font_bbody  = ImageFont.load_default()
        font_bsmall = ImageFont.load_default()

    # Layout
    margin = 30
    right_margin = 30
    y = 34

    # Title
    logo_max_width = 150
    logo_max_height = 100
    barcode_max_width = 256
    business_id = 4112022

    barcode_class = EAN13
    writer = ImageWriter()
    writer.font_path = "consola.ttf"
    ean13 = EAN13(f"{business_id}{order_number}", writer=writer)
    options = {
        "module_height": 25.0,    # Bar height
        "module_width": 0.4,      # Bar thickness
        "quiet_zone": 5,        # Side margins
        "font_size": 5,          # Size of number text below bars
        "text_distance": 2.0,     # Distance between bars and text
        "background": "white",
        "foreground": "black",
        "write_text": True,       # Show the 13-digit number below (recommended for EAN-13)
    }

    temp_barcode_path = os.path.join(temp_dir, f"temp_barcode_{order_number}.png")
    ean13.save(temp_barcode_path[:-4], options)

    logo = Image.open(logo_path).convert("RGBA")  # Support transparency
    barcode = Image.open(temp_barcode_path).convert("RGBA")

    # Calculate new size while preserving aspect ratio
    logo.thumbnail((logo_max_width, logo_max_height or logo.height), Image.LANCZOS)
    logo_width, logo_height = logo.size
    
    barcode.thumbnail((barcode_max_width, barcode.height), Image.LANCZOS)
    barcode_width, barcode_height = barcode.size

    quantity_x = margin
    y += 637

    j = 0
    for i in order_list_final:
        if j < len(order_list_final):
            y += 24  # Line spacing for items
        j += 1

    bottom_margin = 207
    content_bottom = y
    required_height = content_bottom + bottom_margin
    if required_height > height:
        # Create new taller image
        new_height = required_height
        new_img = Image.new('RGB', (width, new_height), color=(255, 255, 255))
        new_draw = ImageDraw.Draw(new_img)
        draw = new_draw

        # Replace old image with new one
        img = new_img
        height = new_height  # Update height variable if needed later

        y = 34

        logo_x = (width - 150) // 2
        img.paste(logo, (logo_x, y), logo)  # Use logo itself as mask for transparency
        y += 75
        draw.text((width//2, y), f"Subsidiary of The Camelos", fill=text_color, font=font_bsmall, anchor="mm")
        y += 32

        centered_text("Tax Accountants LLP", font_bbody)
        y += 24

        centered_text("111 Meteor Street", font_bbody)
        y += 24

        centered_text("7098 Los Santos", font_bbody)
        y += 24

        centered_text(f"Business ID: {business_id}", font_bbody)
        y += 28

        draw.text((width//2, y), f"-------------------------------------------------", fill=text_color, font=font_body, anchor="mm")
        y += 16

        draw.text((margin, y), f"{todays_date}", fill=text_color, font=font_bbody)
        draw_right_aligned(f"{utc_time}", y, font=font_bbody)
        y += 28

        draw.text((width//2, y), f"-------------------------------------------------", fill=text_color, font=font_body, anchor="mm")
        y += 16

        # Customer info
        bbox = draw.textbbox((0, 0), "PHONE NUMBER:", font_bbody)
        text_width_1 = bbox[2] - bbox[0]
        bbox = draw.textbbox((0, 0), "NAME", font_bbody)
        text_width_2 = bbox[2] - bbox[0]
        draw.text((margin + text_width_1, y), f"NAME:", fill=text_color, font=font_bbody, anchor="rt")
        draw.text((margin + text_width_1 + 10, y), f"{name}", fill=text_color, font=font_body)
        y += 24

        draw.text((margin, y), f"PHONE NUMBER:", fill=text_color, font=font_bbody)
        draw.text((margin + text_width_1 + 10, y), f"{phone_number}", fill=text_color, font=font_body)
        y += 24

        draw.text((margin, y), f"ORDER NUMBER:", fill=text_color, font=font_bbody)
        draw.text((margin + text_width_1 + 10, y), f"{order_number}", fill=text_color, font=font_body)
        y += 28

        draw.text((width//2, y), f"-------------------------------------------------", fill=text_color, font=font_body, anchor="mm")
        y += 16

        draw.text((margin, y), "PRODUCT", fill=text_color, font=font_bbody)
        centered_text("ITEM COUNT", font_bbody)
        draw_right_aligned("PRICE", y, font=font_bbody)
        y += 28

        draw.text((width//2, y), f"-------------------------------------------------", fill=text_color, font=font_body, anchor="mm")
        y += 16

        # Order items - aligned columns
        quantity_x = margin

        j = 0
        for i in order_list_final:
            draw.text((quantity_x, y), i, fill=text_color, font=font_body)
            draw_right_aligned(f"{item_price_list[j]}", y, font=font_body)
            centered_text(f"{item_count_list[j]}", font_body)
            if j < len(order_list_final):
                y += 24  # Line spacing for items
            j += 1
        
        y += 24

        # Total Price
        draw.text((margin + 50, y), f"PRICE:", fill=text_color, font=font_bbody)
        draw_right_aligned(f"{total_price}", y, font=font_body)
        y += 24

        draw.text((margin + 50, y), f"TAXES:", fill=text_color, font=font_bbody)
        draw_right_aligned(f"-{discount_price}", y, font=font_body)
        y += 24

        draw.text((margin + 50, y), f"TOTAL:", fill=text_color, font=font_bbody)
        draw_right_aligned(f"{total_price_wd}", y, font=font_bbody)
        y += 28

        draw.text((width//2, y), f"-------------------------------------------------", fill=text_color, font=font_body, anchor="mm")
        y += 4

        draw.text((width//2, y), f"-------------------------------------------------", fill=text_color, font=font_body, anchor="mm")
        y += 48
        
        centered_text("THANK YOU FOR YOUR ORDER", font_bbody)
        y += 24

        centered_text("HAVE A NICE DAY", font_bbody)

        img.paste(barcode, (width//2 - barcode_width//2, height-202), barcode)

        img = new_img
    # Save
    os.remove(temp_barcode_path)
    img.save(order_file_dir)

    # Console output
    print("Order has been successfully filed.")
    print(f"You can find the order at {order_file_dir}\n")

#order()
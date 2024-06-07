
#   Generate this hex from this website   
#   https://xantorohara.github.io/led-matrix-editor/


hex = "4122140808080800"

# clockwise/right rotation phases
hex_rotate = [
    "003c20203c04043c",
    "00009e9292f20000",
    "3c20203c04043c00",
    "00004f4949790000"
]

def write_txt(filename, text):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(text)

def get_rev_bin(hex):
    b = bin(int(hex[:2],16))[2:]

    while(len(b) < 8):
        b = "0" + b 
    
    r = ""
    for c in b:
        if(c == '0'):
            r += '1'
        else:
            r += '0'
    
    return "0b" + r

def get_row_activations(hex):
    hex = hex[::-1]

    bins = []

    for i in range(0,16,2):
        h = hex[i+1] + hex[i]
        # print(h)
        bins.append(get_rev_bin(h))

    s = "{ "

    for i in range(8):
        s += bins[i]
        if(i != 7):
            s += ", "
    
    s += " }"
    return s

def get_static_code(hex):
    s = "volatile unsigned char image[8] \n = "
    s += get_row_activations(hex)
    s += "; "
    s += "\n"
    return s

def get_right_rotation_code(hex_rotate):
    s = "volatile unsigned char image_rotate[4][8] \n = {\n      "
    for i in range(4):
        s += get_row_activations(hex_rotate[i])
        if(i != 3):
            s += ",\n      "
    s += "\n  }; \n"
    return s 


# print("\n\n\n")
# print(get_static_code(hex))
# print(get_right_rotation_code(hex_rotate))
# print("\n")

output = get_static_code(hex) + "\n\n" + get_right_rotation_code(hex_rotate)

write_txt("output.txt", output)

print("\nOutput written to file\n")

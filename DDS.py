import crcmod
import serial
import time


# test_comand = 0x020011ff06000000000000
# test_comand = "12345678"
test_comand = "020011ff06000000000000"
# g16 = 0x1021
start_byte = "7e"
stop_byte = "7f"
# hex_comand = 0x3232
get_addr = "00004fff00"
inq_addr = "11ff00"


def calculate_crc(data):
    print("Вычисляю ...")
    crc_func = crcmod.mkCrcFun(0x11021, rev=False, initCrc=0x0000, xorOut=0x0000)
    print(f'Сообщение - {data}')
    calculated_crc = crc_func(bytes.fromhex(data))
    modified_crc = hex(calculated_crc)[4:] + hex(calculated_crc)[2:4]
    final_request = start_byte + data + hex(calculated_crc)[4:] + hex(calculated_crc)[2:4] + stop_byte
    hex_str = hex(int(final_request, 16))
    print(f'CRC - {hex(calculated_crc)}')
    print(f'CRC modified - {modified_crc}')
    print(f'Final Request - {final_request}')
    print(f'Final HEX Request - {hex_str}')
    return hex_str


def get_address_query():
    f_str = calculate_crc(get_addr)
    print(f_str)
    return f_str


def get_par_query(n_module):
    if is_hex_str(n_module) and 0 <= int(n_module, 16) <= 65535:
        mod_n_hex = hex(int(n_module, 16))[2:].zfill(4)
        gen_str = mod_n_hex[2:] + mod_n_hex[:2] + inq_addr
        print(gen_str)
        final_str = calculate_crc(gen_str)
        print(final_str)
        return final_str
    else:
        return False


def get_con():
    try:
        ser = serial.Serial('/dev/ttyUSB0', 115200)
        print(ser.name)
        return ser
    except serial.SerialException as e:
        print(e)
        return False


def close_con(c):
    try:
        c.close()
        return True
    except serial.SerialException as e:
        print(e)
        return False


def send_query(connection, q):
    out = ''
    try:
        connection.write(bytes.fromhex(q[2:]))
        print(f'Отправляю {q}')
        time.sleep(1)
        while connection.in_waiting > 0:
            out += connection.read(1).hex()
        print(out)
    except serial.SerialException as e:
        print(e)
    return out


def is_int_str(s):
    if s.isdigit():
        try:
            int(s)
            return True
        except ValueError:
            return False
    else:
        return False


def is_hex_str(s):
    try:
        int(s, 16)
        return True
    except ValueError:
        return False

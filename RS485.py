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


def send_query(query):
    out = ''
    try:
        ser = serial.Serial('/dev/ttyUSB0', 115200)
        print(ser.name)
        ser.write(bytes.fromhex(query[2:]))
        print(f'Send {query}')
        time.sleep(1)
        while ser.in_waiting > 0:
            out += ser.read(1).hex()
        print(out)
        ser.close()
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


def main():
    module_number = ""
    while True:
        # gen_str = ""
        print(f'-------------Номер модуля:-----')
        print(f'-------------{module_number}----------------')
        print('1: Запросить номер модуля (0x4f)')
        print('2: Запросить статус модуля (0x11)')
        print('3: Запросить параметры модуля (0x12)')
        print('4: Установить параметры модуля (0x13)')
        print('5: Запросить пороговые параметры (0x50)')
        print('6: Установить пороговые параметры (0x51)')
        print('0: Выход')
        command = input('Введите команду: ')
        if command == '1':
            query_module_number = get_address_query()
            # print(query_module_number)
            response = send_query(query_module_number)
            print(response)
            module_number = response[-8:-6]
            print(module_number)
        elif command == '2':
            while True:
                # module_number = get_address()
                if module_number:
                    if is_hex_str(module_number) and 0 <= int(module_number, 16) <= 65535:
                        mod_n_hex = hex(int(module_number, 16))[2:].zfill(4)
                        gen_str = mod_n_hex[2:] + mod_n_hex[:2] + inq_addr
                        print(gen_str)
                        final_str = calculate_crc(gen_str)
                        print(final_str)
                        send_query(final_str)
                        break
                    else:
                        continue
        elif command == '0':
            break
        else:
            print('-----------------------------')
            print('Введите правильную цифру')
            # print('-----------------------------')
            continue


if __name__ == "__main__":
    main()

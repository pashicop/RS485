import time
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText
# from ttkbootstrap.tableview import Tableview
from PIL import Image, ImageTk
import DDS
import socket


# noinspection PyTypeChecker
class Kappa(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=BOTH, expand=YES)
        image_path = "gr.png"
        pil_image = Image.open(image_path).resize((16, 16))
        self.img_green = ImageTk.PhotoImage(pil_image)
        image_path = "red.png"
        pil_image = Image.open(image_path).resize((16, 16))
        self.img_red = ImageTk.PhotoImage(pil_image)
        image_path = "gray.png"
        pil_image = Image.open(image_path).resize((16, 16))
        self.img_gray = ImageTk.PhotoImage(pil_image)
        self.type_var = ttk.StringVar(value='ip')
        self.ip = ttk.StringVar(value='10.1.4.157')
        self.auto = False

        header = ttk.Frame(self)
        header.pack(side=TOP, fill=BOTH, expand=YES)

        self.con_frame = ttk.LabelFrame(header, text="Тип подключения")
        self.con_frame.pack(side=LEFT, anchor=NW, padx=15, pady=15)

        con_ip = ttk.Frame(master=self.con_frame)
        con_ip.pack(fill=BOTH, expand=YES, pady=0, ipady=0)
        opt_rb_ip = ttk.Radiobutton(con_ip,
                                    text='IP',
                                    command=self.on_type_selection,
                                    variable=self.type_var,
                                    value='ip')
        opt_rb_ip.pack(side=LEFT, padx=30, pady=(0, 5))

        self.opt_ip_inp = ttk.Entry(con_ip, textvariable=self.ip)
        self.opt_ip_inp.pack(side=LEFT, padx=30, pady=(0, 5))

        con_com = ttk.Frame(self.con_frame)
        con_com.pack(fill=BOTH, expand=YES)
        opt_rb_com = ttk.Radiobutton(con_com,
                                     text='COM',
                                     command=self.on_type_selection,
                                     variable=self.type_var,
                                     value='com')
        opt_rb_com.pack(fill=BOTH, side=LEFT, expand=YES, padx=30, pady=(0, 5))

        con_btn = ttk.Frame(self.con_frame)
        con_btn.pack(fill=BOTH, expand=YES)
        global btn_discon, btn_con
        btn_con = ttk.Button(master=con_btn, text="Подключить", command=self.on_connect)
        btn_con.pack(side=LEFT, padx=(30, 15), pady=15)
        btn_discon = ttk.Button(master=con_btn, text="Отключить", command=self.on_disconnect, state=DISABLED)
        btn_discon.pack(side=LEFT, padx=(0, 15), pady=15)

        self.setvar('con_st', 'Нет подключения')
        txt = ttk.Label(master=self.con_frame, textvariable='con_st')
        txt.pack(fill=BOTH, expand=YES, padx=30, pady=(0, 15))

        self.option_lf_mod = ttk.LabelFrame(header, text="Параметры модуля")
        self.option_lf_mod.pack(fill=Y, anchor=NW, padx=15, pady=15)

        container = ttk.Frame(self.option_lf_mod)
        container.pack(fill=BOTH, expand=YES)
        global btn_get_par, btn_set_par, btn_set_par_test1, btn_set_par_test2
        btn_get_par = ttk.Button(master=container, text="Получить", command=self.get_par, state=DISABLED)
        btn_get_par.pack(side=LEFT, padx=15, pady=15)
        btn_set_par = ttk.Button(master=container, text="Загрузить", command=self.set_par, state=DISABLED)
        btn_set_par.pack(side=LEFT, padx=15, pady=15)
        container2 = ttk.Frame(self.option_lf_mod)
        container2.pack(fill=BOTH, expand=YES)
        btn_set_par_test1 = ttk.Button(master=container2, text="Тест 1", command=lambda: self.set_par_test(True),
                                       state=DISABLED)
        btn_set_par_test1.pack(side=LEFT, padx=15, pady=15)
        btn_set_par_test2 = ttk.Button(master=container2, text="Тест 2", command=lambda: self.set_par_test(False),
                                       state=DISABLED)
        btn_set_par_test2.pack(side=LEFT, padx=15, pady=15)
        container3 = ttk.Frame(self.option_lf_mod)
        container3.pack(fill=BOTH, expand=YES)
        ttk.Label(container3, text='Авт. опрос (1 сек)').pack(side=LEFT, padx=15, pady=15)
        self.btn_auto = ttk.Button(master=container3, text="Включить", style=SUCCESS, command=self.set_auto, state=NORMAL)
        self.btn_auto.pack(side=LEFT, padx=15, pady=15)
        btn_set_par_test2.pack(side=LEFT, padx=15, pady=15)
        self.var_lf = {}
        col = ttk.Frame(self)
        col.pack(side=TOP, fill=BOTH, expand=YES)
        for i in range(4):
            # var_name = f'mod{i + 1}'
            mod_name = ttk.LabelFrame(col, text=i + 1)
            mod_name.pack(side=LEFT, fill=X, expand=YES, padx=15, pady=(0, 15))
            self.make_device(i, mod_name)
            # for child in mod_name.winfo_children():
            #     # self.set_state_frame(child, DISABLED)
            #     child.state(['disabled'])
        log_bar = ttk.Frame(self, relief=SUNKEN)
        log_bar.pack(side=BOTTOM, fill=BOTH, expand=YES)
        self.option_lf_logs = ttk.LabelFrame(log_bar, text="Лог")
        self.option_lf_logs.pack(fill=BOTH, expand=YES, pady=15, padx=15)
        self.create_log_bar()

    def make_device(self, i, m_name):
        fr_par_num = ttk.Frame(m_name)
        fr_par_num.pack(fill=X)
        # номер модуля
        mod_num = ttk.Label(fr_par_num, text='Номер модуля:')
        mod_num.pack(side=LEFT, anchor=N, padx=15, pady=(15, 5))

        var_num_name = f'var_num_{i + 1}'
        var_num = ttk.Label(fr_par_num, textvariable=var_num_name)
        var_num.pack(side=LEFT, anchor=N, fill=X, pady=(15, 5))
        self.setvar(var_num_name, '-')
        # Диапазон частот
        fr_freqs = ttk.Frame(m_name)
        fr_freqs.pack(fill=X)

        lbl_freqs = ttk.Label(fr_freqs, text='Частоты:')
        lbl_freqs.pack(side=LEFT, anchor=E, padx=15, pady=(0, 5))

        var_freq_min_name = f'var_freq_min_{i + 1}'
        var_freq_min = ttk.Entry(fr_freqs, textvariable=var_freq_min_name, width=4, state=DISABLED)
        var_freq_min.pack(side=LEFT, anchor=N, fill=X)
        self.setvar(var_freq_min_name, '-')

        lbl_freqs = ttk.Label(fr_freqs, text='—')
        lbl_freqs.pack(side=LEFT, anchor=E, padx=5, pady=(0, 5))

        var_freq_max_name = f'var_freq_max_{i + 1}'
        var_freq_max = ttk.Entry(fr_freqs, textvariable=var_freq_max_name, width=4, state=DISABLED)
        var_freq_max.pack(side=LEFT, anchor=N, fill=X, pady=(0, 5), padx=(0, 15))
        self.setvar(var_freq_max_name, '-')
        # Мощность
        fr_par_rf = ttk.Frame(m_name)
        fr_par_rf.pack(fill=X)

        lbl_rf_out = ttk.Label(fr_par_rf, text='Мощность RF:')
        lbl_rf_out.pack(side=LEFT, anchor=N, padx=15, pady=(0, 5))

        var_rf_name = f'var_rf_{i + 1}'
        var_rf_out = ttk.Label(fr_par_rf, textvariable=var_rf_name)
        var_rf_out.pack(side=LEFT, anchor=N, fill=X, pady=(0, 5), padx=(0, 15))
        self.setvar(var_rf_name, '-')

        alarm_rf_name = f'alarm_rf_{i + 1}'
        self.var_lf[alarm_rf_name] = ttk.Label(fr_par_rf, image=self.img_gray)
        self.var_lf[alarm_rf_name].pack(side=RIGHT, anchor=N, fill=X, padx=(20, 40))
        # Температура
        fr_par_tmp = ttk.Frame(m_name)
        fr_par_tmp.pack(fill=X)

        lbl_tmp = ttk.Label(fr_par_tmp, text='Температура:')
        lbl_tmp.pack(side=LEFT, anchor=N, padx=15, pady=(0, 5))

        var_tmp_name = f'var_tmp_{i + 1}'
        var_tmp = ttk.Label(fr_par_tmp, textvariable=var_tmp_name)
        var_tmp.pack(side=LEFT, anchor=N, fill=X, pady=(0, 5), padx=(0, 15))
        self.setvar(var_tmp_name, '-')

        alarm_tmp_name = f'alarm_tmp_{i + 1}'
        self.var_lf[alarm_tmp_name] = ttk.Label(fr_par_tmp, image=self.img_gray)
        self.var_lf[alarm_tmp_name].pack(side=RIGHT, anchor=N, fill=X, padx=(20, 40))
        # Напряжение
        fr_par_vol = ttk.Frame(m_name)
        fr_par_vol.pack(fill=X)

        lbl_vol = ttk.Label(fr_par_vol, text='Напряжение:')
        lbl_vol.pack(side=LEFT, anchor=N, padx=15, pady=(0, 5))

        var_vol_name = f'var_vol_{i + 1}'
        var_vol = ttk.Label(fr_par_vol, textvariable=var_vol_name)
        var_vol.pack(side=LEFT, anchor=N, fill=X, pady=(0, 5))
        self.setvar(var_vol_name, '-')

        alarm_vol_name = f'alarm_vol_{i + 1}'
        self.var_lf[alarm_vol_name] = ttk.Label(fr_par_vol, image=self.img_gray)
        self.var_lf[alarm_vol_name].pack(side=RIGHT, anchor=N, fill=X, padx=(20, 40))
        # Потребление тока
        fr_par_cur = ttk.Frame(m_name)
        fr_par_cur.pack(fill=X)

        lbl_cur = ttk.Label(fr_par_cur, text='Потребление:')
        lbl_cur.pack(side=LEFT, anchor=N, padx=15, pady=(0, 5))

        var_cur_name = f'var_cur_{i + 1}'
        var_cur = ttk.Label(fr_par_cur, textvariable=var_cur_name)
        var_cur.pack(side=LEFT, anchor=N, fill=X, pady=(0, 5))
        self.setvar(var_cur_name, '-')

        alarm_cur_name = f'alarm_cur_{i + 1}'
        self.var_lf[alarm_cur_name] = ttk.Label(fr_par_cur, image=self.img_gray)
        self.var_lf[alarm_cur_name].pack(side=RIGHT, anchor=N, fill=X, padx=(20, 40))
        # КСВ
        fr_par_vswr = ttk.Frame(m_name)
        fr_par_vswr.pack(fill=X)

        lbl_vswr = ttk.Label(fr_par_vswr, text='КСВ:')
        lbl_vswr.pack(side=LEFT, anchor=N, padx=15, pady=(0, 5))

        var_vswr_name = f'var_vswr_{i + 1}'
        var_vswr = ttk.Label(fr_par_vswr, textvariable=var_vswr_name)
        var_vswr.pack(side=LEFT, anchor=N, fill=X, pady=(0, 5))
        self.setvar(var_vswr_name, '-')

        alarm_vswr_name = f'alarm_vswr_{i + 1}'
        self.var_lf[alarm_vswr_name] = ttk.Label(fr_par_vswr, image=self.img_gray)
        self.var_lf[alarm_vswr_name].pack(side=RIGHT, anchor=N, fill=X, padx=(20, 40))
        # Модуль установки RF
        power_fr = ttk.Frame(m_name)
        power_fr.pack(fill=X)
        lbl_rf_pow = ttk.Label(power_fr, text='Мощность')
        lbl_rf_pow.pack(side=LEFT, anchor=E, padx=15, pady=(0, 5))
        # Задать мощность
        rf_power_name = f'rf_power_{i + 1}'
        self.setvar(rf_power_name, '')
        rf_power = ttk.Entry(master=power_fr, textvariable=rf_power_name, width=2)
        rf_power.pack(side=LEFT, anchor=N, padx=(15, 5), pady=(10, 15))
        # rf_power.config(state=DISABLED)
        # rf_power.state(['disabled'])
        lbl_rf_pow = ttk.Label(power_fr, text='дБм')
        lbl_rf_pow.pack(side=LEFT, anchor=E, padx=15, pady=(0, 5))
        # Кнопка
        rf_switch_name = f'rf_switch_{i + 1}'
        self.setvar(rf_switch_name, 0)
        rf_sw = ttk.Checkbutton(master=power_fr,
                                # text='',
                                bootstyle='danger-round-toggle',
                                variable=rf_switch_name)
        rf_sw.pack(side=RIGHT, anchor=W, padx=(15, 35))
        # rf_sw.state(['disabled'])

    def create_log_bar(self):
        global logs_box
        logs_box = ScrolledText(master=self.option_lf_logs, height=10, hbar=True)
        logs_box.pack(fill=X, expand=YES, padx=15, pady=15)
        logs_box.insert(END, 'Программа готова к работе\n')


    def on_type_selection(self):
        print(self.type_var.get())
        print(self.ip.get())
        if self.type_var.get() == 'com':
            self.opt_ip_inp['state'] = DISABLED
        else:
            self.opt_ip_inp['state'] = NORMAL

    def on_connect(self):
        global sock
        sock = False
        mode = self.type_var.get()
        if mode == 'com':
            global con
            con = DDS.get_con()
            if con:
                l_text = 'ПОДКЛЮЧЕНО к ' + con.name
                self.setvar('con_st', l_text)
                logs_box.insert(END, l_text + '\n')
                btn_discon['state'] = NORMAL
                btn_con['state'] = DISABLED
                # btn_get_addr['state'] = NORMAL
            else:
                self.setvar('con_st', 'Ошибка! Попробуйте ещё раз!')
                logs_box.insert(END, "Ошибка подключения\n")
        elif mode == 'ip':
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                sock.connect((self.ip.get(), 5000))
                print(f'Подключен к {self.ip.get()}:5000')
                logs_box.insert(END, f'Подключен к {self.ip.get()}:5000\n')
                logs_box.see(END)
                l_text = 'ПОДКЛЮЧЕНО к ' + self.ip.get() + ':5000'
                self.setvar('con_st', l_text)
                btn_discon['state'] = NORMAL
                btn_set_par['state'] = NORMAL
                btn_set_par_test1['state'] = NORMAL
                btn_set_par_test2['state'] = NORMAL
                self.get_mod_address(self.type_var.get())
            except Exception as e:
                print(e)
        else:
            print('Неверный тип подключения!')

    def on_disconnect(self):
        mode = self.type_var.get()
        if mode == 'com':
            is_closed = DDS.close_con(con)
            if is_closed:
                self.setvar('con_st', 'ОТКЛЮЧЕНО')
                btn_con['state'] = NORMAL
                btn_discon['state'] = DISABLED
                # btn_get_addr['state'] = DISABLED
                btn_get_par['state'] = DISABLED
                btn_set_par['state'] = DISABLED
                logs_box.insert(END, "ОТКЛЮЧЕНО\n")
            else:
                self.setvar('con_st', 'ОШИБКА ОТКЛЮЧЕНИЯ')
                logs_box.insert(END, "ОШИБКА ОТКЛЮЧЕНИЯ\n")
        elif mode == 'ip':
            if 'sock' in globals() and sock:
                sock.close()
                print('Соединение отключено')
                logs_box.insert(END, 'Соединение отключено\n')
                logs_box.insert(END, '=========================================================\n')
                logs_box.see(END)
                l_text = 'Соединение отключено'
                self.setvar('con_st', l_text)
        else:
            print('Не получилось отключить')

    def get_mod_address(self, mode):
        if mode == 'com':
            query = DDS.get_address_query()
            # logs_box.insert(END, "Запрос" + query + "\n")
            logs_box.insert(END, "Запрос " + ' '.join(query[i:i+2] for i in range(0, len(query), 2)) + "\n")
            response = DDS.send_query(con, query)
            if response:
                global module_number
                module_number = response[-8:-6]
                mod_n_text = 'Номер модуля - 0x' + module_number + ', ' + str(int(module_number, 16))
                self.setvar('mod_addr', mod_n_text)
                logs_box.insert(END, "Ответ " + ' '.join(response[i:i+2] for i in range(0, len(response), 2)) + "\n")
                logs_box.insert(END, mod_n_text + "\n")
                btn_get_par['state'] = NORMAL
                btn_set_par['state'] = NORMAL
            else:
                self.setvar('mod_addr', 'Не удалось получить номер модуля')
                logs_box.insert(END, "Не удалось получить номер модуля\n")
        elif mode == 'ip':
            query = b'7e010013ff009db37f'
            query_par = b'7e010011ff00fddd7f'
            responses = []
            for i, q in enumerate([query, query_par]):
                print(q)
                logs_box.insert(END, "Запрос " + ' '.join(q.decode()[i:i + 2] for i in range(0, len(q.decode()), 2)) + "\n")
                byte_data = bytes.fromhex(q.decode())
                sock.sendall(byte_data)
                try:
                    data = sock.recv(1024)
                    if data:
                        responses.append(data)
                except Exception as e:
                    print(f'Какая-то ошибка - {e}')
                print(' '.join(responses[i].hex()[j:j + 2] for j in range(0, len(responses[i].hex()), 2)))
                if responses[i]:
                    logs_box.insert(END,
                                    "Ответ " + ' '.join(responses[i].hex()[j:j + 2] for j in range(0, len(responses[i].hex()), 2))
                                    + "\n")
                    logs_box.see(END)
                time.sleep(0.5)
            self.show_mod_data(responses)
        else:
            print('Непонятен тип подключения')

    def show_mod_data(self, r):
        resp_mod_num = r[0].hex()
        print(resp_mod_num)
        modules = []
        if resp_mod_num[:10] == '7e01001300':
            lenght = resp_mod_num[10:12]
            for i in range(int(int(lenght, 16)/9)):
                mod_info = resp_mod_num[12+9*i*2:12+(i+1)*9*2]
                print(i, mod_info)
                mod_number = int((mod_info[2:4] + mod_info[:2]), 16)
                # self.setvar('var_num_' + str(i + 1), mod_number)
                start_freq = int((mod_info[6:8] + mod_info[4:6]), 16)
                # self.setvar('var_freq_min_' + str(i + 1), start_freq)
                stop_freq = int((mod_info[10:12] + mod_info[8:10]), 16)
                # self.setvar('var_freq_max_' + str(i + 1), stop_freq)
                modules.append({'mod_num': mod_number, 'start_freq': start_freq, 'stop_freq': stop_freq})
                print(f'{mod_number}, {start_freq} - {stop_freq}')
        resp_mod_data = r[1].hex()
        print(resp_mod_data)
        if resp_mod_data[:10] == '7e01001100':
            print(resp_mod_data[10:])
            lenght = resp_mod_data[10:12]
            mod_datas = resp_mod_data[20:]
            for i in range(int((int(lenght, 16) - 4)/8)):
                mod_data = mod_datas[i*8*2:(i+1)*8*2]
                print(i, mod_data)
                mod_number_from_mod_data = int((mod_data[2:4] + mod_data[:2]), 16)
                mod_rf = str(int(mod_data[4:6], 16)) + ' дБм'
                # self.setvar('var_rf_' + str(i + 1), mod_rf)
                mod_tmp = str(int(mod_data[6:8], 16)) + '℃'
                # self.setvar('var_tmp_' + str(i + 1), mod_tmp)
                mod_vol = str(int(mod_data[8:10], 16)) + 'В'
                # self.setvar('var_vol_' + str(i + 1), mod_vol)
                mod_cur = str(int(mod_data[10:12], 16)) + 'А'
                # self.setvar('var_cur_' + str(i + 1), mod_cur)
                mod_vswr = int(mod_data[12:14], 16)/10
                # self.setvar('var_vswr_' + str(i + 1), mod_vswr)
                alarm_bit = bin(int(mod_data[14:16], 16))[2:].zfill(8)
                mod_addition_data = {'rf': mod_rf,
                                     'tmp': mod_tmp,
                                     'vol': mod_vol,
                                     'cur': mod_cur,
                                     'vswr': mod_vswr,
                                     'rf_switch': alarm_bit[-1],
                                     'alarm_tmp': alarm_bit[-2],
                                     'alarm_vol': alarm_bit[-3],
                                     'alarm_cur': alarm_bit[-4],
                                     'alarm_vswr': alarm_bit[-5]
                                     }
                for mod in modules:
                    if mod['mod_num'] == mod_number_from_mod_data:
                        mod.update(mod_addition_data)
                        break
        print(modules)
        for i, mod in enumerate(modules):
            self.setvar('var_num_' + str(i + 1), mod['mod_num'])
            self.setvar('var_freq_min_' + str(i + 1), mod['start_freq'])
            self.setvar('var_freq_max_' + str(i + 1), mod['stop_freq'])
            self.setvar('var_rf_' + str(i + 1), mod['rf'])
            self.setvar('var_tmp_' + str(i + 1), mod['tmp'])
            self.setvar('var_vol_' + str(i + 1), mod['vol'])
            self.setvar('var_cur_' + str(i + 1), mod['cur'])
            self.setvar('var_vswr_' + str(i + 1), mod['vswr'])
            self.setvar('rf_switch_' + str(i + 1), mod['rf_switch'])
            alarm_tmp_name = 'alarm_tmp_' + str(i + 1)
            if mod['alarm_tmp'] == '1':
                self.var_lf[alarm_tmp_name].config(image=self.img_red)
            else:
                self.var_lf[alarm_tmp_name].config(image=self.img_green)
            alarm_vol_name = 'alarm_vol_' + str(i + 1)
            if mod['alarm_vol'] == '1':
                self.var_lf[alarm_vol_name].config(image=self.img_red)
            else:
                self.var_lf[alarm_vol_name].config(image=self.img_green)
            alarm_cur_name = 'alarm_cur_' + str(i + 1)
            if mod['alarm_cur'] == '1':
                self.var_lf[alarm_cur_name].config(image=self.img_red)
            else:
                self.var_lf[alarm_cur_name].config(image=self.img_green)
            alarm_vswr_name = 'alarm_vswr_' + str(i + 1)
            if mod['alarm_vswr'] == '1':
                self.var_lf[alarm_vswr_name].config(image=self.img_red)
            else:
                self.var_lf[alarm_vswr_name].config(image=self.img_green)

    def update_mod_data(self, r):
        print(r.hex())

    def get_par(self):
        pass

    def set_par(self):
        pass

    def set_par_test(self, on=True):
        if on:
            test_query = b'7e010020ff52fddd0a00200368036a0384038603b603b803d40328010f00fc082e09380974097e09a609c409280a28011e0020034c0400000000000000000000000028007300580220030000000000000000000000002800ca487f'
        else:
            test_query = b'7e010020ff52fddd0a00200368036a0384038603b603b803d40328000f00fc082e09380974097e09a609c409280a28001e0020034c0400000000000000000000000028007300580220030000000000000000000000002800ca487f'
        try:
            # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # sock.settimeout(5)
            # sock.connect((self.ip.get(), 5000))
            # print(f'Подключен к {self.ip.get()}:5000')
            # l_text = 'ПОДКЛЮЧЕНО к ' + self.ip.get() + ':5000'
            # self.setvar('con_st', l_text)
            # btn_discon['state'] = NORMAL
            # btn_set_par['state'] = NORMAL
            response = ''
            print(test_query)
            logs_box.insert(END,
                            "Запрос " + ' '.join(test_query.decode()[i:i + 2] for i in range(0, len(test_query.decode()), 2)) + "\n")
            byte_data = bytes.fromhex(test_query.decode())
            global sock
            sock.sendall(byte_data)
            try:
                response = sock.recv(1024)
            except Exception as e:
                print(f'Какая-то ошибка - {e}')
            print(' '.join(response.hex()[j:j + 2] for j in range(0, len(response.hex()), 2)))
            if response:
                logs_box.insert(END,
                                "Ответ " + ' '.join(
                                    response.hex()[j:j + 2] for j in range(0, len(response.hex()), 2))
                                + "\n")
                logs_box.see(END)
                self.update_mod_data(response)
            time.sleep(0.3)
            # self.set_mod_data(response)
        except Exception as e:
            print(e)

    def set_auto(self):
        if self.auto:
            self.btn_auto.config(text='Включить', bootstyle=SUCCESS)
            self.auto = False
        else:
            self.btn_auto.config(text="Выключить", bootstyle=DANGER)
            self.auto = True
            self.after(0, self.survey)

    def survey(self):
        req = self.after(1000, self.survey)
        # print('conf')
        print(req)
        if not self.auto:
            self.after_cancel(req)

    def set_state_frame(self, widget, state):
        try:
            # if hasattr(widget, 'state') and callable(getattr(widget, 'state')):
            #     if state == 'disabled':
            #         widget.state(['disabled'])
            #     else:
            #         widget.state(['!disabled'])
            # elif 'state' in widget.config():
            widget.config(state=DISABLED)

        except Exception as e:
            print(e)


if __name__ == '__main__':
    app = ttk.Window("KAPPA", themename="darkly")
    Kappa(app)
    app.mainloop()

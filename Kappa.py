import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText
from ttkbootstrap.tableview import Tableview
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
        self.type_var = ttk.StringVar(value='ip')
        self.ip = ttk.StringVar(value='10.1.4.157')
        # self.connection_state = "Нет подключения"
        # self.columnconfigure(0, weight=1)
        # self.columnconfigure(1, weight=1)
        # self.columnconfigure(2, weight=1)
        # self.rowconfigure(0, weight=1)
        # self.rowconfigure(1, weight=1)
        # self.rowconfigure(2, weight=1)
        row0 = ttk.Frame(self)
        row0.grid(row=0, column=0, sticky=NSEW)
        opt_ip = ttk.LabelFrame(row0, text="Тип подключения")
        opt_ip.pack(fill=BOTH, expand=YES, pady=15, padx=15)
        type_con = ttk.Frame(master=opt_ip)
        type_con.pack(fill=BOTH, expand=YES)
        opt_rb_ip = ttk.Radiobutton(type_con,
                                    text='IP',
                                    command=self.on_type_selection,
                                    variable=self.type_var,
                                    value='ip')
        opt_rb_ip.pack(side=LEFT, padx=30, pady=(0, 5))
        self.opt_ip_inp = ttk.Entry(type_con, textvariable=self.ip)
        self.opt_ip_inp.pack(side=LEFT, padx=30, pady=(0, 5))
        opt_rb_com = ttk.Radiobutton(opt_ip,
                                     text='COM',
                                     command=self.on_type_selection,
                                     variable=self.type_var,
                                     value='com')
        opt_rb_com.pack(side=LEFT, padx=30, pady=(0, 10))
        self.option_lf = ttk.LabelFrame(row0, text="Подключение к COM порту")
        self.option_lf.pack(fill=BOTH, expand=YES, pady=(0, 15), padx=15)
        # self.option_lf.columnconfigure(0, weight=1)
        # self.option_lf.rowconfigure(0, weight=1)
        self.create_connection_buttons()
        row1 = ttk.Frame(self)
        row1.grid(row=1, column=0, sticky=NSEW)
        self.option_lf_addr = ttk.LabelFrame(row1, text="Адрес Модуля")
        self.option_lf_addr.pack(fill=BOTH, expand=YES, pady=(0, 15), padx=15)
        # self.option_lf_addr.columnconfigure(0, weight=1)
        # self.option_lf_addr.rowconfigure(0, weight=1)
        self.create_get_addr_button()
        self.option_lf_mod = ttk.LabelFrame(row1, text="Параметры модуля")
        self.option_lf_mod.pack(fill=BOTH, expand=YES, pady=(0, 15), padx=15)
        self.create_get_set_pars_buttons()
        self.var_lf = {}
        for i in range(4):
            var_name = f'mod{i + 1}'
            col = ttk.Frame(self)
            # col.grid(row=0, column=(i // 2) + 1, sticky=NSEW)
            if i % 2 == 0:
                col.grid(row=0, column=(i // 2) + 1, sticky=NSEW, pady=(15, 0), padx=15)
            else:
                col.grid(row=1, column=(i // 2) + 1, sticky=NSEW, padx=15)
            self.var_lf[var_name] = ttk.LabelFrame(col, text=i + 1)
            self.var_lf[var_name].pack(fill=BOTH, expand=YES, pady=(0, 15))
            # global alarm_rf, alarm_tmp, alarm_vol, alarm_cur, alarm_vswr
            fr_par_num = ttk.Frame(self.var_lf[var_name])
            fr_par_num.pack(fill=X)
            mod_num = ttk.Label(fr_par_num, text='Номер модуля:')
            mod_num.pack(side=LEFT, anchor=N, padx=15, pady=(15, 5))
            var_num_name = f'var_num_{i + 1}'
            var_rf_out = ttk.Label(fr_par_num, textvariable='var_num_name')
            var_rf_out.pack(side=LEFT, anchor=N, fill=X, pady=(15, 5))
            self.setvar('var_num_name', '-')
            fr_par_rf = ttk.Frame(self.var_lf[var_name])
            fr_par_rf.pack(fill=X)
            lbl_rf_out = ttk.Label(fr_par_rf, text='Мощность RF:')
            lbl_rf_out.pack(side=LEFT, anchor=N, padx=15, pady=(0, 5))
            var_rf_out = ttk.Label(fr_par_rf, textvariable='var_rf')
            var_rf_out.pack(side=LEFT, anchor=N, fill=X, pady=(0, 5), padx=(0, 15))
            self.setvar('var_rf', '-')
            alarm_rf_name = f'alarm_rf_{i + 1}'
            self.var_lf[alarm_rf_name] = ttk.Label(fr_par_rf, image=self.img_red)
            self.var_lf[alarm_rf_name].pack(side=RIGHT, anchor=N, fill=X, padx=(20, 40))
            fr_par_tmp = ttk.Frame(self.var_lf[var_name])
            fr_par_tmp.pack(fill=X)
            lbl_tmp = ttk.Label(fr_par_tmp, text='Температура:')
            lbl_tmp.pack(side=LEFT, anchor=N, padx=15, pady=(0, 5))
            var_tmp = ttk.Label(fr_par_tmp, textvariable='var_tmp')
            var_tmp.pack(side=LEFT, anchor=N, fill=X, pady=(0, 5), padx=(0, 15))
            self.setvar('var_tmp', '-')
            alarm_tmp_name = f'alarm_tmp_{i + 1}'
            self.var_lf[alarm_tmp_name] = ttk.Label(fr_par_tmp, image=self.img_red)
            self.var_lf[alarm_tmp_name].pack(side=RIGHT, anchor=N, fill=X, padx=(20, 40))
            fr_par_vol = ttk.Frame(self.var_lf[var_name])
            fr_par_vol.pack(fill=X)
            lbl_tmp = ttk.Label(fr_par_vol, text='Напряжение:')
            lbl_tmp.pack(side=LEFT, anchor=N, padx=15, pady=(0, 5))
            var_tmp = ttk.Label(fr_par_vol, textvariable='var_vol')
            var_tmp.pack(side=LEFT, anchor=N, fill=X, pady=(0, 5))
            self.setvar('var_vol', '-')
            alarm_vol_name = f'alarm_vol_{i + 1}'
            self.var_lf[alarm_vol_name] = ttk.Label(fr_par_vol, image=self.img_red)
            self.var_lf[alarm_vol_name].pack(side=RIGHT, anchor=N, fill=X, padx=(20, 40))
            fr_par_cur = ttk.Frame(self.var_lf[var_name])
            fr_par_cur.pack(fill=X)
            lbl_tmp = ttk.Label(fr_par_cur, text='Потребление:')
            lbl_tmp.pack(side=LEFT, anchor=N, padx=15, pady=(0, 5))
            var_tmp = ttk.Label(fr_par_cur, textvariable='var_cur')
            var_tmp.pack(side=LEFT, anchor=N, fill=X, pady=(0, 5))
            self.setvar('var_cur', '-')
            alarm_cur_name = f'alarm_cur_{i + 1}'
            self.var_lf[alarm_cur_name] = ttk.Label(fr_par_cur, image=self.img_red)
            self.var_lf[alarm_cur_name].pack(side=RIGHT, anchor=N, fill=X, padx=(20, 40))
            fr_par_vswr = ttk.Frame(self.var_lf[var_name])
            fr_par_vswr.pack(fill=X)
            lbl_tmp = ttk.Label(fr_par_vswr, text='КСВ:')
            lbl_tmp.pack(side=LEFT, anchor=N, padx=15, pady=(0, 5))
            var_tmp = ttk.Label(fr_par_vswr, textvariable='var_vswr')
            var_tmp.pack(side=LEFT, anchor=N, fill=X, pady=(0, 5))
            self.setvar('var_vswr', '-')
            alarm_vswr_name = f'alarm_vswr_{i + 1}'
            self.var_lf[alarm_vswr_name] = ttk.Label(fr_par_vswr, image=self.img_red)
            self.var_lf[alarm_vswr_name].pack(side=RIGHT, anchor=N, fill=X, padx=(20, 40))
            # rf_switch = 0
            rf_switch_name = f'rf_switch_{i + 1}'
            self.setvar(rf_switch_name, 0)
            rf_sw = ttk.Checkbutton(master=self.var_lf[var_name],
                                    text='Кнопка вкл. RF',
                                    bootstyle='danger-round-toggle',
                                    variable=rf_switch_name)
            rf_sw.pack(side=LEFT, anchor=N, padx=(15, 5))
        # col2 = ttk.Frame(self)
        # col2.grid(row=0, column=1, sticky=NSEW)
        # self.option_lf_pars = ttk.LabelFrame(col2, text="Параметры")
        # self.option_lf_pars.pack(fill=BOTH, side=TOP, expand=YES, pady=15, padx=15)
        # self.create_pars()
        log_bar = ttk.Frame(self)
        log_bar.grid(row=2, column=0, columnspan=3, sticky=NSEW)
        self.option_lf_logs = ttk.LabelFrame(log_bar, text="Лог")
        self.option_lf_logs.pack(fill=BOTH, expand=YES, pady=15, padx=15)
        self.create_log_bar()

    def create_log_bar(self):
        # txt = ttk.Label(master=self.option_lf_logs, text='ЛОГИ')
        # txt.pack(fill=X, expand=YES, padx=15, pady=(0, 15))
        global logs_box
        logs_box = ScrolledText(master=self.option_lf_logs, height=10)
        logs_box.pack(fill=X, expand=YES, padx=15, pady=15)
        logs_box.insert(END, 'Программа готова к работе\n')

    # def create_pars(self):
    #     global alarm_rf, alarm_tmp, alarm_vol, alarm_cur, alarm_vswr
    #     fr_par_rf = ttk.Frame(self.option_lf_pars)
    #     fr_par_rf.pack(fill=X)
    #     lbl_rf_out = ttk.Label(fr_par_rf, text='Мощность RF:')
    #     lbl_rf_out.pack(side=LEFT, anchor=N, padx=15, pady=(15, 5))
    #     var_rf_out = ttk.Label(fr_par_rf, textvariable='var_rf')
    #     var_rf_out.pack(side=LEFT, anchor=N, fill=X, pady=(15, 5))
    #     self.setvar('var_rf', '-')
    #     # alarm_rf = ttk.Label(fr_par_rf, image=self.img_red)
    #     # alarm_rf.pack(side=RIGHT, anchor=N, fill=X, pady=(15, 5), padx=(0, 70))
    #     fr_par_tmp = ttk.Frame(self.option_lf_pars)
    #     fr_par_tmp.pack(fill=X)
    #     lbl_tmp = ttk.Label(fr_par_tmp, text='Температура:')
    #     lbl_tmp.pack(side=LEFT, anchor=N, padx=15, pady=(0, 5))
    #     var_tmp = ttk.Label(fr_par_tmp, textvariable='var_tmp')
    #     var_tmp.pack(side=LEFT, anchor=N, fill=X, pady=(0, 5))
    #     self.setvar('var_tmp', '-')
    #     alarm_tmp = ttk.Label(fr_par_tmp, image=self.img_red)
    #     alarm_tmp.pack(side=RIGHT, anchor=N, fill=X, padx=(0, 70))
    #     fr_par_vol = ttk.Frame(self.option_lf_pars)
    #     fr_par_vol.pack(fill=X)
    #     lbl_tmp = ttk.Label(fr_par_vol, text='Напряжение:')
    #     lbl_tmp.pack(side=LEFT, anchor=N, padx=15, pady=(0, 5))
    #     var_tmp = ttk.Label(fr_par_vol, textvariable='var_vol')
    #     var_tmp.pack(side=LEFT, anchor=N, fill=X, pady=(0, 5))
    #     self.setvar('var_vol', '-')
    #     alarm_vol = ttk.Label(fr_par_vol, image=self.img_red)
    #     alarm_vol.pack(side=RIGHT, anchor=N, fill=X, padx=(0, 70))
    #     fr_par_cur = ttk.Frame(self.option_lf_pars)
    #     fr_par_cur.pack(fill=X)
    #     lbl_tmp = ttk.Label(fr_par_cur, text='Потребление:')
    #     lbl_tmp.pack(side=LEFT, anchor=N, padx=15, pady=(0, 5))
    #     var_tmp = ttk.Label(fr_par_cur, textvariable='var_cur')
    #     var_tmp.pack(side=LEFT, anchor=N, fill=X, pady=(0, 5))
    #     self.setvar('var_cur', '-')
    #     alarm_cur = ttk.Label(fr_par_cur, image=self.img_red)
    #     alarm_cur.pack(side=RIGHT, anchor=N, fill=X, padx=(0, 70))
    #     fr_par_vswr = ttk.Frame(self.option_lf_pars)
    #     fr_par_vswr.pack(fill=X)
    #     lbl_tmp = ttk.Label(fr_par_vswr, text='КСВ:')
    #     lbl_tmp.pack(side=LEFT, anchor=N, padx=15, pady=(0, 5))
    #     var_tmp = ttk.Label(fr_par_vswr, textvariable='var_vswr')
    #     var_tmp.pack(side=LEFT, anchor=N, fill=X, pady=(0, 5))
    #     self.setvar('var_vswr', '-')
    #     alarm_vswr = ttk.Label(fr_par_vswr, image=self.img_red)
    #     alarm_vswr.pack(side=RIGHT, anchor=N, fill=X, padx=(0, 70))
    #     # rf_switch = 0
    #     self.setvar('rf_switch', 0)
    #     rf_sw = ttk.Checkbutton(master=self.option_lf_pars,
    #                             text='Кнопка вкл. RF',
    #                             bootstyle='danger-round-toggle',
    #                             variable='rf_switch')
    #     rf_sw.pack(side=LEFT, anchor=N, padx=(15, 5))

    def create_connection_buttons(self):
        container = ttk.Frame(self.option_lf)
        container.pack(fill=X, expand=YES)
        global btn_discon, btn_con
        btn_con = ttk.Button(master=container, text="Подключить", command=self.on_connect)
        btn_con.pack(side=LEFT, padx=15, pady=15)
        btn_discon = ttk.Button(master=container, text="Отключить", command=self.on_disconnect, state=DISABLED)
        btn_discon.pack(side=LEFT, padx=(0, 15), pady=15)
        self.setvar('con_st', 'Нет подключения')
        txt = ttk.Label(master=self.option_lf, textvariable='con_st')
        txt.pack(fill=X, expand=YES, padx=15, pady=(0, 15))

    def create_get_addr_button(self):
        container = ttk.Frame(self.option_lf_addr)
        container.pack(fill=BOTH, expand=YES)
        global btn_get_addr
        btn_get_addr = ttk.Button(master=container, text="Получить адрес", command=self.get_mod_address, state=DISABLED)
        btn_get_addr.pack(side=LEFT, padx=15, pady=15)
        self.setvar('mod_addr', 'Неизвестно')
        txt = ttk.Label(master=self.option_lf_addr, textvariable='mod_addr')
        txt.pack(fill=X, expand=YES, padx=15, pady=(0, 15))

    def create_get_set_pars_buttons(self):
        container = ttk.Frame(self.option_lf_mod)
        container.pack(fill=BOTH, expand=YES)
        global btn_get_par, btn_set_par
        btn_get_par = ttk.Button(master=container, text="Получить", command=self.get_par, state=DISABLED)
        btn_get_par.pack(side=LEFT, padx=15, pady=15)
        btn_set_par = ttk.Button(master=container, text="Загрузить", command=self.set_par, state=DISABLED)
        btn_set_par.pack(side=LEFT, padx=15, pady=15)

    def on_type_selection(self):
        print(self.type_var.get())
        print(self.ip.get())
        if self.type_var.get() == 'com':
            self.opt_ip_inp['state'] = DISABLED
        else:
            self.opt_ip_inp['state'] = NORMAL

    def on_connect(self):
        sock = False
        if self.type_var.get() == 'com':
            global con
            con = DDS.get_con()
            if con:
                l_text = 'ПОДКЛЮЧЕНО к ' + con.name
                self.setvar('con_st', l_text)
                logs_box.insert(END, l_text + '\n')
                btn_discon['state'] = NORMAL
                btn_con['state'] = DISABLED
                btn_get_addr['state'] = NORMAL
            else:
                self.setvar('con_st', 'Ошибка! Попробуйте ещё раз!')
                logs_box.insert(END, "Ошибка подключения\n")
        else:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                sock.connect((self.ip.get(), 5000))
                print(f'Подключен к {self.ip.get()}:5000')
                # query = DDS.get_address_query()
                query = b'7e010013ff009db37f'
                print(query)
                # logs_box.insert(END, "Запрос " + ' '.join(query[i:i + 2] for i in range(0, len(query), 2)) + "\n")
                byte_data = bytes.fromhex('7e010013ff009db37f')
                sock.sendall(byte_data)
                response = sock.recv(1024)
                # print(response)
                print(' '.join(response.hex()[i:i + 2] for i in range(0, len(response.hex()), 2)))
                # if response:
                #     logs_box.insert(END,
                #                     "Ответ " + ' '.join(response[i:i + 2] for i in range(0, len(response), 2)) + "\n")
            except Exception as e:
                print(e)
            finally:
                if 'sock' in locals() and sock:
                    sock.close()
                    print('Соединение отключено')

    def on_disconnect(self):
        is_closed = DDS.close_con(con)
        if is_closed:
            self.setvar('con_st', 'ОТКЛЮЧЕНО')
            btn_con['state'] = NORMAL
            btn_discon['state'] = DISABLED
            btn_get_addr['state'] = DISABLED
            btn_get_par['state'] = DISABLED
            btn_set_par['state'] = DISABLED
            logs_box.insert(END, "ОТКЛЮЧЕНО\n")
        else:
            self.setvar('con_st', 'ОШИБКА ОТКЛЮЧЕНИЯ')
            logs_box.insert(END, "ОШИБКА ОТКЛЮЧЕНИЯ\n")

    def get_mod_address(self):
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

    def get_par(self):
        # if module_number:
        #     query = DDS.get_par_query(module_number)
        #     logs_box.insert(END, "Запрос " + ' '.join(query[i:i + 2] for i in range(0, len(query), 2)) + "\n")
        #     response = DDS.send_query(con, query)
        #     if response:
        #         logs_box.insert(END, "Ответ " + ' '.join(response[i:i + 2] for i in range(0, len(response), 2)) + "\n")
        #         self.setvar('var_rf', str(int(response[-18:-16], 16)) + 'дБм')
        #         self.setvar('var_tmp', str(int(response[-16:-14], 16)) + '℃')
        #         self.setvar('var_vol', str(int(response[-14:-12], 16)) + 'В')
        #         self.setvar('var_cur', str(int(response[-12:-10], 16)) + 'А')
        #         self.setvar('var_vswr', str(int(response[-10:-8], 16)/10))
        #         alarm_bit = bin(int(response[-8:-6], 16))[2:].zfill(8)
        #         global rf_switch
        #         if alarm_bit[-1] == '1':
        #             self.setvar('rf_switch', 1)
        #         else:
        #             self.setvar('rf_switch', 0)
        #         if alarm_bit[-2] == '1':
        #             alarm_tmp.config(image=self.img_red)
        #         else:
        #             alarm_tmp.config(image=self.img_green)
        #         if alarm_bit[-3] == '1':
        #             alarm_vol.config(image=self.img_red)
        #         else:
        #             alarm_vol.config(image=self.img_green)
        #         if alarm_bit[-4] == '1':
        #             alarm_cur.config(image=self.img_red)
        #         else:
        #             alarm_cur.config(image=self.img_green)
        #         if alarm_bit[-5] == '1':
        #             alarm_vswr.config(image=self.img_red)
        #         else:
        #             alarm_vswr.config(image=self.img_green)
        #     else:
        #         logs_box.insert(END, "Не удалось получить параметры модуля\n")
        # else:
        #     logs_box.insert(END, 'Запросите сначала адрес модуля!')
        pass

    def set_par(self):
        pass


if __name__ == '__main__':
    app = ttk.Window("KAPPA", themename="darkly")
    Kappa(app)
    app.mainloop()

from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from models import Users, Products, Tickets
from sqlalchemy import and_, or_, text
from barcode import EAN13
from barcode.writer import ImageWriter
import db

class Login:

    db = "databases/drugstore.db"

    def __init__(self, root):
        self.window = root
        self.window.title("FARMACIA LA PAC")
        self.window["bg"] = "white"
        self.window.resizable(0, 0)

        frame = LabelFrame(self.window, bg = "white")
        frame.grid(row = 0, column= 0, columnspan = 3)

        self.message = Label(self.window, text="¡QUE BUENO VOLVER A VERTE!", bg = "white")
        self.message.grid(row = 1, columnspan = 3, pady = 20)

        # Image
        self.logo = Image.open("resource/logo.png")  # 400 x 398 pixeles
        self.logo = ImageTk.PhotoImage(self.logo)
        self.logo_label = Label(frame, image = self.logo)
        self.logo_label.image = self.logo
        self.logo_label.grid(row = 0, column = 0)

        # Label usuario
        self.label_user = Label(frame, text = "USUARIO", width = 50, bg = "white")
        self.label_user.grid(row = 2, column = 0, pady = 5)
        # Input usuario
        self.user = Entry(frame, width = 53, borderwidth = 3)
        self.user.place(height = 100)
        self.user.grid(row = 3, column = 0)
        self.user.focus()

        # Label passwd
        self.label_passwd = Label(frame, text = "CONTRASEÑA", width = 50, bg = "white")
        self.label_passwd.grid(row = 4, column = 0, pady = 5)
        # Input passwd
        self.passwd = Entry(frame, width = 53, show = "*", borderwidth = 3)
        self.passwd.grid(row = 5, column = 0)

        #Button iniciar
        self.init = ttk.Button(frame, text = "INICIAR SESIÓN", width = 50, padding = 10, command = self.login)
        self.init.grid(row = 6, pady = 10)

    def login(self):

        try:
            row = db.session.query(Users).where(Users.name == self.user.get() and Users.passwd == self.passwd.get()).first()
            if row.name == self.user.get() and row.passwd == self.passwd.get():
                self.message["text"] = "LOGIN CORRECTO PARA {}".format(row.name.upper())
                self.message["fg"] = "green"
                if row.rol == "admin":
                    changeApp(Admin)
                elif row.rol == "vendedor":
                    changeApp(Salesman)
                elif row.rol == "cajero":
                    changeApp(Checker)
            else:
                self.message["text"] = "LOGIN FAILED"
                self.message["fg"] = "red"

        except AttributeError:
            self.message["text"] = "EL USUARIO NO EXISTE!"
            self.message["fg"] = "red"
            return self.message

class Admin:

    db = "database/drugstore.db"

    def backLogin(self):
        changeApp(Login)

    def __init__(self, root):
        self.window = root
        self.window.title("FARMACIA LA PAC - ADMINISTRADOR")
        self.window.geometry("1024x720")
        self.window.resizable(0, 0)

        # Menu bar
        self.menu = Menu(root)
        root.config(menu=self.menu)
        self.admin_menu = Menu(self.menu, tearoff = 0)
        self.menu.add_cascade(label="ADMINISTRADOR", menu=self.admin_menu)
        self.admin_menu.add_command(label="Cerrar sesión", command=self.backLogin)

        # Tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack()

        self.productos = Frame(self.notebook, width=1024, height=720)
        self.busqueda = Frame(self.notebook, width=1024, height=720)
        self.edit = Frame(self.notebook, width=1024, height=720)
        self.usuarios = Frame(self.notebook, width=1024, height=720)

        self.productos.pack(fill="both", expand=1)
        self.busqueda.pack(fill="both", expand=1)
        self.edit.pack(fill="both", expand=1)
        self.usuarios.pack(fill="both", expand=1)

        self.notebook.add(self.productos, text="LISTA DE PRODUCTOS")
        self.notebook.add(self.busqueda, text="BUSQUEDA DE PRODUCTOS")
        self.notebook.add(self.edit, text="EDITAR PRODUCTO")
        self.notebook.add(self.usuarios, text="CREAR USUARIOS")

        self.notebook.tab(self.edit, state="disabled")

        # Frame de registro

        frameP = LabelFrame(self.productos)
        frameP.grid(row=0, column=0, columnspan=6, pady=10)

        self.labelTitle = Label(frameP, text="INGRESO DE PRODUCTOS", font=(20))
        self.labelTitle.grid(row = 0, columnspan = 6, pady = 10, sticky = W + E)

        self.separator1 = ttk.Separator(frameP, orient="horizontal")
        self.separator1.grid(row=1, columnspan = 6, sticky = W + E)

        self.labelCode = Label(frameP, text="CODIGO")
        self.labelCode.grid(row=2, column=0, pady=15)
        self.entryCode = Entry(frameP, borderwidth=3, width = 70)
        self.entryCode.focus()
        self.entryCode.grid(row=2, column=1, sticky = W + E, columnspan = 2)

        self.labelName = Label(frameP, text="DESCRIPCION   ")
        self.labelName.grid(row=2, column=3, pady=10, sticky = E)
        self.entryName = Entry(frameP, borderwidth=3, width = 67)
        self.entryName.grid(row=2, column=4, sticky = W + E, columnspan = 2)

        self.labelStock = Label(frameP, text="STOCK   ")
        self.labelStock.grid(row=3, column=0, sticky = E)
        self.entryStock = Entry(frameP, borderwidth=3)
        self.entryStock.grid(row=3, column=1, sticky = W + E, pady = 15)

        self.labelPurchase = Label(frameP, text="PRECIO DE COMPRA   ")
        self.labelPurchase.grid(row=3, column=2, sticky = E)
        self.entryPurchase = Entry(frameP, width=20, borderwidth=3)
        self.entryPurchase.grid(row=3, column=3)

        self.labelSale = Label(frameP, text="PRECIO DE VENTA   ")
        self.labelSale.grid(row=3, column=4, sticky = E)
        self.entrySale = Entry(frameP, width=20, borderwidth=3)
        self.entrySale.grid(row=3, column=5, sticky = W + E)

        self.separator = ttk.Separator(frameP, orient="horizontal")
        self.separator.grid(row=4, columnspan = 6, sticky = W + E)

        self.buttonSend = ttk.Button(frameP, text = "REGISTRAR PRODUCTO", padding = 10, command = self.add_products)
        self.buttonSend.grid(row = 5, column = 2, columnspan = 3, sticky = W + E, pady = 10)

        self.message = Label(self.productos, text="")
        self.message.grid(row=1, columnspan=6, pady=10)

        # Frame Lista de Productos

        frameList = LabelFrame(self.productos)
        frameList.grid(row=2, column = 0, columnspan = 4)

        self.labelTitle = Label(frameList, text="LISTA DE PRODUCTOS", font=(20))
        self.labelTitle.grid(row=0, columnspan = 4, pady=10, sticky= W + E)

        self.tabla = ttk.Treeview(frameList, height=15, columns=(1, 2, 3, 4))
        self.tabla.grid(row = 1, column = 0)
        self.tabla.heading("#0", text = "CODIGO", anchor = CENTER)
        self.tabla.heading("#1", text = "DESCRIPCION", anchor = CENTER)
        self.tabla.heading("#2", text = "STOCK", anchor = CENTER)
        self.tabla.heading("#3", text = "PRECIO COMPRA", anchor = CENTER)
        self.tabla.heading("#4", text="PRECIO VENTA", anchor=CENTER)

        scrollbar = ttk.Scrollbar(frameList, orient = VERTICAL, command=self.tabla.yview)
        self.tabla.configure(yscroll=scrollbar.set)
        scrollbar.grid(row = 1, column=1, sticky = "ns")

        self.get_productos()

        # TAB DE BUSQUEDA

        frameBusqueda = Frame(self.busqueda)
        frameBusqueda.grid(row=0, column=0, columnspan=4, pady=10)

        self.labelBusqueda = Label(frameBusqueda, text="BUSQUEDA DE PRODUCTOS", font=(20), width = 112)
        self.labelBusqueda.grid(row=0, columnspan=4, pady=10, sticky= W + E)

        self.separator = ttk.Separator(frameBusqueda, orient="horizontal")
        self.separator.grid(row=1, columnspan = 4, sticky = W + E, pady=10)

        self.labelCodeBusqueda = Label(frameBusqueda, text="CODIGO   ")
        self.labelCodeBusqueda.grid(row=2, column=0, pady=10, sticky = E)
        self.entryCodeBusqueda = Entry(frameBusqueda, width = 60, borderwidth = 3)
        self.entryCodeBusqueda.grid(row=2, column=1, columnspan=2, sticky = W + E)

        self.buttonBusqueda = ttk.Button(frameBusqueda, text="BUSCAR", width=80, padding=10, command=self.find)
        self.buttonBusqueda.grid(row=3, column=1, columnspan=2, sticky= W + E, pady=10)

        self.labelMessageBus = Label(frameBusqueda, text="")
        self.labelMessageBus.grid(row=4, columnspan=4, sticky=W + E, pady=10)

        frameList2 = LabelFrame(self.busqueda, width = 1024)
        frameList2.grid(row=1, column=0, columnspan=4, pady=10)

        self.labelTitle = Label(frameList2, text="LISTA DE PRODUCTOS", font=(20))
        self.labelTitle.grid(row=0, columnspan=4, pady=10, sticky=W + E)

        self.tablaBus = ttk.Treeview(frameList2, height=15, columns=(1, 2, 3, 4))
        self.tablaBus.grid(row=1, column=0)
        self.tablaBus.heading("#0", text="CODIGO", anchor=CENTER)
        self.tablaBus.heading("#1", text="DESCRIPCION", anchor=CENTER)
        self.tablaBus.heading("#2", text="STOCK", anchor=CENTER)
        self.tablaBus.heading("#3", text="PRECIO COMPRA", anchor=CENTER)
        self.tablaBus.heading("#4", text="PRECIO VENTA", anchor=CENTER)

        scrollbar2 = ttk.Scrollbar(frameList2, orient=VERTICAL, command=self.tablaBus.yview)
        self.tablaBus.configure(yscroll=scrollbar2.set)
        scrollbar2.grid(row=1, column=1, sticky="ns")

        # Frame para botones

        buttonframe = Frame(self.busqueda)
        buttonframe.grid(row=2, column = 0, columnspan = 4, sticky = W + E)

        self.buttonEdit = ttk.Button(buttonframe, text = "EDITAR", padding = 10, width = 80, command = self.edit_product)
        self.buttonEdit.grid(row = 2, column = 0, columnspan = 2)
        self.buttonErrase = ttk.Button(buttonframe, text = "ELIMINAR", padding = 10, width = 80, command = self.del_producto)
        self.buttonErrase.grid(row=2, column = 3, columnspan = 2)

        self.get_productosB()
        self.get_productos()

    # TAB CREAR USUARIOS

        frameUser = Frame(self.usuarios)
        frameUser.grid(row=0, column=0, columnspan= 4, pady=10)

        self.userTitle = Label(frameUser, text="CREACION DE USUARIOS", font=(20))
        self.userTitle.grid(row=0, columnspan= 4, pady=10, sticky = W + E )

        self.separatorUser = ttk.Separator(frameUser, orient="horizontal")
        self.separatorUser.grid(row=1, columnspan = 4, sticky = W + E, pady=10)

        self.labelUser = Label(frameUser, text="USUARIO ")
        self.labelUser.grid(row=2, column=0)
        self.entryUser = Entry(frameUser, width=60, borderwidth=3)
        self.entryUser.grid(row=2, column=1, pady=10, sticky = E)

        self.labelPwd = Label(frameUser, text="CONTRASEÑA ")
        self.labelPwd.grid(row=2, column=2)
        self.entryPwd = Entry(frameUser, width=62, borderwidth=3, show="*")
        self.entryPwd.grid(row=2, column=3, pady=10, sticky = E)

        self.labelRol = Label(frameUser, text="ROL DEL USUARIO ")
        self.labelRol.grid(row=3, column=0, pady=10)
        self.rol = StringVar(frameUser)
        self.rol.set("")
        self.entryRol = OptionMenu(frameUser, self.rol, "ADMIN", "VENDEDOR", "CAJERO")
        self.entryRol.grid(row=3, column=1, pady=10, columnspan=1, sticky = W + E)

        self.labelConfirm = Label(frameUser, text="CONFIRME LA CONTRASEÑA ")
        self.labelConfirm.grid(row=3, column=2, pady=10)
        self.entryConfrim = Entry(frameUser, width=62, borderwidth=3, show="*")
        self.entryConfrim.grid(row=3, column=3, columnspan=2, pady=10, sticky = E)

        self.separatorUser2 = ttk.Separator(frameUser, orient="horizontal")
        self.separatorUser2.grid(row=4, columnspan = 4, sticky = W + E, pady=10)

        self.buttonCrear = ttk.Button(frameUser, text = "CREAR NUEVO USUARIO", padding=10, width=80, command=self.add_user)
        self.buttonCrear.grid(row=5, columnspan=4, pady=10)

        self.messageUser = Label(frameUser, text="")
        self.messageUser.grid(row=6, columnspan=4, sticky = W + E, pady=10)

        # FRAME LISTA DE USUARIOS

        frameListUsers = Frame(self.usuarios)
        frameListUsers.grid(row=1, column=0, columnspan = 3, pady=10)
        self.separatorListUser = ttk.Separator(frameListUsers, orient="horizontal")
        self.separatorListUser.grid(row=0, columnspan = 3, sticky = W + E)

        self.labelTitleList = Label(frameListUsers, text="LISTA DE USUARIOS", width=113, font = (20))
        self.labelTitleList.grid(row=1, columnspan=3, pady=10, sticky = W + E)
        self.tablaUsers = ttk.Treeview(frameListUsers, height=10, columns=(1))
        self.tablaUsers.grid(row=2, columnspan=3, sticky = W + E)
        self.tablaUsers.heading("#0", text="NOMBRE DE USUARIO", anchor=CENTER)
        self.tablaUsers.heading("#1", text="ROL DEL USUARIO", anchor= CENTER)
        self.get_users()

        # FRAME BOTONES USUARIOS

        frameButtonUsers = Frame(self.usuarios)
        frameButtonUsers.grid(row=2, column=0, columnspan=2, pady=10)

        self.buttonEditUsers = ttk.Button(frameButtonUsers, text="EDITAR USUARIO", width=81, padding=10, command=self.edit_users)
        self.buttonEditUsers.grid(row=0, column=0, pady=10)
        self.buttonDelUsers = ttk.Button(frameButtonUsers, text="ELIMINAR USUARIO", width=80, padding=10, command=self.del_users)
        self.buttonDelUsers.grid(row=0, column=1, pady=10)

    def get_productos(self):

        registros_tabla = self.tabla.get_children()  # Devuelve los valores que estan en la tabla
        for fila in registros_tabla:
            self.tabla.delete(fila)

        query = "SELECT * FROM products ORDER BY code DESC"  # Consulta a la tabla productos
        registros = db.session.query(Products).from_statement(text(query))
        db.session.commit()
        db.session.close()

        for i in registros:
            self.tabla.insert("", 0, text = i.code, values = [i.name, i.stock, i.purchase_price, i.sale_price])

    def get_productosB(self):

        registros_tabla2 = self.tablaBus.get_children()  # Devuelve los valores que estan en la tabla
        for fila in registros_tabla2:
            self.tablaBus.delete(fila)

        query = "SELECT * FROM products ORDER BY code DESC"  # Consulta a la tabla productos
        registros = db.session.query(Products).from_statement(text(query))
        db.session.commit()
        db.session.close()

        for i in registros:
            self.tablaBus.insert("", 0, text = i.code, values = [i.name, i.stock, i.purchase_price, i.sale_price])

    # Validación de entry

    def valid_code(self):
        code_user = self.entryCode.get()
        return len(code_user) != 0

    def valid_name(self):
        name_user = self.entryName.get()
        return len(name_user) != 0

    def valid_stock(self):
        stock_user = self.entryStock.get()
        return len(stock_user) != 0

    def valid_purchase(self):
        purchase_user = self.entryPurchase.get()
        return len(purchase_user) != 0

    def valid_sale(self):
        sale_user = self.entrySale.get()
        return len(sale_user) != 0

    def add_products(self):
        if self.valid_code() and self.valid_name() and self.valid_stock() and self.valid_purchase() and self.valid_sale():
            p = Products(self.entryCode.get().upper(), self.entryName.get().upper(), self.entryStock.get().upper(), self.entryPurchase.get().upper(), self.entrySale.get().upper())
            db.session.add(p)
            db.session.commit()
            db.session.close()

            self.message["text"] = "{} SE HA REGISTRADO CORRECTAMENTE!".format(self.entryName.get().upper())
            self.message["fg"] = "green"

            # Limpiar formulario

            self.entryCode.delete(0, END)
            self.entryName.delete(0, END)
            self.entryStock.delete(0, END)
            self.entryPurchase.delete(0, END)
            self.entrySale.delete(0, END)

        elif self.valid_code() == False and self.valid_name() and self.valid_stock() and self.valid_purchase() and self.valid_sale():
            self.message["text"] = "EL CODIGO ES OBLIGATORIO"
            self.message["fg"] = "red"

        elif self.valid_code() and self.valid_name() == False and self.valid_stock() and self.valid_purchase() and self.valid_sale():
            self.message["text"] = "LA DESCRIPCION ES OBLIGATORIA"
            self.message["fg"] = "red"

        elif self.valid_code() and self.valid_name() and self.valid_stock() == False and self.valid_purchase() and self.valid_sale():
            self.message["text"] = "EL STOCK ES OBLIGATORIO"
            self.message["fg"] = "red"

        elif self.valid_code() and self.valid_name() and self.valid_stock() and self.valid_purchase() == False and self.valid_sale():
            self.message["text"] = "EL PRECIO DE COMPRA ES OBLIGATORIO"
            self.message["fg"] = "red"

        elif self.valid_code() and self.valid_name() and self.valid_stock() and self.valid_purchase() and self.valid_sale() == False:
            self.message["text"] = "EL PRECIO DE VENTA ES OBLIGAGTORIO"
            self.message["fg"] = "red"

        else:
            self.message["text"] = "DEBE RELLENAR TODOS LOS CAMPOS"
            self.message["fg"] = "red"

        # Actualizar tabla
        self.get_productos()
        self.get_productosB()

    def del_producto(self):

        try:
            self.tablaBus.item(self.tablaBus.selection())["text"]
        except IndexError as e:
            self.labelMessageBus["text"] = "DEBE SELECCIONAR UN PRODUCTO"
            self.labelMessageBus["fg"] = "red"
            return

        code = self.tablaBus.item(self.tablaBus.selection())["text"]

        db.session.query(Products).filter_by(code = code).delete()
        db.session.commit()
        db.session.close()

        self.labelMessageBus["text"] = "{} SE HA ELIMINADO CON EXITO!".format(self.tablaBus.item(self.tablaBus.selection())["values"][0].upper())
        self.labelMessageBus["fg"] = "red"

        self.get_productos()
        self.get_productosB()

    def find(self):
        registros = self.tablaBus.get_children()
        buscar = False
        try:
            for i in registros:
                if self.tablaBus.item(i)["text"] == int(self.entryCodeBusqueda.get()):
                    self.tablaBus.selection_set(i)
                    self.tablaBus.focus(i)
                    buscar = True

            if buscar == False:
                self.labelMessageBus["text"] = "EL PRODUCTO NO EXISTE"
                self.labelMessageBus["fg"] = "red"

        except ValueError:
            self.labelMessageBus["text"] = "DEBE INGRESAR UN CODIGO PARA REALIZAR LA BUSQUEDA"
            self.labelMessageBus["fg"] = "red"

    def edit_product(self):

        try:
            self.tablaBus.item(self.tablaBus.selection())["text"]
        except IndexError as e:
            self.labelMessageBus["text"] = "DEBE SELECCIONAR UN PRODUCTO"
            self.labelMessageBus["fg"] = "red"
            return

        self.notebook.tab(self.edit, state="normal")
        self.notebook.select(2)

        # TAB EDITAR PRODUCTOS

        frameEditar = Frame(self.edit)
        frameEditar.grid(row=0, column=0, columnspan=6, pady=10)

        codeA = self.tablaBus.item(self.tablaBus.selection())["text"]
        nameA = self.tablaBus.item(self.tablaBus.selection())["values"][0]
        stockA = self.tablaBus.item(self.tablaBus.selection())["values"][1]
        purchaseA = self.tablaBus.item(self.tablaBus.selection())["values"][2]
        saleA = self.tablaBus.item(self.tablaBus.selection())["values"][3]

        self.labelTitle = Label(frameEditar, text="MODIFICAR PRODUCTOS", font=(20))
        self.labelTitle.grid(row=0, columnspan=6, pady=10, sticky=W + E)

        self.separator1 = ttk.Separator(frameEditar, orient="horizontal")
        self.separator1.grid(row=1, columnspan=6, sticky=W + E)

        self.labelCodeEdit = Label(frameEditar, text="CODIGO")
        self.labelCodeEdit.grid(row=2, column=0, pady=15)
        self.entryCodeEdit = Entry(frameEditar, borderwidth=3, width=70, textvariable=StringVar(self.edit, value=codeA), state="readonly")
        self.entryCodeEdit.focus()
        self.entryCodeEdit.grid(row=2, column=1, sticky=W + E, columnspan=2)

        self.labelNameEdit = Label(frameEditar, text="DESCRIPCION   ")
        self.labelNameEdit.grid(row=2, column=3, pady=10, sticky=E)
        self.entryNameEdit = Entry(frameEditar, borderwidth=3, width=67, textvariable=StringVar(self.edit, value=nameA))
        self.entryNameEdit.grid(row=2, column=4, sticky=W + E, columnspan=2)

        self.labelStockEdit = Label(frameEditar, text="STOCK   ")
        self.labelStockEdit.grid(row=3, column=0, sticky=E)
        self.entryStockEdit = Entry(frameEditar, borderwidth=3, textvariable=StringVar(self.edit, value=stockA))
        self.entryStockEdit.grid(row=3, column=1, sticky=W + E, pady=15)

        self.labelPurchaseEdit = Label(frameEditar, text="PRECIO DE COMPRA   ")
        self.labelPurchaseEdit.grid(row=3, column=2, sticky=E)
        self.entryPurchaseEdit = Entry(frameEditar, width=20, borderwidth=3, textvariable=StringVar(self.edit, value=purchaseA))
        self.entryPurchaseEdit.grid(row=3, column=3)

        self.labelSaleEdit = Label(frameEditar, text="PRECIO DE VENTA   ")
        self.labelSaleEdit.grid(row=3, column=4, sticky=E)
        self.entrySaleEdit = Entry(frameEditar, width=20, borderwidth=3, textvariable=StringVar(self.edit, value=saleA))
        self.entrySaleEdit.grid(row=3, column=5, sticky=W + E)

        self.separatorEdit = ttk.Separator(frameEditar, orient="horizontal")
        self.separatorEdit.grid(row=4, columnspan=6, sticky=W + E)

        self.buttonSendEdit = ttk.Button(frameEditar, text="EDITAR PRODUCTO", padding=10, command= lambda: self.actualizar_product(self.entryCodeEdit.get(), self.entryNameEdit.get(), self.entryStockEdit.get(), self.entryPurchaseEdit.get(), self.entrySaleEdit.get()))
        self.buttonSendEdit.grid(row=5, column=2, columnspan=3, sticky=W + E, pady=10)

        self.separatorEdit = ttk.Separator(frameEditar, orient="horizontal")
        self.separatorEdit.grid(row=6, columnspan=6, sticky=W + E)

        self.labelMessage = Label(frameEditar, text="")
        self.labelMessage.grid(row = 7, columnspan= 6, sticky = W + E, pady = 10)

    def actualizar_product(self, code, name, stock, purchase, sale):
        producto_modificado = False

        db.session.query(Products).filter(Products.code == code).update({"name": name, "stock": stock, "purchase_price": purchase, "sale_price": sale})
        db.session.commit()
        producto_modificado = True

        if name == "" or stock == "" or purchase == "" or sale == "":
            producto_modificado = False

        if(producto_modificado):
            self.notebook.tab(self.edit, state="disabled")
            self.notebook.select(1)
            self.get_productosB()
            self.get_productos()

            self.labelMessageBus["text"] = "{} HA SIDO MODIFICADO CON EXITO".format(name)
            self.labelMessageBus["fg"] = "green"
        else:
            self.labelMessage["text"] = "PRODUCTO NO MODIFICADO. DEBE RELLANAR TODOS LOS ESPACIOS"
            self.labelMessage["fg"] = "red"

    def valid_user(self):
        valid_user = self.entryUser.get()
        return len(valid_user) != 0

    def valid_pwd(self):
        valid_pwd = self.entryPwd.get()
        return len(valid_pwd) != 0

    def valid_rol(self):
        valid_rol = self.rol.get()
        return len(valid_rol) != 0

    def add_user(self):

        if self.valid_user() and self.valid_pwd() and self.valid_rol():
            u = Users(self.entryUser.get(), self.entryPwd.get(), self.rol.get().lower())
            db.session.add(u)
            db.session.commit()
            db.session.close()

            self.messageUser["text"] = "EL USUARIO {} SE HA CREADO CON EXITO".format(self.entryUser.get().upper())
            self.messageUser["fg"] = "green"
            self.entryUser.delete(0, END)
            self.entryPwd.delete(0, END)
            self.entryConfrim.delete(0, END)
            self.rol.set("")

        elif self.entryPwd.get() != self.entryConfrim.get():
            self.messageUser["text"] = "LAS CONTRASEÑAS DEBEN COINCIDIR"
            self.messageUser["fg"] = "red"

        elif self.valid_user() == False and self.valid_pwd() and self.valid_rol():
            self.messageUser["text"] = "EL NOMBRE DE USUARIO ES OBLIGATORIO"
            self.messageUser["fg"] = "red"

        elif self.valid_pwd() == False and self.valid_user() and self.valid_rol():
            self.messageUser["text"] = "LA CONTRASEÑA ES OBLIGATORIA"
            self.messageUser["fg"] = "red"

        elif self.valid_rol() == False and self.valid_user() and self.valid_pwd():
            self.messageUser["text"] = "EL ROL ES OBLIGATORIO"
            self.messageUser["fg"] = "red"
        else:
            self.messageUser["text"] = "TODO LOS CAMPOS SON OBLIGATORIOS"
            self.messageUser["fg"] = "red"

        # ACTUALIZAR TABLA
        self.get_users()

    def get_users(self):
        registros_tabla = self.tablaUsers.get_children()  # Devuelve los valores que estan en la tabla
        for fila in registros_tabla:
            self.tablaUsers.delete(fila)

        query = "SELECT * FROM users ORDER BY id DESC"  # Consulta a la tabla productos
        registros = db.session.query(Users).from_statement(text(query))
        db.session.commit()
        db.session.close()

        for i in registros:
            self.tablaUsers.insert("", 0, text=i.name.upper(), values=[i.rol.upper()])

    def edit_users(self):
        try:
            self.tablaUsers.item(self.tablaUsers.selection())["text"][0]
        except IndexError as e:
            self.messageUser["text"] = "DEBE SELECCIONAR UN USUARIO"
            self.messageUser["fg"] = "red"
            return

        name = self.tablaUsers.item(self.tablaUsers.selection())["text"].lower()
        rol = self.tablaUsers.item(self.tablaUsers.selection())["values"][0].lower()
        row = db.session.query(Users).where(Users.name == name and Users.rol == rol).first()
        global passwdActual
        passwdActual = row.passwd

        self.winUserEdit = Toplevel()
        self.winUserEdit.geometry("400x500")
        self.winUserEdit.title("ADMINISTRADOR - EDITAR USUARIO")
        self.winUserEdit.focus()

        self.separatorEditUser = ttk.Separator(self.winUserEdit, orient="horizontal")
        self.separatorEditUser.grid(row=0, sticky=W + E, pady=10)

        self.labelTitleEditUser = Label(self.winUserEdit, text="EDITAR USUARIO", font = (20), width=45)
        self.labelTitleEditUser.grid(row=1, sticky= W + E, pady=10)

        self.separatorEditUser2 = ttk.Separator(self.winUserEdit, orient="horizontal")
        self.separatorEditUser2.grid(row=2, sticky= W + E, pady=10)

        self.labelUserEdit = Label(self.winUserEdit, text="USUARIO ", width=50)
        self.labelUserEdit.grid(row=3, column=0, pady=5)
        self.entryUserEdit = Entry(self.winUserEdit, textvariable=StringVar(self.winUserEdit, value=name), width=50, borderwidth=3)
        self.entryUserEdit.grid(row=4, column=0, pady=5)

        self.labelRolEdit = Label(self.winUserEdit, text="ROL DEL USUARIO", width=50)
        self.labelRolEdit.grid(row=5, column=0, pady=5)
        self.rolEdit = StringVar(self.winUserEdit)
        self.rolEdit.set(rol)
        self.entryRol = OptionMenu(self.winUserEdit, self.rolEdit, "ADMIN", "VENDEDOR", "CAJERO")
        self.entryRol.grid(row=6, column=0, pady=5)

        self.labelNewPass = Label(self.winUserEdit, text="NUEVA CONTRASEÑA")
        self.labelNewPass.grid(row=7, column=0, pady=5)
        self.entryNewPass = Entry(self.winUserEdit, width=50, borderwidth=3, show="*")
        self.entryNewPass.grid(row=8, column=0, pady=5)

        self.labelActualPass = Label(self.winUserEdit, text="CONTRASEÑA ACTUAL")
        self.labelActualPass.grid(row=9, column=0, pady=5)
        self.entryActualPass = Entry(self.winUserEdit, width=50, borderwidth=3, show="*")
        self.entryActualPass.grid(row=10, column=0, pady=5)

        self.separatorEditUser3 = ttk.Separator(self.winUserEdit, orient="horizontal")
        self.separatorEditUser3.grid(row=11, sticky= W + E, pady=10)

        self.buttonUpdateUser = ttk.Button(self.winUserEdit, text = "ACTUALIZAR", padding=10, width=50, command= lambda : self.update_users(self.entryUserEdit.get(), self.rolEdit.get(), self.entryNewPass.get(), self.entryActualPass.get(), passwdActual))
        self.buttonUpdateUser.grid(row=12, column=0, pady=10)

        self.separatorEditUser4 = ttk.Separator(self.winUserEdit, orient="horizontal")
        self.separatorEditUser4.grid(row=13, sticky= W + E, pady=10)

        global messageEditUser

        self.messageEditUser = Label(self.winUserEdit, text="")
        self.messageEditUser.grid(row=14, column=0, pady=5)

    def del_users(self):
        try:
            self.tablaUsers.item(self.tablaUsers.selection())["text"][0]
        except IndexError as e:
            self.messageUser["text"]="DEBE SELECCIONAR UN USUARIO"
            self.messageUser["fg"]="red"
            return

        name = self.tablaUsers.item(self.tablaUsers.selection())["text"].lower()

        db.session.query(Users).filter_by(name = name).delete()
        db.session.commit()
        db.session.close()

        self.messageUser["text"] = "EL USUARIO {} HA SIDO ELIMINADO CON EXITO!".format(name.upper())
        self.messageUser["fg"] = "red"

        self.get_users()

    def update_users(self, nameEdit, rolEdit, newPass, actualPass, passwdActual):
        userModificado = False

        name = self.tablaUsers.item(self.tablaUsers.selection())["text"].lower()

        if passwdActual == actualPass:

            if newPass == "":
                newPass = passwdActual

            db.session.query(Users).filter_by(name = name).update({"name": nameEdit, "passwd": newPass, "rol": rolEdit.lower()})
            db.session.commit()
            db.session.close()
            userModificado = True

        elif nameEdit == "" or rolEdit == "" or newPass == "" or actualPass == "":
            userModificado = False

        if userModificado:
            self.winUserEdit.destroy()
            self.messageUser["text"] = "USUARIO {} SE HA MODIFICADO CON EXITO".format(nameEdit.upper())
            self.messageUser["fg"] = "green"

        elif passwdActual != actualPass:
            self.messageEditUser["text"] = "LA CONTRASEÑA ACTUAL NO ES CORRECTA"
            self.messageEditUser["fg"] = "red"

        elif userModificado == False:
            self.messageEditUser["text"] = "USUARIO NO MODIFICADO, DEBE RELLENAR TODO LOS CAMPOS"
            self.messageEditUser["fg"] = "red"

        self.get_users()

class Salesman:

    db = "database/drugstore.db"

    def backLogin(self):
        changeApp(Login)

    def __init__(self, root):
        self.window = root
        self.window.title("FARMACIA LA PAC - VENDEDOR")
        self.window.geometry("1024x720")
        self.window.resizable(0, 0)

        #MENU BAR

        self.menu = Menu(root)
        root.config(menu=self.menu)
        self.admin_menu = Menu(self.menu, tearoff = 0)
        self.menu.add_cascade(label="VENDEDOR", menu=self.admin_menu)
        self.admin_menu.add_command(label="Cerrar sesión", command=self.backLogin)

        frameSaleman = LabelFrame(self.window, text="VENTA")
        frameSaleman.grid(row=0, column=0, pady=10, padx=10)

        self.labelCode = Label(frameSaleman, text="CÓDIGO: ")
        self.labelCode.grid(row=0, column =0, pady=10, padx=30)
        self.entryCode = Entry(frameSaleman, width=40, borderwidth=3)
        self.entryCode.grid(row=0, column=1, pady=10)

        self.labelCantidad = Label(frameSaleman, text="CANTIDAD: ")
        self.labelCantidad.grid(row=0, column=2, pady=10, padx=30)
        self.entryCantidad = Entry(frameSaleman, width=40, borderwidth=3)
        self.entryCantidad.insert(0, "1")
        self.entryCantidad.grid(row=0, column=3, pady=10)

        self.buttonFind = ttk.Button(frameSaleman, text="AGREGAR ARTICULO", width=30, padding=5, command=self.add)
        self.buttonFind.grid(row=0, column=4, pady=10, padx=30)

        self.buttonRemove = ttk.Button(frameSaleman, text="ELIMINAR ARTICULO", width=30, padding=5, command=self.remove)
        self.buttonRemove.grid(row=1, column=4, pady=10, padx=30)

        self.buttonRemove = ttk.Button(frameSaleman, text="TOTALIZAR CUENTA", width=30, padding=5, command=self.totalizar)
        self.buttonRemove.grid(row=2, column=4, pady=10, padx=30)

        self.tablaSale = ttk.Treeview(frameSaleman, height=10, columns=(1, 2, 3, 4, 5))
        self.tablaSale.grid(row = 3, column = 0, pady=10, padx=10, columnspan=5)
        self.tablaSale.heading("#0", text = "CODIGO")
        self.tablaSale.column("#0", width=200)
        self.tablaSale.heading("#1", text = "DESCRIPCION")
        self.tablaSale.column("#1", width=300)
        self.tablaSale.heading("#2", text = "STOCK")
        self.tablaSale.column("#2", width=80)
        self.tablaSale.heading("#3", text = "PRECIO")
        self.tablaSale.column("#3", width=150)
        self.tablaSale.heading("#4", text="CANTIDAD")
        self.tablaSale.column("#4", width=80)
        self.tablaSale.heading("#5", text="PRECIO FINAL")
        self.tablaSale.column("#5", width=150)

        frameSaleman2 = LabelFrame(self.window)
        frameSaleman2.grid(row=1, column=0, pady=10, padx=10, ipadx=10)
        self.labelTotal = Label(frameSaleman2, text="TOTAL VENTA:")
        self.labelTotal.grid(row = 0, column=0, pady=10, padx=30)
        self.entryTotal = Entry(frameSaleman2, width=40, state = DISABLED)
        self.entryTotal.grid(row=0, column=1, pady=10, padx=10, ipady=10)

        self.buttonTicket = ttk.Button(frameSaleman2, text="GENERAR TICKET", width=40, padding=10, command=self.ticket)
        self.buttonTicket.grid(row=0, column=3, pady=10, padx=10, columnspan=2)

        self.buttonCancel = ttk.Button(frameSaleman2, text="CANCELAR VENTA", width=40, padding=10, command=self.cancel)
        self.buttonCancel.grid(row=0, column=5, pady=10, padx=10, columnspan=2)

    def add(self):
        try:
            code = self.entryCode.get()
            p = db.session.query(Products).filter(Products.code == code).first()
            totalPrice = p.sale_price * int(self.entryCantidad.get())
            self.tablaSale.insert("", 0, text=p.code, values=[p.name.upper(), p.stock, p.sale_price, self.entryCantidad.get(), totalPrice])
            if p.stock <= 5:
                messagebox.showinfo(message = "EL PRODUCTO AGREGADO TIENE UN STOCK DE {} UNIDADES".format(p.stock), title = "ALERTA BAJO STOCK")
            self.entryCode.delete(0, END)
            self.entryCantidad.delete(0, END)
            self.entryCantidad.insert(0, "1")

        except AttributeError:
            print("PRODUCTO NO SE ENCUENTRA REGISTRADO")

    def remove(self):

        code = self.tablaSale.item(self.tablaSale.selection())["text"]
        registro = self.tablaSale.get_children()
        for i in registro:
            if self.tablaSale.item(i)["text"] == code:
                self.tablaSale.delete(i)

    def totalizar(self):
        sumaTotal = 0

        registros = self.tablaSale.get_children()
        for i in registros:
            sumaTotal += float(self.tablaSale.item(i)["values"][4])
            print(sumaTotal)

        self.entryTotal["state"] = NORMAL
        self.entryTotal.delete(0, END)
        self.entryTotal.insert(END, sumaTotal)
        self.entryTotal["state"] = DISABLED

    def ticket(self):
        total = 0
        registros = self.tablaSale.get_children()
        with open("tickets/ticket.txt", "w") as f:
            f.write("= = = = = = = = = = = = = = = = = = = = = = = = = = = =")
            f.write("\n- 	     F A R M A C I A * L A * P A C            -")
            f.write("\n= = = = = = = = = = = = = = = = = = = = = = = = = = = =")
            f.write("\n        direccion:Av. Club Hipico #2576 - Local 4      ")
            f.write("\n	           tel: +56992789314                   ")
            f.write("\n= = = = = = = = = = = = = = = = = = = = = = = = = = = =")
            f.write("\n            T I C K E T * D E * C O M P R A            ")
            f.write("\n= = = = = = = = = = = = = = = = = = = = = = = = = = = =")
            f.write("\ncant desc 					 precio\n")

            for i in registros:
                f.write("\n " + str(self.tablaSale.item(i)["values"][3]) + "    " + self.tablaSale.item(i)["values"][0].lower() + "\t\t\t\t" + "$" + str(self.tablaSale.item(i)["values"][4]))
                total += float(self.tablaSale.item(i)["values"][4])
            f.write("\n")
            f.write("\n= = = = = = = = = = = = = = = = = = = = = = = = = = = =")
            f.write("\nTOTAL				$" + str(total))
            f.write("\n\n= = = = = = = = = = = = = = = = = = = = = = = = = = = =")
            f.write("\n      G R A C I A S * P O R * T U * C O M P R A !")
            f.write("\n")

        self.showTicket = Toplevel()
        self.showTicket.geometry("480x750")
        self.showTicket.title("VENDEDOR - TICKET")
        self.showTicket.focus()

        self.ticket = Text(self.showTicket, width = 55, height = 35, borderwidth=3, font=("Consolas", 11))
        self.ticket.grid(row=0, column=0, pady = 10, padx = 14, sticky = W + E)

        self.buttomAccept = ttk.Button(self.showTicket, text = "ACEPTAR", padding = 10,  command = self.addTicket)
        self.buttomAccept.grid(row = 1, column = 0, pady = 10, padx = 14, sticky = W + E )

        with open("tickets/ticket.txt", "r", encoding="UTF-8") as f:
            lines = f.read()
            self.ticket.insert(END, lines)

        global numticket

        query = "SELECT * FROM tickets ORDER BY id DESC"
        numticket = db.session.query(Tickets).from_statement(text(query)).first()
        numticket = numticket.numticket
        db.session.commit()

        numticket+=1

        number = numticket
        my_code = EAN13(str(number), writer=ImageWriter())
        my_code.save("tickets/codebar", {"dpi":250})

        global codebar

        codebar = PhotoImage(file="tickets/codebar.png")
        self.ticket.image_create(END, image=codebar)

    def cancel(self):
        registros = self.tablaSale.get_children()

        for i in registros:
            self.tablaSale.delete(i)

        self.entryCode.delete(0, END)
        self.entryCantidad.delete(0, END)
        self.entryCantidad.insert(END, 1)
        self.entryTotal["state"] = NORMAL
        self.entryTotal.delete(0, END)
        self.entryTotal["state"] = DISABLED

    def addTicket(self):

        registros = self.tablaSale.get_children()

        for i in registros:
            t = Tickets(numticket, self.tablaSale.item(i)["text"], self.tablaSale.item(i)["values"][3], self.tablaSale.item(i)["values"][0], self.tablaSale.item(i)["values"][2], self.tablaSale.item(i)["values"][4], paid = False)
            db.session.add(t)
            db.session.commit()
            db.session.close()

        self.showTicket.destroy()
        self.cancel()

class Checker:

    db = "database/drugstore.db"

    def backLogin(self):
        changeApp(Login)

    def __init__(self, root):
        self.window = root
        self.window.title("FARMACIA LA PAC - CAJERO")
        self.window.geometry("1024x720")
        self.window.resizable(0, 0)

        #MENUBAR

        self.menu = Menu(root)
        root.config(menu=self.menu)
        self.admin_menu = Menu(self.menu, tearoff = 0)
        self.menu.add_cascade(label="CAJERO", menu=self.admin_menu)
        self.admin_menu.add_command(label="Cerrar sesión", command=self.backLogin)

        self.ticketFrame = LabelFrame(self.window, text = "BUSCAR")
        self.ticketFrame.grid(row=0, column=0, pady=10, padx=15, ipadx=20)

        self.labelTicket = Label(self.ticketFrame, text = "TICKET: ")
        self.labelTicket.focus()
        self.labelTicket.grid(row=0, column=0, pady=10, padx=10)
        self.entryTicket = Entry(self.ticketFrame, width=60, borderwidth=3)
        self.entryTicket.grid(row=0, column=1, pady=10, padx=10)
        self.buttonTicket = ttk.Button(self.ticketFrame, text="BUSCAR TICKET", width=35, padding=5, command=self.search)
        self.buttonTicket.grid(row=0, column=2, pady=10, padx=10)
        self.buttonCancel = ttk.Button(self.ticketFrame, text="ELIMINAR BUSQUEDA", width=35, padding=5, command=self.cancelSearch)
        self.buttonCancel.grid(row=0, column=3, pady=10, padx=10)
        self.labelStatus = Label(self.ticketFrame, text="ESTADO: ")
        self.labelStatus.grid(row=1, column=0, pady=10)
        self.entryStatus = Entry(self.ticketFrame, width=30, borderwidth=3)
        self.entryStatus.grid(row=1, column=1, pady=10, padx=10, sticky = W)

        self.elementFrame = LabelFrame(self.window, text = "LISTA DE ELEMENTOS")
        self.elementFrame.grid(row=1, column=0, pady=10, padx=10)

        self.tablaCheker = ttk.Treeview(self.elementFrame, height=10, columns=(1,2,3,4))
        self.tablaCheker.grid(row=0, column=0, pady=10, padx=10)
        self.tablaCheker.heading("#0", text="CODIGO")
        self.tablaCheker.column("#0", width=200)
        self.tablaCheker.heading("#1", text="DESCRIPCION")
        self.tablaCheker.column("#1", width=310)
        self.tablaCheker.heading("#2", text="PRECIO")
        self.tablaCheker.column("#2", width=180)
        self.tablaCheker.heading("#3", text="CANTIDAD")
        self.tablaCheker.column("#3", width=100)
        self.tablaCheker.heading("#4", text="PRECIO FINAL")
        self.tablaCheker.column("#4", width=180)

        self.payFrame = LabelFrame(self.window, text="PAGAR")
        self.payFrame.grid(row=2, column=0, pady=10, padx=10)

        self.totalLabel = Label(self.payFrame, text="TOTAL DE LA VENTA")
        self.totalLabel.grid(row=0, column=0, pady=10, padx=10)
        self.entryTotal = Entry(self.payFrame, width=40, borderwidth=3, state=DISABLED)
        self.entryTotal.grid(row=0, column=1, pady=10, padx=10, ipady=5)

        self.paidLabel = Label(self.payFrame, text="PAGA CON")
        self.paidLabel.grid(row=1, column=0, pady=10, padx=10)
        self.entryPaid = Entry(self.payFrame, width=40, borderwidth=3)
        self.entryPaid.grid(row=1, column=1, pady=10, padx=10, ipady=5)

        self.changeLabel = Label(self.payFrame, text="VUELTO")
        self.changeLabel.grid(row=2, column=0, pady=10, padx=10)
        self.entryChange = Entry(self.payFrame, width=40, borderwidth=3, state=DISABLED)
        self.entryChange.grid(row=2, column=1, pady=10, padx=10, ipady=5)

        self.paidButton = ttk.Button(self.payFrame, text="PAGAR CUENTA", padding=10, width=40, command=self.paid)
        self.paidButton.grid(row=1, column=3, pady=10, padx=162)

    def search(self):
        try:
            ticket = self.entryTicket.get()
            total = 0
            registros = db.session.query(Tickets).where(Tickets.numticket == ticket).all()

            for i in registros:
                self.tablaCheker.insert("", 0, text=i.code, values=[i.desc.upper(), i.price, i.cant, i.totalprice])
                total += i.totalprice
                status = i.paid

            if status == 1:
                self.entryStatus.insert(END, "PAGADO")
                self.entryStatus["fg"] = "green"

            elif status == 0:

                self.entryStatus.insert(END, "NO PAGADO")
                self.entryStatus["fg"] = "red"

            self.entryTotal["state"] = NORMAL
            self.entryTotal.insert(END, total)
            self.entryTotal["state"] = DISABLED
        except UnboundLocalError:
            messagebox.showerror(title="ERROR TICKET", message="EL TICKET INGRESADO NO SE ENCUENTRA")

    def cancelSearch(self):

        registros = self.tablaCheker.get_children()

        for i in registros:
            self.tablaCheker.delete(i)

        self.entryTicket.delete(0, END)
        self.entryStatus.delete(0, END)
        self.entryPaid.delete(0, END)
        self.entryTotal["state"] = NORMAL
        self.entryTotal.delete(0, END)
        self.entryTotal["state"] = DISABLED
        self.entryChange["state"] = NORMAL
        self.entryChange.delete(0, END)
        self.entryChange["state"] = DISABLED


    def paid(self):

        total = float(self.entryTotal.get())
        pago = float(self.entryPaid.get())
        ticket = self.entryTicket.get()
        sobrante = pago - total

        self.entryChange["state"] = NORMAL
        self.entryChange.insert(END, sobrante)
        self.entryChange["state"] = DISABLED

        db.session.query(Tickets).where(Tickets.numticket == ticket).update({"paid": 1})

        registrosTi = db.session.query(Tickets).where(Tickets.numticket == ticket).all()

        for i in registrosTi:

            if i.paid == 1:
                cant = i.cant
                code = i.code
                pro = db.session.query(Products).where(Products.code == code).first()
                cantPro = pro.stock
                newstock = cantPro - cant
                db.session.query(Products).where(Products.code == code).update({"stock": newstock})

        db.session.commit()
        db.session.close()

        messagebox.showinfo(message="PAGO REALIZADO CON EXITO!", title="INFORMACION")

        self.cancelSearch()

if __name__ == "__main__":

    def app(window):
        global root
        root = Tk()
        app = window(root)
        root.mainloop()

    def changeApp(window):
        root.destroy()
        app(window)

    db.Base.metadata.create_all(db.engine)
    app(Login)
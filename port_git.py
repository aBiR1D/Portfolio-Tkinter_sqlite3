#Import Requird Libraries

from tkinter import *
from tkinter import messagebox, Menu
import requests
import json
import sqlite3

con = sqlite3.connect("coin.db")
cObj = con.cursor()

cObj.execute("CREATE TABLE IF NOT EXISTS coin(id INTEGER PRIMARY KEY, name STR, quantity REAL, price REAL)")
con.commit()

def reset():
    for cells in crypto.winfo_children():
        cells.destroy()
        
    nav()
    coin_header()
    my_portfolio()
    
def nav():
    
    def clear_all():
        cObj.execute("DELETE FROM coin")
        con.commit()
        
        reset()
        messagebox.showinfo("Please Note","All coins has been deleted. Please Add New Coins!")
        
    def close_app():
        crypto.destroy()
        
    
    menu = Menu(crypto)
    file_item = Menu(menu)
    file_item.add_command(label = "Clear Portfolio",command = clear_all)
    file_item.add_command(label = "Close App",command = close_app)
    menu.add_cascade(label = "File",menu = file_item)
    
    crypto.config(menu = menu)
    
    
def my_portfolio():
    api_request = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=60&convert=INR&CMC_PRO_API_KEY='YOUR_API_KEY'") #Insert your Api Key

    api = json.loads(api_request.content)
    
    def font_colour(amount):
        if amount > 0 :
            return "green"
        elif amount == 0:
            return "white"
        else:
            return "red"
    
    def get_values():
        cObj.execute("INSERT INTO coin(name, quantity, price) VALUES(?, ?, ?)", (sym_text.get(),sym_quantity.get(), sym_price.get()))
        con.commit()
        reset()
        messagebox.showinfo("Please Note", "Coin has been added!")
        
    def update_values():
        cObj.execute("UPDATE coin SET name = ?, quantity = ?, price = ? WHERE id = ?", (upd_text.get(),upd_quantity.get(), upd_price.get(), uid.get()))
        con.commit()
        reset()
        messagebox.showinfo("Please Note", "Coin has been modified!")
    
    def delete_values():
        cObj.execute("DELETE from coin WHERE id =?", (did.get(),))
        con.commit()
        reset()
        messagebox.showinfo("Please Note", "Coin has been deleted!")
    
    
    cObj.execute("SELECT * FROM coin")
    coins = cObj.fetchall()


    s= []
    coin_row = 1
    total_paid = 0
    total_value = 0

    for i in range(0,60): 
        for coin in coins:
            if api["data"][i]["symbol"] == coin[1]:
                               
                diff = api["data"][i]["quote"]["INR"]["price"]*coin[2] - coin[2]*coin[3]
                total_paid = total_paid + coin[2] * coin[3]
                
                p_id = Label(crypto, text = coin[0],bg = "#00BFFF", fg = "white", font = "Lato 12 bold", padx = "5", pady = "5", borderwidth = 3, relief = "groove")
                p_id.grid(column = 0, row = coin_row, sticky = N+S+E+W)
                
                name = Label(crypto, text = api["data"][i]["symbol"],bg = "#00BFFF", fg = "white", font = "Lato 12 bold", padx = "5", pady = "5", borderwidth = 3, relief = "groove")
                name.grid(column = 1, row = coin_row, sticky = N+S+E+W)

                qty = Label(crypto, text = "{0:.2f}".format(coin[2]),bg = "#00BFFF", fg = "white", font = "Lato 12 bold", padx = "5", pady = "5", borderwidth = 3, relief = "groove")
                qty.grid(column = 2, row = coin_row, sticky = N+S+E+W)

                a_paid = Label(crypto, text = "Rs.{0:.2f}".format(coin[2] * coin[3]),bg = "#00BFFF", fg = "white", font = "Lato 12 bold", padx = "5", pady = "5", borderwidth = 3, relief = "groove")
                a_paid.grid(column = 3, row = coin_row, sticky = N+S+E+W)

                c_val = Label(crypto, text = "Rs.{0:.2f}".format(api["data"][i]["quote"]["INR"]["price"]*coin[2]),bg = "#00BFFF", fg = "white", font = "Lato 12 bold", padx = "5", pady = "5", borderwidth = 3, relief = "groove")
                c_val.grid(column = 4, row = coin_row, sticky = N+S+E+W)

                pl = Label(crypto, text ="Rs.{0:.2f}".format(diff),bg = "#00BFFF", fg = font_colour(float(diff)), font = "Lato 12 bold", padx = "5", pady = "5", borderwidth = 3, relief = "groove")
                pl.grid(column = 5, row = coin_row, sticky = N+S+E+W)
                
                coin_row +=1
                total_value += api["data"][i]["quote"]["INR"]["price"]*coin[2]
                
                s.append(diff)
   
    #INSERT COIN
    sym_text = Entry(crypto, borderwidth=3,relief="solid")
    sym_text.grid(column = 1, row = coin_row+1)
    
    sym_price= Entry(crypto, borderwidth=3, relief="solid")
    sym_price.grid(column=4, row = coin_row+1)
    
    sym_quantity = Entry(crypto, borderwidth=3, relief="solid")
    sym_quantity.grid(column=2, row = coin_row+1)
    
    add_coin = Button(crypto, text = "ADD COIN",bg = "white", fg = "black", command = get_values, font = "Lato 12 bold", padx = "5", pady = "5", borderwidth = 3, relief = "groove")
    add_coin.grid(column = 3, row = coin_row+1, sticky = N+S+E+W)
    
    #UPDATE COIN
    upd_text = Entry(crypto, borderwidth=3,relief="solid")
    upd_text.grid(column = 1, row = coin_row+2)
    
    upd_price= Entry(crypto, borderwidth=3, relief="solid")
    upd_price.grid(column=4, row = coin_row+2)
    
    upd_quantity = Entry(crypto, borderwidth=3, relief="solid")
    upd_quantity.grid(column=2, row = coin_row+2)
    
    uid = Entry(crypto, borderwidth=3, relief="solid")
    uid.grid(column=0,row=coin_row+2)
    
    upd_coin = Button(crypto, text = "UPDATE COIN",bg = "white", fg = "black", command = update_values, font = "Lato 12 bold", padx = "5", pady = "5", borderwidth = 3, relief = "groove")
    upd_coin.grid(column = 3, row = coin_row+2, sticky = N+S+E+W)
    
    #DELETE COIN
    did = Entry(crypto, borderwidth=3, relief="solid")
    did.grid(column = 0, row = coin_row+3)
    
    del_coin = Button(crypto, text = "DELETE COIN",bg = "white", fg = "black", command = delete_values, font = "Lato 12 bold", padx = "5", pady = "5", borderwidth = 3, relief = "groove")
    del_coin.grid(column = 3, row = coin_row+3, sticky = N+S+E+W)
    
    
    tamp = Label(crypto, text ="Rs.{0:.2f}".format(total_paid),bg = "#00BFFF", fg = "white", font = "Lato 12 bold", padx = "5", pady = "5", borderwidth = 3, relief = "groove")
    tamp.grid(column = 3, row = coin_row, sticky = N+S+E+W)
    
    tcv = Label(crypto, text ="Rs.{0:.2f}".format(total_value),bg = "#00BFFF", fg = "white", font = "Lato 12 bold", padx = "5", pady = "5", borderwidth = 3, relief = "groove")
    tcv.grid(column = 4, row = coin_row, sticky = N+S+E+W)
    
    tpl = Label(crypto, text = "Rs.{0:.2f}".format(sum(s)),bg = "#00BFFF", fg = font_colour(float(sum(s))), font = "Lato 12 bold", padx = "5", pady = "5", borderwidth = 3, relief = "groove")
    tpl.grid(column = 5, row = coin_row, sticky = N+S+E+W)
    
    
    
    api = "" 
    
    updt = Button(crypto, text = "REFRESH", bg ="white", fg = 'black', command = reset, font = "Lato 12 bold", padx = "5", pady = "5", borderwidth = 3, relief = "groove")
    updt.grid(column = 5, row = coin_row+1, sticky = N+S+E+W)
    
    
crypto = Tk()
crypto.title("My Portfolio")


def coin_header():
    
    id = Label(crypto, text = "ID",bg = "#FF10F0", fg = "#44FF77", font = "Lato 12 bold", padx = "5", pady = "5", borderwidth = 3, relief = "groove")
    id.grid(column = 0, row = 0, sticky = N+S+E+W)
    
    name = Label(crypto, text = "Coin Name",bg = "#FF10F0", fg = "#44FF77", font = "Lato 12 bold", padx = "5", pady = "5", borderwidth = 3, relief = "groove")
    name.grid(column = 1, row = 0, sticky = N+S+E+W)

    qty = Label(crypto, text = "Qty.",bg = "#FF10F0", fg = "#44FF77", font = "Lato 12 bold", padx = "5", pady = "5", borderwidth = 3, relief = "groove")
    qty.grid(column = 2, row = 0, sticky = N+S+E+W)

    a_paid = Label(crypto, text = "Amt. Invested",bg = "#FF10F0", fg = "#44FF77", font = "Lato 12 bold", padx = "5", pady = "5", borderwidth = 3, relief = "groove")
    a_paid.grid(column = 3, row = 0, sticky = N+S+E+W)

    c_val = Label(crypto, text = "Current Value",bg = "#FF10F0", fg = "#44FF77", font = "Lato 12 bold", padx = "5", pady = "5", borderwidth = 3, relief = "groove")
    c_val.grid(column = 4, row = 0, sticky = N+S+E+W)

    pl = Label(crypto, text = "Position",bg = "#FF10F0", fg = "#44FF77", font = "Lato 12 bold", padx = "5", pady = "5", borderwidth = 3, relief = "groove")
    pl.grid(column = 5, row = 0, sticky = N+S+E+W)
    
    
nav()    
coin_header()

my_portfolio()

crypto.mainloop()

cObj.close()
con.close()
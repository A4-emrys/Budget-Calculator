import tkinter as tk
import math
from fpdf import FPDF
import time
from tkinter import messagebox


window = tk.Tk()
window.title('BUDGET CALCULATOR')
window.geometry('655x600')
window.resizable(width=False, height=False)


#============================== NAMING TITLE ===================================
lab = tk.Label(text='BUDGET CALCULATOR',relief='groove', bd=0.7, font=('times new roman',20,'bold'))
lab.pack(fill='x')

#============================= BUILDING A FRAME =============================================

lab_frame = tk.Frame(bd=4, relief='ridge', width=300, height=540)
lab_frame.place(x=20, y=48)

#============================= SHOVING LABELS AND ENTRIES INTO THE MY FRAME ============================

lab1 = tk.Label(lab_frame,text='Please enter your salary a month:', fon=('times new roman',13), padx=20)
lab1.place(x=5, y=5)

lab2 = tk.Label(lab_frame, text='GHC', font=('times new roman',14,'bold'))
lab2.place(x=5, y=35)

lab2_entry = tk.Entry(lab_frame, font=('roboto',13))
lab2_entry.place(x=62, y=35)
lab2_entry.focus()

lab3 = tk.Label(lab_frame, text='name each item you are spending on', fg='red' ,font=('roboto',11), padx=20)
lab3.place(y=100)
lab4 = tk.Label(lab_frame, text='with the prices attached.',fg='red', font=('roboto',11), padx=50)
lab4.place(y=125)

item_lab = tk.Label(lab_frame,text='Item', font=('roboto',11), padx=20)
item_lab.place(x=20, y=175)

item_price = tk.Label(lab_frame,text='Price', font=('roboto',11), padx=20)
item_price.place(x=187, y=175)

item1 = tk.Entry(lab_frame, font=('roboto', 11), width=10)
item1.place(x=20, y=200)

item1_price = tk.Entry(lab_frame, font=('roboto', 11), width=10)
item1_price.place(x=187, y=200)


item2 = tk.Entry(lab_frame, font=('roboto', 11), width=10)
item2.place(x=20, y=250)

item2_price = tk.Entry(lab_frame, font=('roboto', 11), width=10)
item2_price.place(x=187, y=250)

item3 = tk.Entry(lab_frame, font=('roboto', 11), width=10)
item3.place(x=20, y=300)

item3_price = tk.Entry(lab_frame, font=('roboto', 11), width=10)
item3_price.place(x=187, y=300)

#======================================== BUTTON FRAME ===============================================
button_frame = tk.Frame(lab_frame, width=270, height=80, bd=3, relief='ridge')
button_frame.place(x=10,y=440)


#======================================= BULDING A BUTTON INSIDE THE BUTTONFRAME ===================================
button_cal = tk.Button(button_frame, text='CALCULATE', fg='white', bg='green',font=('times new roman', 15), width=15, command=lambda:calc())
button_cal.place(x=45, y=17)


#========================================= DEFINING MY BUTTON =======================================================
def calc():


    global head_lab
    global result

    if lab2_entry.get() == '':
        lab2_entry.focus()
        messagebox.showerror('ERROR', '* field required')

    elif  item1.get() == '':
        item1.focus()
        messagebox.showerror('ERROR', '* field required')

    elif  item1_price.get() == '':
        item1_price.focus()
        messagebox.showerror('ERROR', '* field required')

    elif item2.get() == '':
        item2.focus()
        messagebox.showerror('ERROR', '* field required')

    elif item2_price.get() == '':
        item2_price.focus()
        messagebox.showerror('ERROR', '* field required')

    elif item3.get() == '':
        item3.focus()
        messagebox.showerror('ERROR', '* field required')

    elif item3_price.get() == '':
        item3_price.focus()
        messagebox.showerror('ERROR', '* field required')
    else:


        head_lab = tk.Label(window, text='Calculation done!', font=('times new roman',18,'bold'))
        head_lab.place(x=400, y=72)

        item1_lab = tk.Label(window, text='✔  ' + item1.get() + '  =       ', font=('times new roman',13))
        item1_lab.place(x=350, y=142)

        itemlab_price = tk.Label(window, text='GHC ' + item1_price.get(), font=('times new roman',13))
        itemlab_price.place(x=480, y=142)

        item2_lab = tk.Label(window, text='✔  ' + item2.get() + '   =       ', font=('times new roman', 13))
        item2_lab.place(x=350, y=185)

        item2lab_price = tk.Label(window, text='GHC ' + item2_price.get(), font=('times new roman', 13))
        item2lab_price.place(x=470, y=186)

        item3_lab = tk.Label(window, text = '✔  ' + item3.get() + '   =       ', font=('times new roman',13,))
        item3_lab.place(x=350, y=240)

        item3lab_price = tk.Label(window, text='GHC ' + item3_price.get(), font=('times new roman',13,))
        item3lab_price.place(x=480, y=240)



    #============================================= CALCULATIONS =======================================================

        num1 = int(item1_price.get())
        num2 = int(item2_price.get())
        num3 = int(item3_price.get())

        total = num1 + num2 + num3
        answer = tk.Label(window, text=total, font=('times new roman', 15, 'bold'))
        answer.place(x=490, y=295)

        total_lab = tk.Label(text='Total      GHC ', font=('times new roman', 15, 'bold'))
        total_lab.place(x=355, y=295)

        lablab = tk.Label(text= 'Your remaining balance is: ', font=('roboto',13,'bold'))
        lablab.place(x=350, y=395)


        num = int(lab2_entry.get())
        result = num - total
        result = tk.Label(text= result, fg='green',font=('times new roman', 14,'bold'))
        result.place(x=487, y=419)

        amount = tk.Label(text='GHC ', fg='green', font=('times new roman',14,'bold'))
        amount.place(x=418, y=419)

    #=================================== BUILDING A BUTTON =====================================================
        button_clear = tk.Button(text='Clear', fg='red', width=6, bd=3, font=('roboto',10, 'bold'), command=lambda: clear())
        button_clear.place(y=520, x=418)

        button_print = tk.Button(text='Print', bd=3, width=6, font=('roboto',10, 'bold'), command=lambda:prnt())
        button_print.place(y=520, x=510)

        


    #========================================== CREATING A FUNCTION FOR BUTTON ================================
        def clear():


            head_lab.destroy()
            item1_lab.destroy()
            item2_lab.destroy()
            item3_lab.destroy()
            itemlab_price.destroy()
            item2lab_price.destroy()
            item3lab_price.destroy()
            answer.destroy()
            total_lab.destroy()
            lablab.destroy()
            result.destroy()
            amount.destroy()
            button_print.destroy()
            button_clear.destroy()
            item1.delete(0,20)
            item1_price.delete(0,50)
            item2.delete(0,20)
            item2_price.delete(0,50)
            item3.delete(0,20)
            item3_price.delete(0,50)
            lab2_entry.delete(0,100)
            lab2_entry.focus()
            no_entry = tk.Label(text='No entry',padx=4, font=('roboto',12))
            no_entry.place(x=442, y=188)

    #==================================== GENERATING A PDF FILE ================================================
        def prnt():
            pdf = FPDF('P', 'mm', 'A5')

            #add page
            pdf.add_page()

            pdf.set_font('helvetica', 'BU', 16)
            pdf.set_text_color(20,6,12)
            pdf.cell(77,10, 'ITEMS')
            pdf.set_font('helvetica', 'BU', 16)
            pdf.cell(5,10, 'PRICE TAGS', ln=1)
            pdf.set_font_size(11)
            pdf.set_font('helvetica')
            pdf.cell(77,10,item1.get(),)
            # pdf.set_font('helvetica',13)
            pdf.cell(5,10, 'GHC '+ item1_price.get() + '.00',ln=1)
            pdf.cell(77,10, item2.get())
            pdf.cell(5,10, 'GHC ' + item2_price.get() + '.00', ln=1)
            pdf.cell(77,10, item3.get())
            pdf.cell(5,10, 'GHC ' + item3_price.get() + '.00',ln=1)
            pdf.set_text_color(10,6,12)
            pdf.set_font('helvetica')
            pdf.set_font_size(11)
            pdf.cell(68,5, 'Thanks for using our Budget Calculator.', ln=1)
            pdf.cell(68,5, 'Have a nice day and we hope to see you again.')
            pdf.output('budget_receipt.pdf')



window.mainloop()
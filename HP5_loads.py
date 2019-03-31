import os, shutil
from tkinter import *
from time import sleep


def replace_save(event):
    if mode=="load":
        try:
            os.remove(base_path+base_save)
        except:
            pass
        buttnr=event.widget
        for savenr in range(0,len(save_buttons)):
            if str(buttnr) == str(save_buttons[savenr]):
                nr=savenr
                break
        shutil.copy(base_path+saves[nr],base_path+base_save)
        add_save.config(text="Add save file")
    elif mode=="delete":
        buttnr=event.widget
        for savenr in range(0,len(save_buttons)):
            if str(buttnr) == str(save_buttons[savenr]):
                nr=savenr
                break
        os.remove(base_path+saves[nr])
        while len(save_buttons)>0:
            save_buttons[-1].destroy()
            save_buttons.pop(-1)
        buttons()
    


def change_user():
    global current_user, base_path
    new_user=user_txt.get()
    if new_user!=current_user and new_user!='' and new_user!=' ':
        base_path=base_path.replace(current_user,new_user)
        current_user=new_user
        curr_user.config(text="Current username: "+current_user)
        
        while len(save_buttons)>0:
            save_buttons[-1].destroy()
            save_buttons.pop(-1)
        buttons()

    
def buttons():
    global saves
    saves=[]
##    try:
##        os.remove(base_path+base_save)
##    except:
##        pass
    try:
        for r, d, f in os.walk(base_path):
            for file in f:
                file=file.replace("HPOOTP",base_save)
                saves.append(os.path.join(file))
    except:
        pass
    if len(saves)==0:
        if len(ns)==0:
            ns.append(Label(okno, text='no saves found'))
        ns[0].pack()
    else:
        saves.pop(0)
        try:
            ns[0].destroy()
            ns.pop(0)
        except:
            pass
        for save in saves:
            if save==base_save:
                continue
            else:
                save_buttons.append(Button(okno, text=save.replace(base_save,""),bg="white",width="30"))
            save_buttons[-1].bind("<Button-1>",replace_save)
            save_buttons[-1].pack()


def new_save():
    if os.path.isfile(base_path+base_save):
        if add_save_name.get()=='' or add_save_name.get()==' ':
            for i in range(0,100):
                if os.path.isfile(base_path+base_save+' '+str(i)):
                    continue
                else:
                    break
            name=str(i)
        else:
            name=add_save_name.get()
        shutil.copy(base_path+base_save,base_path+base_save+' '+name)
        while len(save_buttons)>0:
            save_buttons[-1].destroy()
            save_buttons.pop(-1)
        buttons()
    else:
        add_save.config(text="There's no file to save")


def bg_c():
    if mode=='load':
        return 'dark green'
    elif mode=='delete':
        return 'dark red'

def mode_change():
    global mode, mode_butt
    if mode=='load':
        mode='delete'
    else:
        mode='load'
    mode_butt.config(text="mode: "+mode,bg=bg_c())


base_path=r"C:\Users\Marek\AppData\Local\Electronic Arts\Harry Potter and the Order of the Phoenix\HPOOTP"
base_save=r"\HPOOTP"
#saves=['\HPOOTP 12%', '\HPOOTP bench skip train', '\HPOOTP crash', '\HPOOTP endgame', '\HPOOTP heavy tested mid', '\HPOOTP last parts', '\HPOOTP mid game', '\HPOOTP sam start']
saves=[]
modes=['load','delete']
mode = 'load'
current_user=base_path.split("\\")[2]
ns=[]
##for i in range(0,len(saves)):
##    print(i+1,': ',saves[i].replace(base_save,""))
##nr=int(input("chose save: "))-1
##
##print()
##shutil.copy(base_path+saves[nr],base_path+base_save)

okno=Tk("HP5 saves")

curr_user=Label(okno, text="Current username: "+current_user)
curr_user.pack()
user_txt=Entry(okno, width="30")
user_txt.pack()
Button(okno, text="Change user", width="20", command=change_user, bg="dark grey", fg="white").pack()

Label(okno, height="1").pack()

add_save_name=Entry(okno, width='30', bg='light blue')
add_save_name.pack()
add_save=Button(okno, text="Add save file", width="30", bg="light blue", command=new_save)
add_save.pack()
mode_butt=Button(okno, text="mode: "+mode, width='20', fg='white', bg=bg_c(), command=mode_change)
mode_butt.pack()
Label(text="Chose save file:").pack()
save_buttons=[]
buttons()

okno.mainloop()

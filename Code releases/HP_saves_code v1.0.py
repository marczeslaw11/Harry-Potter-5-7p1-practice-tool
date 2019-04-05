import os, shutil
from tkinter import *
from time import sleep


def replace_save(event):
    global add_save
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
    
    
def buttons():
    global saves, add_save, add_save_name, mode_butt, saves_list, resource_butt
    if len(additions)==0:
        try:
            additions.pop(additions.index(resource_butt))
            resource_butt.destroy()
        except:
            pass
        add_save_name=Entry(okno, width='30', bg='light blue')
        add_save_name.pack()
        additions.append(add_save_name)
        add_save=Button(okno, text="Add save file", width="30", bg="light blue", command=new_save)
        add_save.pack()
        additions.append(add_save)
        mode_butt=Button(okno, text="mode: "+mode, width='20', fg='white', bg=bg_c(), command=mode_change)
        mode_butt.pack()
        additions.append(mode_butt)
        try:
            missing_game.destroy()
        except:
            pass
        if os.path.isdir(os.path.realpath("Resources")+"\\"+games[base_game]):
            resource_butt=Button(okno, text="load save pack", command=unpack, width="20",bg="dark blue",fg="yellow")
            resource_butt.pack()
            additions.append(resource_butt)
        saves_list=Label(text="Chose save file:")
        saves_list.pack()
        additions.append(saves_list)

    saves=[]
    try:
        for r, d, f in os.walk(base_path):
            for file in f:
                if str(file)!="config":
                    saves.append(os.path.join(file))
    except:
        pass
    try:
        if saves[0]==base_save:
            saves.pop(0)
    except:
        pass
    if len(saves)==0:
        if len(ns)==0:
            ns.append(Label(okno, text='no saves found'))
        ns[0].pack()
    else:
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


def change_game():
    def sub_change(event):
        global base_game, base_save, base_path, resource_butt
        try:
            additions.pop(additions.index(resource_butt))
            resource_butt.destroy()
        except:
            pass
        if os.path.isdir(os.path.realpath("Resources")+"\\"+games[base_game]):
            resource_butt=Button(okno, text="Load save pack", command=unpack, width="20",bg="dark blue",fg="yellow")
            resource_butt.pack()
            additions.append(resource_butt)
        x=game_butts.index(event.widget)        
        base_game=game_paths[x]
        base_save=save_files[base_game]
        base_path=EA_path+base_game
        curr_game.config(text="Current game: "+games[base_game])
        while len(save_buttons)>0:
            save_buttons[-1].destroy()
            save_buttons.pop(-1)
        while len(additions)>0:
            additions[0].destroy()
            additions.pop(0)
        if os.path.isdir(base_path):
            buttons()
        else:
            missing() 
        av_games.destroy()
    
    av_games=Tk()
    game_butts=[]
    for i in games:
        game_butts.append(Button(av_games, text=games[i], width="20"))
        game_butts[-1].bind("<Button-1>",sub_change)
        game_butts[-1].pack()
    av_games.mainloop()


def missing():
    global missing_game
    try:
        missing_game.destroy()
    except:
        pass
    while len(additions)>0:
        additions[0].destroy()
        additions.pop(0)
    missing_game=Label(okno, text="Game folder not found",height="5",width='31')
    missing_game.pack()

    
def unpack():
    global resource_butt
    indicator=False
    for r,d,f in os.walk(os.path.realpath("Resources")+"\\"+games[base_game]):
        for file in f:
            indicator=True
            shutil.copy(os.path.realpath("Resources")+"\\"+games[base_game]+"\\"+str(file), base_path+str(file))
    if not indicator:
        resource_butt.config(text="Resource folder is empty")
        return
    while len(save_buttons)>0:
        save_buttons[-1].destroy()
        save_buttons.pop(-1)
    buttons()
        

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

    


EA_path=os.getenv('LOCALAPPDATA')+"\\Electronic Arts"
game_paths=["\\Harry Potter and the Order of the Phoenix\\HPOOTP\\","\\Harry Potter and the Half Blood Prince\\HPHBP0\\","\\Harry Potter and the Deathly Hallows (TM) – Part 1\\"]#,"\\Harry Potter and the Deathly Hallows (TM) – Part 2\\"]
games={game_paths[0]:"HP 5",game_paths[1]:"HP 6",game_paths[2]:"HP 7p1"}
base_game=game_paths[0]  #default game is HP5
save_files={game_paths[0]:r"HPOOTP",game_paths[1]:r"HPHBP0",game_paths[2]:"auto"}
base_save=save_files[base_game]
saves=[]
save_buttons=[]
additions=[]
modes=['load','delete']
mode = 'load'   #default mode is "load"
ns=[]



okno=Tk()

curr_game=Label(okno, text="Current game: "+games[base_game])
curr_game.pack()
games_butt=Button(text="Change game", bg="light grey", command=change_game)
games_butt.pack()
Label(okno, height="1").pack()

if os.path.isdir(EA_path+base_game):
    base_path=EA_path+base_game
    buttons()
else:
    missing()

okno.mainloop()

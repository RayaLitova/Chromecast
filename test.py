import pychromecast
from pychromecast.controllers.youtube import YouTubeController
from tkinter import *
from tkinter import messagebox
import lxml
from lxml import etree
import urllib.request
import re
import requests
from youtube_search import YoutubeSearch
import json
from keyboard import is_pressed
from tkinter.filedialog import askopenfile
import pytube
#----------------------------------------------------------
global active
chromecasts = pychromecast.Chromecast('192.168.0.101')
cast = chromecasts
cast.wait()
yt = YouTubeController()
cast.register_handler(yt)
names=[]
ids=[]
local_files=[]
local_names=[]
playlist_names=["Playlist","sejtsrt","nqn","sheufhi"]
plists={"Playlist": ["omg","pesen"],
         "sejtsrt": ["haha","juiusebhv","njnskjvbj"]
         }
queue=['nqen',"sjkber","uoseg","uihe"]
#----------------------------------------------------------------
def ret(win,op):
        win.destroy()
        return op

def messageWindow(title,op1,op2):
        win = Toplevel()
        win.title(title)
        Label(win, text=title).pack()
        Button(win, text=op1, command=ret(win,op1)).pack()
        Button(win, text=op2, command=ret(win,op1)).pack()
        return a

def extract_title(current_id):
        youtube = etree.HTML(urllib.request.urlopen("http://www.youtube.com/watch?v="+current_id).read())
        video_title = youtube.xpath("//span[@id='eow-title']/@title")
        return video_title


def download(vid,a):
        try:
            yt = pytube.YouTube(vid)
            vids= yt.streams.filter(only_audio=True).all()
            min_res=vids[0].abr[:-4]
            vnum=0
            for i in range(len(vids)):
                if vids[i].abr[:-4]<min_res:
                    min_res=vids[i].abr[:-4]
                    vnum=i
                    
            parent_dir = r"D:\music"
            vids[vnum].download(parent_dir)
            if a==1:
                    new_filename = vids[vnum].default_filename[:-1]+"3"
                    default_filename=vids[vnum].default_filename
                    os.rename(os.path.join(parent_dir, default_filename),\
                              os.path.join(parent_dir, new_filename))
        except:
            messagebox.showinfo("ERROR", "This song can't be downloaded")

        
def youtube(current_id):
        yt.play_video(current_id)
        
def yt_search(song,opt,i):
        if opt==1:
                results = YoutubeSearch(song, max_results=1).to_json()
                results=json.loads(results)
                a=results["videos"][0]['id']
                try:
                        if a not in ids:
                                ids.append(a)
                                names.append(extract_title(a))
                        if i==0:
                                youtube(a)
                        else:
                                answer=messageWindow("File format","mp3","mp4")
                                if answer=="mp3":
                                        download("https://www.youtube.com/watch?v=" + a,1)
                                elif answer=="mp4":
                                        download("https://www.youtube.com/watch?v=" + a,0)
                except:
                        messagebox.showinfo("ERROR", "No videos found :((")


        

def local():
        mc = cast.media_controller
        mc.play_media("D:\programirane\python prg\chromecast\nicebeatzprod - помоги мне его забыть.mp4", content_type = "video/mp4")
        mc.block_until_active()
        mc.play()
              

def pause():
        pass
def next_song():
        pass
def stop():
        pass
def prev():
        pass
def brs(opt,window_a):
        if opt==2:
              file=askopenfile(parent=window_a,mode='rb',title='Browse',filetypes =[('.mp4 .mp3')])
              local_files.append(file.name)
              name=str(file.name)
              for i in range(len(name)-1):
                      if name[i]=="/":
                              last=i
              name=name[(last+1):]
              local_names.append(name)

def add():
        window_a=Toplevel()
        window_a.geometry("200x150")
        window_a.title("Add song")
        
        v=IntVar()  
        yt_radio=Radiobutton(window_a, text="YouTube", variable=v, value=1).pack(anchor="w")
        lc_radio=Radiobutton(window_a, text="Local", variable=v, value=2).pack(anchor="w")
        entry1 = Entry (window_a)
        entry1.pack(anchor="nw")
        ok=Button(window_a,text="OK",command=lambda: yt_search(entry1.get(),v.get(),0))
        ok.pack(anchor="nw",fill=X)
        download=Button(window_a,text="Download",command=lambda: yt_search(entry1.get(),v.get(),1))
        ok.pack(anchor="w")
        browse=Button(window_a,text="Browse",command=lambda: brs(v.get(),window_a)).pack(side=LEFT)
        
        window_a.mainloop()

def add_queue(event):
        pass

def playlist_play(event):
       a=mylist.get(mylist.curselection())
       print(a)

def get_active(event,songs):
        active=songs.get(songs.curselection())   
        print(active)
        
def edit_playlist(event):
        a=plists[mylist.get(mylist.curselection())]
        edit=Toplevel()
        edit.geometry("200x" + str(len(a)*20+50))
        songs=Listbox(edit)
        for elem in a:
                songs.insert("end", elem)
        songs.pack(anchor=W)
        songs.bind('<Button-1>',get_active(event,songs))
        new=Button(edit,text=" Add New ",command=add)
        queue=Button(edit,text=" Add from queue ",command=add_queue)
        edit.mainloop()
#----------------------------------------------------------
window=Tk()
window.geometry("300x350")
window.title("My Player")

#-------------buttons--------------------------------
pause=Button(window,text=" Pause ",command=pause)
pause.pack(side=LEFT, anchor="n")

Stop=Button(window,text=" Stop ",command=stop)
Stop.pack(side=LEFT, anchor="n")

Prev=Button(window,text=" Prev ",command=prev)
Prev.pack(side=LEFT, anchor="n")

Next=Button(window,text=" Next ",command=next_song)
Next.pack(side=LEFT, anchor="n")

add=Button(window, text="Add Song", command=add)
add.pack(anchor="nw",fill=X)

#---------------------scrollbar-------------------------
scrollbar = Scrollbar(window)
scrollbar.pack(side = RIGHT,fill=Y)
mylist = Listbox(window, yscrollcommand = scrollbar.set )
for elem in playlist_names:
   mylist.insert(END, elem)

mylist.pack( side = RIGHT, fill = BOTH )
mylist.bind('<<ListboxSelect>>',playlist_play)
mylist.bind('<Double-1>',edit_playlist)
scrollbar.config( command = mylist.yview )
#-------------------------------------------------------



window.mainloop()
#cast.quit_app()


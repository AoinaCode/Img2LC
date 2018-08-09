from PIL import ImageTk,Image
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter import messagebox
import json
import os

#Image to Label Cut Ver1.0
#By AoinaCode https://github.com/AoinaCode/Img2LC


class UI(tk.Tk):
    def __init__(self):
        self.windows = tk.Tk()
        self.windows.geometry('1280x720')
        self.windows.title('Img2LC')

        #fram_start
        self.fram_start=ttk.Frame(self.windows)
        self.fram_start.grid(column=0,row=0,stick='wsne')

        self.img2labelcut_title = tk.Label(self.fram_start,text='Img2LabelCut',font=(None,100))
        self.img2labelcut_title.grid(column=0,columnspan=2,row=0,stick='nwns',padx=300)
        self.BtnSavePath = tk.Button(self.fram_start,text='設定專案資料夾:',font=(None,25),command=self.ChangeSavePath,bg='light sky blue')
        self.BtnSavePath.grid(column=0,columnspan=2,row=1,stick='n')
        self.BtnSavePathVal = tk.StringVar()
        self.SavePathShow = tk.Label(self.fram_start, textvariable=self.BtnSavePathVal,font=(None,25),bg='white')
        self.SavePathShow.grid(column=0,columnspan=2,row=2,stick='n')
        self.btn_enter_main = tk.Button(self.fram_start,text='開始',font=(None,50),command=self.enter_main)
        self.btn_enter_main.grid(column=0,columnspan=2,row=3,stick='n')
        self.enter_info_val =tk.StringVar()
        self.enter_info_title = tk.Label(self.fram_start,text='Info:',font=(None,25),bg='yellow')
        self.enter_info_title.grid(column=0,row=4,stick='ne')
        self.enter_info = tk.Label(self.fram_start,textvariable=self.enter_info_val,font=(None,25),bg='white')
        self.enter_info.grid(column=1,row=4,stick='nw')
        self.enter_info_val.set('---')

        #fram_main
        self.fram_main=ttk.Frame(self.windows)
        self.fram_main.grid(column=0,row=0,stick='wsne')
        self.NowImg_Title = tk.Button(self.fram_main,text='Input Image',font=(None,20),command=self.ChooseFile,bg='coral')
        self.NowImg_Title.grid(column=0,columnspan=1,row=0,rowspan=1,stick='ns')

        self.NowImg_Fram=ttk.Frame(self.fram_main)
        self.NowImg_Fram.grid(column=0,columnspan=1,row=1,rowspan=1,stick='wesn',padx=5)
        self.NowImgVal=tk.StringVar()
        self.NowImg_Num=tk.Label(self.NowImg_Fram,textvariable=self.NowImgVal,font=(None,15))
        self.NowImg_Num.pack(side='top')
        self.NowImgVal.set('ImgNum:00000')
        self.NowImg_Listbox = tk.Listbox(self.NowImg_Fram)
        self.NowImg_Listbox.pack(side='left',fill='both')
        self.NowImg_Scrollbar=ttk.Scrollbar(self.NowImg_Fram,orient=tk.VERTICAL,command=self.NowImg_Listbox.yview)
        self.NowImg_Scrollbar.pack(side='right',fill='both')
        self.NowImg_Listbox['yscrollcommand'] = self.NowImg_Scrollbar.set
        self.NowImg_Listbox.bind('<<ListboxSelect>>',self.ChooseImg,self.NowImg_Listbox)

        self.remove_chooseimg = tk.Button(self.fram_main,text='刪除圖片',font=(None,15),command=self.Del_cooseimg,bg='red')
        self.remove_chooseimg.grid(column=0,columnspan=1,row=2,rowspan=1,stick='we',padx=20)
        self.now_label_var = tk.StringVar()
        self.now_label_title = tk.Label(self.fram_main,textvariable=self.now_label_var,font=(None,15),bg='white')
        self.now_label_title.grid(column=0,columnspan=1,row=3,rowspan=1,stick='we',pady=2)
        self.now_label_var.set('標籤:New')
        self.load_label = tk.Button(self.fram_main,text='載入標籤',font=(None,15),bg='RoyalBlue1',command=self.LoadLabel)
        self.load_label.grid(column=0,columnspan=1,row=4,rowspan=1,stick='we',padx=10,pady=2)
        
        self.sync_label =tk.Button(self.fram_main,text='Sync Label',font=(None,15),bg='pink',command=self.SyncLabel)
        self.sync_label.grid(column=0,columnspan=1,row=5,rowspan=1,stick='we',padx=10,pady=2)

        self.Label3 = tk.Label(self.fram_main,text='定位點:',font=(None,20))
        self.Label3.grid(column=1,columnspan=1,row=0,stick='esn')
        self.Label3Val = tk.StringVar()
        self.Label3Box = tk.Label(self.fram_main,textvariable=self.Label3Val,font=(None,20))
        self.Label3Box.grid(column=2,columnspan=1,row=0,stick='wns')
        self.Label3Val.set('目前座標X:000,Y:000')
        self.Label2_title = tk.Label(self.fram_main,text='裁切預覽',font=(None,20))
        self.Label2_title.grid(column=3,columnspan=1,row=0,stick='sne')
        
        self.Bkimg = ImageTk.PhotoImage(Image.new('RGBA',(512,512), (255,255,255,255)))
        self.Canvas1 = tk.Canvas(self.fram_main,width=512,height=512,cursor="cross")
        self.Canvas1.bind("<ButtonPress-1>", self.OnMouseDown)
        self.Canvas1.bind("<B1-Motion>", self.OnMouseMove)
        self.Canvas1.bind("<ButtonRelease-1>", self.OnMouseUp)
        self.Canvas1.grid(column=1,columnspan=2,row=1,stick='wen',padx=10)
        self.Canvas1_Img=self.Canvas1.create_image(0,0,anchor='nw',image=self.Bkimg)
        
        self.canvas2_frame = tk.Frame(self.fram_main)
        self.canvas2_frame.grid(column=3,columnspan=2,row=1,stick='wen',padx=10)
        self.Canvas2 = tk.Canvas(self.canvas2_frame,width=384,height=384)
        self.Canvas2.pack(side='top',fill='both')
        self.Canvas2_Img = self.Canvas2.create_image(0,0,anchor='nw',image=self.Bkimg)
        self.canvas2_var_x = tk.StringVar()
        self.canvas2_var_x.set('X_Max:000 X_Min:000')
        self.canvas2_var_y = tk.StringVar()
        self.canvas2_var_y.set('Y_Max:000 Y_Min:000')
        
        self.canvas2_x = tk.Label(self.canvas2_frame,textvariable=self.canvas2_var_x,font=(None,30))
        self.canvas2_x.pack(side='top',fill='both')
        self.canvas2_y = tk.Label(self.canvas2_frame,textvariable=self.canvas2_var_y,font=(None,30))
        self.canvas2_y.pack(side='bottom',fill='both')


        self.image_optios = tk.Frame(self.fram_main)
        self.image_optios.grid(column=1,columnspan=2,row=2,stick='nswe')
        self.BtnCutImg=tk.Button(self.image_optios,text='裁切',font=(None,18),command=self.CutImage,bg='pink')
        self.BtnCutImg.grid(column=0,columnspan=1,row=0,stick='nswe',padx=10)
        self.BtnWriteData = tk.Button(self.image_optios,text='寫入標籤',font=(None,18),bg='light sky blue',command= self.WriteData)
        self.BtnWriteData.grid(column=1,columnspan=1,row=0,stick='nswe',padx=10)
        self.del_select_class=tk.Button(self.image_optios,text='刪除選取標籤',font=(None,18),bg='red',command=lambda:self.select_input('action','del'))
        self.del_select_class.grid(column=2,columnspan=1,row=0,stick='nswe',padx=10)

        self.SaveFileNameTitle = tk.Label(self.fram_main, text='標籤檔名:',font=(None,20))
        self.SaveFileNameTitle.grid(column=3,columnspan=1,row=4,stick='ens')
        self.SaveFileName = tk.StringVar()
        self.SaveFileNameInput = ttk.Entry(self.fram_main,textvariable=self.SaveFileName,font=(None,20))
        self.SaveFileNameInput.grid(column=4,columnspan=1,row=4,stick='ewn')
        
        self.CalssNum_Title = tk.Label(self.fram_main,text='ClassNum:',font=(None,20))
        self.CalssNum_Title.grid(column=1,columnspan=1,row=3,stick='nse')
        self.ClassNum=tk.StringVar()
        self.ClassNumInput = ttk.Combobox(self.fram_main,textvariable=self.ClassNum,font=(None,20))
        self.ClassNumInput.grid(column=2,columnspan=1,row=3,stick='we')
        self.ClassNumInput.bind('<<ComboboxSelected>>',lambda event:self.select_input(event,'num'))

        self.CalssText_Title = tk.Label(self.fram_main,text='ClassText:',font=(None,20))
        self.CalssText_Title.grid(column=1,columnspan=1,row=4,stick='nse')
        self.ClassText=tk.StringVar()
        self.ClassTextInput = ttk.Combobox(self.fram_main,textvariable=self.ClassText,font=(None,20))
        self.ClassTextInput.grid(column=2,columnspan=1,row=4,stick='we')
        self.ClassTextInput.bind('<<ComboboxSelected>>',lambda event:self.select_input(event,'text'))

        self.SysInfoTitle=tk.Label(self.fram_main,text='Info:',font=(None,20),bg='cyan')
        self.SysInfoTitle.grid(column=1,columnspan=1,row=5,stick='we')
        self.SysInfo=tk.Variable()
        self.SysInfoShow= tk.Label(self.fram_main,textvariable=self.SysInfo,font=(None,20),bg='yellow')
        self.SysInfoShow.grid(column=2,columnspan=3,row=5,stick='we')

        
        self.now_label_frame = tk.Frame(self.fram_main)
        self.now_label_frame.grid(column=5,row=0,rowspan=2,stick='wsen')
        self.label_input_title_var = tk.StringVar()
        self.label_input_title = tk.Label(self.now_label_frame,textvariable=self.label_input_title_var,font=(None,15))
        self.label_input_title_var.set('LabelNum:000000')
        self.label_input_title.pack(side='top',fill='both')
        self.label_input_litbox = tk.Listbox(self.now_label_frame,selectbackground='black',selectforeground='white')
        self.label_input_litbox.pack(side='left',fill='both')
        self.label_input_scrollbar = ttk.Scrollbar(self.now_label_frame,orient=tk.VERTICAL,command=self.label_input_litbox.yview)
        self.label_input_scrollbar.pack(side='right',fill='both')
        self.label_input_litbox['yscrollcommand'] = self.label_input_scrollbar.set
        self.label_input_litbox.bind('<<ListboxSelect>>',self.Choose_label,self.label_input_litbox)
        

        self.label_input_class_title = tk.Label(self.fram_main,text='選擇標籤內容',font=(None,20))
        self.label_input_class_title.grid(column=3,columnspan=2,row=2,stick='wnse')
        self.label_input_class_var = tk.StringVar()
        self.label_input_class_num_var = tk.StringVar()
        self.label_input_class = tk.Label(self.fram_main,textvariable=self.label_input_class_var,font=(None,20))
        self.label_input_class.grid(column=3,columnspan=1,row=3,stick='wnse')
        self.label_input_class_num = tk.Label(self.fram_main,textvariable=self.label_input_class_num_var,font=(None,20))
        self.label_input_class_num.grid(column=4,columnspan=1,row=3,stick='wnse')
        self.label_input_class_var.set('Text:---')
        self.label_input_class_num_var.set('Num:--')

        self.label_input_remove = tk.Button(self.fram_main,text='刪除標籤',command=self.delete_label,bg='red',font=(None,15))
        self.label_input_remove.grid(column=5,columnspan=1,row=2,stick='we',padx=5)
        self.label_input_reload = tk.Button(self.fram_main,text='重新讀取',command=self.RelodImage,font=(None,15))
        self.label_input_reload.grid(column=5,row=3,stick='we',padx=5,pady=2)
        self.btn_add_image_feature = tk.Button(self.fram_main,text='增加特徵',font=(None,15),bg='sky blue',command=self.add_image_feature)
        self.btn_add_image_feature.grid(column=5,row=4,stick='we',padx=5,pady=2)
        self.BtnSave=tk.Button(self.fram_main,text='儲存專案',font=(None,15),command=self.SaveProject,bg='red')
        self.BtnSave.grid(column=5,row=5,stick='we',padx=5,pady=2)

        #fram_setting
        self.InputImage = None
        self.CanvasImage = None
        self.CropImage=None
        self.ImageFileName=None
        self.StartDrawX=None
        self.StartDrawY=None
        self.EndDrawX=None
        self.EndDrawY=None
        self.SavePath=None
        self.SaveData={'data':{},'label':{}}
        self.save_data_class={}
        self.rectangle =  self.Canvas1.create_rectangle(0,0,0,0,outline='black',width=2)
        self.rectangleMove=None
        self.BtnSavePathVal.set('---')
        self.ChooseImageList = {}
        self.NowLabelChoose=None
        self.IsImgReload = False
        self.is_add_feature=False
        self.is_auto_load_next_img=True
        
        
    def ChooseFile(self):
        try:
            OpenImageUrl = list(filedialog.askopenfilenames(title='選擇要讀取圖片(jpg,jpeg,png)(可多選)'))
            nowlistnum = self.NowImg_Listbox.size()
            updata_item=0
            error_item=0
            for pathlist in OpenImageUrl:
                file = pathlist.split('/')[-1].split('.')
                filename = file[0]+'_512x512.'+file[1]
                if file[1]=='png' or file[1]=='jpg' or file[1]=='jpeg':
                    if filename in self.ChooseImageList:
                        updata_item+=1
                    else:
                        self.NowImg_Listbox.insert('end',filename)
                        if nowlistnum%2==0:
                            self.NowImg_Listbox.itemconfig(nowlistnum,background='white')
                        else:
                            self.NowImg_Listbox.itemconfig(nowlistnum,background='pink')
                        nowlistnum+=1
                    self.ChooseImageList[filename] = pathlist
                    
                else:
                    error_item+=1
            self.NowImgVal.set('ImgNum:'+str(nowlistnum))
            self.SysInfo.set('讀取到圖庫'+str(nowlistnum)+'個檔案路徑,更新路徑檔案有'+str(updata_item)+'個,讀取錯誤檔案有'+str(error_item)+'個')
           
        except:
            self.SysInfo.set('開啟圖片錯誤')
        
    
    def ChooseImg(self,even):
        widget = even.widget
        if widget.curselection():
            value = widget.get(widget.curselection()[0])
            self.InputImage = Image.open(self.ChooseImageList[value]).resize((512,512))
            self.CanvasImage = ImageTk.PhotoImage(self.InputImage)
            self.Canvas1.itemconfig(self.Canvas1_Img,image=self.CanvasImage)
            self.ImageFileName = value
            self.IsImgReload=False
            ImageName=self.ImageFileName
            if len(ImageName)>45:
                ImageName=ImageName[0:45]+'...'
            self.SysInfo.set('開啟['+ImageName+']圖片')
    
    def auto_choose_img(self,img_name):
        self.InputImage = Image.open(self.ChooseImageList[img_name]).resize((512,512))
        self.CanvasImage = ImageTk.PhotoImage(self.InputImage)
        self.Canvas1.itemconfig(self.Canvas1_Img,image=self.CanvasImage)
        self.ImageFileName = img_name
        self.IsImgReload=False
        ImageName=self.ImageFileName
        if len(ImageName)>45:
            ImageName=ImageName[0:45]+'...'
        self.SysInfo.set('開啟['+ImageName+']圖片')
        

    def RelodImage(self):
        if self.NowLabelChoose!=None and self.SavePath!=None:
            self.ImageFileName = self.NowLabelChoose.rsplit('_',2)[0]
            file_path=self.SavePath+self.ImageFileName
            if os.path.isfile(file_path):
                self.InputImage = Image.open(file_path).resize((512,512))
                self.CanvasImage = ImageTk.PhotoImage(self.InputImage)
                self.Canvas1.itemconfig(self.Canvas1_Img,image=self.CanvasImage)
                self.ClassText.set(self.SaveData['data'][self.ImageFileName]['data'][self.NowLabelChoose]['class_text'])
                self.ClassNum.set(str(self.SaveData['data'][self.ImageFileName]['data'][self.NowLabelChoose]['class']))
                self.StartDrawX=self.SaveData['data'][self.ImageFileName]['data'][self.NowLabelChoose]['xmin']
                self.EndDrawX=self.SaveData['data'][self.ImageFileName]['data'][self.NowLabelChoose]['xmax']
                self.StartDrawY=self.SaveData['data'][self.ImageFileName]['data'][self.NowLabelChoose]['ymin']
                self.EndDrawY=self.SaveData['data'][self.ImageFileName]['data'][self.NowLabelChoose]['ymax']
                self.Canvas1.coords(self.rectangle,self.StartDrawX,self.StartDrawY,self.EndDrawX,self.EndDrawY)
                self.CutImage()
                ImageName=self.ImageFileName
                if len(ImageName)>40:
                    ImageName=ImageName[0:40]+'...'
                self.SysInfo.set('重新載入['+ImageName+']圖片')
                self.IsImgReload=True
            else:
                self.SysInfo.set('載入失敗,檔案遺失')
        else:
            self.SysInfo.set('尚未載入標籤or未指定存檔路徑')

    def add_image_feature(self):
        self.IsImgReload=False
        if self.NowLabelChoose!=None:
            self.ImageFileName = self.NowLabelChoose.rsplit('_',2)[0]
            file_path=self.SavePath+self.ImageFileName
            if os.path.isfile(file_path):
                self.InputImage = Image.open(file_path).resize((512,512))
                self.CanvasImage = ImageTk.PhotoImage(self.InputImage)
                self.Canvas1.itemconfig(self.Canvas1_Img,image=self.CanvasImage)
                ImageName=self.ImageFileName
                if len(ImageName)>40:
                    ImageName=ImageName[0:40]+'...'
                self.is_add_feature=True
                self.ClassText.set('')
                self.ClassNum.set('')
                self.SysInfo.set('['+ImageName+']圖片增加特徵')
                
            else:
                self.SysInfo.set('載入失敗,檔案遺失')
        
    def Del_cooseimg(self):
        listboxnum = self.NowImg_Listbox.get(0,'end').index(self.ImageFileName)
        del self.ChooseImageList[self.ImageFileName]
        self.NowImg_Listbox.delete(listboxnum)
        self.Canvas1.itemconfig(self.Canvas1_Img,image=self.Bkimg)
        self.NowImgVal.set('ImgNum:'+str(len(self.NowImg_Listbox.get(0,'end'))))
        ImageName=self.ImageFileName
        if len(ImageName)>40:
            ImageName=ImageName[0:40]+'...'
        self.SysInfo.set('載入圖片['+ImageName+']刪除成功')
        self.Canvas1.itemconfig(self.Canvas1_Img,image=self.Bkimg)
        self.ImageFileName=None
        self.InputImage=None

    def Insert_label(self,name):
        self.label_input_litbox.insert('end',name)
        nowsize = self.label_input_litbox.size()
        text='LabelNum:'+str(nowsize)
        self.label_input_title_var.set(text)
        nowsize-=1
        if nowsize%2==0:
            self.label_input_litbox.itemconfig(nowsize,background='pink')
        else:
            self.label_input_litbox.itemconfig(nowsize,background='deep sky blue')
    
    def delete_label(self):
        if self.NowLabelChoose!=None:
            select_num = self.label_input_litbox.get(0,'end').index(self.NowLabelChoose)
            self.label_input_litbox.delete(select_num)
            del self.SaveData['data'][self.ImageFileName]['data'][self.NowLabelChoose]
            ImageName=self.NowLabelChoose
            if len(ImageName)>45:
                ImageName=ImageName[0:40]+'...'
            self.SysInfo.set('刪除'+ImageName+'標籤成功')
            nowsize = self.label_input_litbox.size()
            text='LabelNum:'+str(nowsize)
            self.label_input_title_var.set(text)
            if self.SaveData['data'][self.ImageFileName]['data']=={}:
                del self.SaveData['data'][self.ImageFileName]
            
        else:
            self.SysInfo.set('尚未選擇標籤')


    def Choose_label(self,even):
        widget=even.widget
        if widget.curselection():
            value = widget.get(widget.curselection()[0])
            self.NowLabelChoose=value
            self.ImageFileName = self.NowLabelChoose.rsplit('_',2)[0]
            Text = self.SaveData['data'][self.ImageFileName]['data'][self.NowLabelChoose]['class_text']
            Num = 'Num:'+str(self.SaveData['data'][self.ImageFileName]['data'][self.NowLabelChoose]['class'])
            if len(Text)>5:
                Text = 'Text:'+Text[0:6]+'...'
                self.label_input_class_var.set(Text)
            else:
                Text = 'Text:'+Text
                self.label_input_class_var.set(Text)
            self.label_input_class_num_var.set(Num)
        
        
    def OnMouseDown(self,event):
        self.StartDrawX=event.x
        self.StartDrawY=event.y
        
    def OnMouseMove(self,event):
        x = event.x
        y = event.y
        if x<0:
            x=0
        elif x>512:
            x=512
        if y<0:
            y=0
        elif y>512:
            y=512
        value = '目前座標X:'+str(x)+',Y:'+str(y)
        self.Label3Val.set(value)
        self.Canvas1.coords(self.rectangle,self.StartDrawX,self.StartDrawY,x,y)
        
    def OnMouseUp(self,event):
        x=event.x
        y=event.y
        if x<0:
            x=0
        elif x>512:
            x=512
        if y<0:
            y=0
        elif y>512:
            y=512
        self.EndDrawX=x
        self.EndDrawY=y

    def select_input(self,event,action):
        if action=='num':
            self.ClassTextInput.set(self.save_data_class[self.ClassNum.get()])
        elif action=='text':
            self.ClassNumInput.set(list(self.save_data_class.keys())[list(self.save_data_class.values()).index(self.ClassTextInput.get())])
        elif action=='del':
            if self.ClassNum.get() and self.ClassText:
                del self.save_data_class[self.ClassNum.get()]
                self.ClassNumInput['values']=list(self.save_data_class.keys())
                self.ClassTextInput['values'] = list(self.save_data_class.values())
                self.ClassText.set('')
                self.ClassNum.set('')

    def CutImage(self):
        if self.InputImage!=None:
            cut =  self.InputImage.crop((self.StartDrawX,self.StartDrawY,self.EndDrawX,self.EndDrawY)).resize((384,384))
            x_label = 'X_Max:'+str(self.EndDrawX)+' X_Min:'+str(self.StartDrawX)
            self.canvas2_var_x.set(x_label)
            y_label = 'Y_Max:'+str(self.EndDrawY)+' Y_Min:'+str(self.StartDrawY)
            self.canvas2_var_y.set(y_label)
            self.CropImage =ImageTk.PhotoImage(cut)
            self.Canvas2.itemconfig(self.Canvas2_Img,image=self.CropImage)
        else:
            self.SysInfo.set('裁切失敗,尚未載入圖片')

    def WriteData(self):
        def save_label():
            try:
                if self.ImageFileName in self.SaveData['data']:
                    self.SaveData['data'][self.ImageFileName]['num'] =self.SaveData['data'][self.ImageFileName]['num']+1
                    new_label_name = self.ImageFileName+'_'+str(self.SaveData['data'][self.ImageFileName]['num'])+'_'+self.ClassNum.get()
                    self.SaveData['data'][self.ImageFileName]['data'][new_label_name]={
                        'xmin':self.StartDrawX,
                        'xmax':self.EndDrawX,
                        'ymin':self.StartDrawY,
                        'ymax':self.EndDrawY,
                        'class_text':self.ClassText.get(),
                        'class':int(self.ClassNum.get())
                    }
                elif self.ImageFileName not in self.SaveData['data']:
                    new_label_name=self.ImageFileName+'_1_'+self.ClassNum.get()
                    self.SaveData['data'][self.ImageFileName]={
                        'data':{
                            new_label_name:{
                                'xmin':self.StartDrawX,
                                'xmax':self.EndDrawX,
                                'ymin':self.StartDrawY,
                                'ymax':self.EndDrawY,
                                'class_text':self.ClassText.get(),
                                'class':int(self.ClassNum.get())
                            }
                        },
                        'num':1,
                        'height':self.InputImage.height,
                        'width':self.InputImage.width,
                        'format':self.ImageFileName.split('.')[1]
                    }
                self.Insert_label(new_label_name)
                if self.is_add_feature==True:
                    self.is_add_feature=False
                    self.Canvas1.itemconfig(self.Canvas1_Img,image=self.Bkimg)
                    self.ImageFileName=None
                    self.InputImage=None
                    if len(new_label_name)>35:
                        new_label_name=new_label_name[0:35]+'...'
                    self.SysInfo.set('標籤['+new_label_name+']寫入完成')
                else:
                    list_box = self.NowImg_Listbox.get(0,'end')  
                    listboxnum = list_box.index(self.ImageFileName)
                    self.NowImg_Listbox.delete(listboxnum)
                    del self.ChooseImageList[self.ImageFileName]
                    if self.is_auto_load_next_img==True and self.NowImg_Listbox.size()!=0 and self.NowImg_Listbox.size()!=(listboxnum+2):
                        self.ImageFileName=None
                        self.InputImage=None
                        nex_img=list_box[(listboxnum+1)]
                        self.auto_choose_img(nex_img)
                        if len(new_label_name)>15:
                            new_label_name=new_label_name[0:15]+'...'
                        if len(nex_img)>15:
                            nex_img=nex_img[0:15]+'...'
                        self.SysInfo.set('標籤['+new_label_name+']寫入完成,自動讀取['+nex_img+']圖片')
                    else:
                        self.Canvas1.itemconfig(self.Canvas1_Img,image=self.Bkimg)
                        self.ImageFileName=None
                        self.InputImage=None
                        if len(new_label_name)>35:
                            new_label_name=new_label_name[0:35]+'...'
                        self.SysInfo.set('標籤['+new_label_name+']寫入完成')
                self.NowImgVal.set('ImgNum:'+str(self.NowImg_Listbox.size()))
                
                
            except:   
                self.SysInfo.set('圖片標籤['+self.ImageFileName+']寫入失敗')

        #main
        if self.InputImage!=None and self.ClassNum.get() and self.ClassText.get():
            if self.IsImgReload:
                if self.NowLabelChoose!=None:
                    self.SaveData['data'][self.ImageFileName]['data'][self.NowLabelChoose]={
                        'xmin':self.StartDrawX,
                        'xmax':self.EndDrawX,
                        'ymin':self.StartDrawY,
                        'ymax':self.EndDrawY,
                        'class_text':self.ClassText.get(),
                        'class':int(self.ClassNum.get())
                    }
                    listboxnum = self.label_input_litbox.get(0,'end').index(self.NowLabelChoose)
                    self.label_input_litbox.delete(listboxnum)
                    self.Insert_label(self.NowLabelChoose)
                    self.Canvas1.itemconfig(self.Canvas1_Img,image=self.Bkimg)
                    self.NowImgVal.set('ImgNum:'+str(self.NowImg_Listbox.size()))
                    if len(self.NowLabelChoose)>35:
                        self.NowLabelChoose=self.NowLabelChoose[0:35]+'...'
                    self.SysInfo.set('圖片標籤['+self.NowLabelChoose+']更新完成')
                    self.ImageFileName=None
                    self.InputImage=None
                    self.IsImgReload=False
                    self.NowLabelChoose=None
                else:
                    self.SysInfo.set('重新寫入標籤錯誤')
                    self.ImageFileName=None
                    self.InputImage=None
                    self.IsImgReload=False
                    self.NowLabelChoose=None
            else:
                if self.SavePath!=None:
                    savepath = self.SavePath+self.ImageFileName
                    if os.path.isfile(savepath)==True:
                        save_label()
                    elif os.path.isfile(savepath)==False:
                        try:
                            savepath = self.SavePath+self.ImageFileName
                            self.InputImage.save(savepath)
                            save_label()
                        except:
                            self.SysInfo.set('圖片寫入專案資料夾錯誤')
                else:
                    self.SysInfo.set('尚未指定儲存路徑')
            #WrtieLabel
            if self.ClassNum.get() not in self.save_data_class:
                self.save_data_class[self.ClassNum.get()]=self.ClassText.get()
                self.ClassNumInput['values']=list(self.save_data_class.keys())
                self.ClassTextInput['values'] = list(self.save_data_class.values())
                
                
        else:
            self.SysInfo.set('尚未編輯標籤或載入圖片')

    def LoadLabel(self):
        def LoadFile():
            filepath=filedialog.askopenfilename(title='讀取標籤(限本程式輸出JSON)')
            if filepath:
                filename=filepath.split('/')[-1]
                if filename.split('.')[1]=='json':
                    with open(filepath,mode='r',encoding='utf-8') as file:
                        self.SaveData = json.load(file)
                    self.SysInfo.set('標籤載入完畢')
                    self.SaveFileName.set(filename.split('.')[0])
                    self.now_label_var.set('標籤:Load')
                    for file in self.SaveData['data']:
                        for label in self.SaveData['data'][file]['data']:
                            self.Insert_label(label)
                else:
                    self.SysInfo.set('讀取標籤錯誤,請選擇*.JSON')
            else:
                self.SysInfo.set('尚未選擇檔案')
        
        if len(self.SaveData['data'])==0:
            LoadFile()
        else:
            question = messagebox.askyesno(message='目前儲存的標籤不是空值,是否要取代原本儲存的標籤?',icon='question',title='取代標籤')
            if question==True:
                self.SaveData.clear()
                LoadFile()
            elif question==False:
                self.SysInfo.set('取消讀取標籤')
            
    def SyncLabel(self):
        if self.SavePath!=None:
            self.Canvas1.itemconfig(self.Canvas1_Img,image=self.Bkimg)
            self.ImageFileName=None
            for data in self.SaveData['data']:
                file = self.SavePath+data
                if os.path.isfile(file)==True:
                    listbox = self.NowImg_Listbox.get(0,'end')
                    self.NowImg_Listbox.delete(listbox.index(data))
            self.NowImgVal.set('ImgNum:'+str(len(self.NowImg_Listbox.get(0,'end'))))
            self.SysInfo.set('標籤與圖庫同步完成')
        else:
            self.SysInfo.set('尚未指定儲存路徑')

    def SaveProject(self):
        if self.SavePath==None:
            self.SysInfo.set('尚未指定儲存路徑')
        elif not self.SaveFileName.get():
            self.SysInfo.set('尚未指定標籤儲存檔名')
        else:
            self.SaveData['version']='1.0'
            self.SaveData['label'].update(self.save_data_class)
            with open(self.SavePath+self.SaveFileName.get()+'.json',mode='w',encoding='utf-8') as file:
                json.dump(self.SaveData,file,ensure_ascii=False,indent=4)
            self.SysInfo.set('圖片標籤存檔完成')

    def ChangeSavePath(self):
        getpath = filedialog.askdirectory()
        if getpath:
            self.SavePath=getpath+'/'
            self.BtnSavePathVal.set(self.SavePath)
        else:
            self.SavePath=None
        
    def enter_main(self):
        if self.SavePath=='---' or self.SavePath==None:
            self.enter_info_val.set('尚未設定專案路徑')
        else:
            if os.path.isdir(self.SavePath):
                self.fram_main.tkraise()
                self.windows.title('Img2LC 目前開啟專案路徑:'+self.SavePath)
            else:
                self.enter_info_val.set('設定專案路徑錯誤')

    def show(self):
        self.fram_start.tkraise()
        self.windows.mainloop()


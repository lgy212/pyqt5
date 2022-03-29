from msilib.schema import Icon
import sys
from turtle import pos
from unicodedata import name
from xml.dom.pulldom import PROCESSING_INSTRUCTION
from PyQt5.QtWidgets import QWidget,QApplication,QMainWindow
from PyQt5 import QtCore,QtGui
from Ui_MainWindow import Ui_MainWindow
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os
import cv2
import numpy as np
import random
import json
from shutil import copyfile 
class My_window(QMainWindow,Ui_MainWindow):
    m_SoftVersion='1.0.0'
    m_trainData=QtGui.QStandardItemModel()
    m_testData=QtGui.QStandardItemModel()
    m_catData=QtGui.QStandardItemModel()
    m_modelData=QtGui.QStandardItemModel()
    m_isTrainData=True
    m_drawMode=0
    m_selectModel=-1
    m_selectCat=-1
    m_showLabel=False
    m_showDetect=False
    m_projectPath='E:/lgy/pyqt/src/'
    m_projectName="test"
    m_projectType='cls'
    def __init__(self):
        super(My_window, self).__init__()
        self.setupUi(self)
        self.initData()
        
    def initData(self):
        self.m_trainData.setHorizontalHeaderLabels(["图片","标记","检测","概率"])
        self.m_testData.setHorizontalHeaderLabels(["图片","标记","检测","概率"])
        self.m_catData.setHorizontalHeaderLabels(['类名','颜色','图片数'])
        self.m_modelData.setHorizontalHeaderLabels(['模型名','Loss','训练总数'])
        #self.tableTrain.horizontalHeader().setStretchLastSection(True)
        #self.tableTrain.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableTrain.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableTest.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableView_modelResult.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableCat.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableView_modelResult.setModel(self.m_modelData)
        self.tableCat.setModel(self.m_catData)
        self.tableTrain.setModel(self.m_trainData)
        self.tableTest.setModel(self.m_testData)
        
        self.showData()
    def showData(self):
        # item1=QStandardItem('模型1')
        # item2=QStandardItem("0.1122")
        # item3=QStandardItem("0")
        # self.m_modelData.appendRow([item1,item2,item3])
        pass
        # self.m_trainData.setItem(1, 0, QtGui.QStandardItem("李四"))
        # self.m_trainData.setItem(1, 1, QtGui.QStandardItem("20120203000000000000000"))
        # #设置条目颜色和字体
        # self.m_trainData.item(0, 0).setForeground(QtGui.QBrush(QtGui.QColor(255, 0, 0)))     
        # self.m_trainData.item(0, 0).setFont(QtGui.QFont("Times", 10, QtGui.QFont.Black))
         
        # self.m_trainData.item(3, 1).setBackground(QtGui.QBrush(QtGui.QColor(255, 255, 0)))
         
        #按照编号排序
        #self.m_trainData.sort(1, QtCore.Qt.DescendingOrder)

    def slot_new(self):#新建
        dir=os.path.join(self.m_projectPath,self.m_projectName)
        if os.path.exists(dir):
            QMessageBox.information(self,"提示","该项目已经存在!",QMessageBox.Yes)
            return
        else:
            os.mkdir(dir)
            os.makedirs(os.path.join(dir,"data"))
            os.makedirs(os.path.join(dir,'image'))
            os.makedirs(os.path.join(dir,'model'))
            os.makedirs(os.path.join(dir,'saves'))

    def slot_open(self):#打开
        fileName_choose, filetype = QFileDialog.getOpenFileName(self,"打开项目", os.getcwd(), "Text Files (*.json)")   # 设置文件扩展名过滤,用双分号间隔

        if fileName_choose == "":
            QMessageBox.information(self,"提示","请选择需要打开的项目!",QMessageBox.Yes)
            return
        with open(fileName_choose,'r') as load_f:
            load_dict = json.load(load_f)
            self.m_SoftVersion=load_dict['Version']
            self.m_projectType=load_dict['ProjectType']
            self.m_projectPath=load_dict['ProjectPath']
            self.m_projectName=load_dict['ProjectName']
            imagelist=load_dict['ImageList']
            catlist=load_dict['CatList']
            modellist=load_dict['ModelList']
            print(self.m_SoftVersion)

       
    def slot_save(self):#保存
        allData={}
        allData['Version']=self.m_SoftVersion
        allData['ProjectType']=self.m_projectType
        allData['ProjectPath']=self.m_projectPath
        allData['ProjectName']=self.m_projectName
         
        allData['ImageList']=''
        allData['CatList']=''
        allData['ModelList']=''
        with open(os.path.join(self.m_projectPath,os.path.join(self.m_projectName,self.m_projectName))+'.json','w') as f:
            json.dump(allData,f)

        
    def slot_select(self):#选定
        self.m_drawMode=0
        
    def slot_move(self):#移动
        self.m_drawMode=1
        
    def slot_line(self):#直线
        self.m_drawMode=2
        
    def slot_polyline(self):#曲线
        self.m_drawMode=3
        
    def slot_rect(self):#矩形
        self.m_drawMode=4
        
    def slot_elli(self):#椭圆
        self.m_drawMode=5
        
    def slot_polygon(self):#多边形
        self.m_drawMode=6
        
    def slot_train(self):#训练
        pass
    def slot_test(self):#检测
        pass
    def slot_traindata(self):#训练集
        self.m_isTrainData=True
        self.stackedWidget.setCurrentIndex(0)
        
    def slot_testdata(self):#测试集
        self.m_isTrainData=False
        self.stackedWidget.setCurrentIndex(1)
        
    def slot_addimage(self):#添加图片
        files, filetype = QFileDialog.getOpenFileNames(self, "多文件选择",os.getcwd(),"Image Files (*.jpg;*.jpeg;*.bmp;*.png)")  

        if len(files) == 0:
            QMessageBox.information(self,"提示","请选择文件!",QMessageBox.Yes)
            return
        for file in files:
            picname=os.path.basename(file)
            copyfile(file,os.path.join(self.m_projectPath,self.m_projectName,'image',picname))
            item1=QStandardItem(picname)
            item2=QStandardItem("")
            item3=QStandardItem("")
            item4=QStandardItem("")
            if self.m_isTrainData==True:
                self.m_trainData.appendRow([item1,item2,item3,item4])
            else:
                self.m_testData.appendRow([item1,item2,item3,item4])
        

    def slot_addFolder(self):#添加文件夹
        dir_choose=QFileDialog.getExistingDirectory(self,"选取文件夹",os.getcwd())
        if dir_choose=="":
            QMessageBox.information(self,"提示","请选择文件夹!",QMessageBox.Yes)
            return
        files=os.listdir(dir_choose)
        if len(files)==0:
            QMessageBox.information(self,"提示","文件夹下不存在图片!",QMessageBox.Yes)
            return
        for file in files:
            filename=os.path.basename(file)
            ext=os.path.splitext(filename)[-1]
            if ext not in ['.jpg','.png','.bmp','.jpeg']:
                continue
            copyfile(os.path.join(dir_choose,file),os.path.join(self.m_projectPath,self.m_projectName,'image',filename))
            item1=QStandardItem(filename)
            item2=QStandardItem("")
            item3=QStandardItem("")
            item4=QStandardItem("")
            if self.m_isTrainData==True:
                self.m_trainData.appendRow([item1,item2,item3,item4])
            else:
                self.m_testData.appendRow([item1,item2,item3,item4])
        
    def slot_moveToOpposite(self):#移至
        if self.m_isTrainData==True:
            selections=self.tableTrain.selectionModel().selectedRows()
            #selected=selections.selectedIndexes()
            list1=[]
            for index in selections:
                list1.append(index.row())
            list1.sort(key=int,reverse=True)
            
            for i in list1:
                self.m_testData.appendRow(self.m_trainData.takeRow(i))
                #self.m_testData.insertRows(selections)
                #self.m_trainData.removeRow(i)                
        else:
            selections=self.tableTest.selectionModel().selectedRows()
            list1=[]
            for index in selections:
                list1.append(index.row())
            list1.sort(key=int,reverse=True)
            for i in list1:
                self.m_trainData.appendRow(self.m_testData.takeRow(i))
        
    def slot_deleteimage(self):#删除图片
        if self.m_isTrainData==True:
            selections=self.tableTrain.selectionModel().selectedRows()
            #selected=selections.selectedIndexes()
            list1=[]
            for index in selections:
                list1.append(index.row())
            list1.sort(key=int,reverse=True)
            for i in list1:
                self.m_trainData.removeRow(i)
        else:
            selections=self.tableTest.selectionModel().selectedRows()
            list1=[]
            for index in selections:
                list1.append(index.row())
            list1.sort(key=int,reverse=True)
            for i in list1:
                self.m_testData.removeRow(i)   

    def slot_picChange(self,modelIndex):#图片切换
        rowindex=modelIndex.row()
        picname=''
        if self.m_isTrainData==True:
            picname=self.m_trainData.index(rowindex,0).data()
        else:
            picname=self.m_testData.index(rowindex,0).data()
        if picname!='':
            picname=os.path.join(self.m_projectPath,picname)
            img=cv2.imdecode(np.fromfile(picname, dtype=np.uint8),cv2.IMREAD_UNCHANGED)
            img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            x=img.shape[1]
            y=img.shape[0]
            self.zoonScale=1
            frame=QImage(img,x,y,QImage.Format.Format_RGB888)
            pix=QPixmap.fromImage(frame)
            self.item=QGraphicsPixmapItem(pix)
            self.scene=QGraphicsScene()
            self.scene.addItem(self.item)
            self.picShow.setScene(self.scene)

    def slot_addClass(self):#添加类
        if self.m_modelData.rowCount()!=0:
            QMessageBox.information(self,"提示","当前存在模型，不可添加类!",QMessageBox.Yes)
            return
        else:
            item1=QStandardItem('类1')
            item2=QStandardItem("")
            item2.setBackground(QBrush(QColor(random.randint(0,255),random.randint(0,255),random.randint(0,255))))
            item3=QStandardItem("0")
            self.m_catData.appendRow([item1,item2,item3])
            self.catNum.setText(str(self.m_catData.rowCount()))
        
    def slot_selectCat(self,modelIndex):#选定类
        self.m_selectCat=modelIndex.row()
        
    def slot_editCat(self,modelIndex):#编辑类
        if self.m_modelData.rowCount()!=0:
            QMessageBox.information(self,"提示","当前存在模型，不可编辑类!",QMessageBox.Yes)
            return
        else:
            row=modelIndex.row()
            col=modelIndex.column()
            if col==0:
                text, okPressed = QInputDialog.getText(self, "输入框","请输入类名:", QLineEdit.Normal, "")
                if okPressed and text != '':
                    self.m_catData.setData(modelIndex,text,Qt.DisplayRole)                
            elif col==1:
                color=QColorDialog.getColor()
                self.m_catData.setData(modelIndex,QBrush(QColor(color.name())),Qt.BackgroundRole)
                #print(color.name())
                
            
    def slot_deleteClass(self):#删除类
        if self.m_modelData.rowCount()!=0:
            QMessageBox.information(self,"提示","当前存在模型，不可删除类!",QMessageBox.Yes)
            return
        else:
            selections=self.tableCat.selectionModel().selectedRows()
            #selected=selections.selectedIndexes()
            list1=[]
            for index in selections:
                list1.append(index.row())
            list1.sort(key=int,reverse=True)
            for i in list1:
                self.m_catData.removeRow(i)
            self.catNum.setText(str(self.m_catData.rowCount()))
    
    def slot_selectModel(self,modelIndex):#选定模型
        self.m_selectModel=modelIndex.row()
        
    def slot_modelInfo(self):#模型信息
        QMessageBox.information(self,"提示","无模型信息!",QMessageBox.Yes)
        
    def slot_importModel(self):#导入模型
        item1=QStandardItem('模型1')
        item2=QStandardItem("loss")
        item3=QStandardItem("trainNum")
        self.m_modelData.appendRow([item1,item2,item3])
        self.modelNum.setText(str(self.m_modelData.rowCount()))
        pass
    def slot_exportModel(self):#导出模型
        #dir_choose=QFileDialog.getExistingDirectory(self,"选取文件夹",os.getcwd())
        dir,name=QFileDialog.getSaveFileName(self,"选取文件夹",os.getcwd())
        print(dir+"-"+name)
        pass
    def slot_deleteModel(self):#删除模型
        selections=self.tableView_modelResult.selectionModel().selectedRows()        
        #selected=selections.selectedIndexes()
        list1=[]
        for index in selections:
            list1.append(index.row())
        list1.sort(key=int,reverse=True)
        for i in list1:
            self.m_modelData.removeRow(i)
        self.modelNum.setText(str(self.m_modelData.rowCount()))
        
    def slot_showLabel(self):#显示标记
        pass
    def slot_showDetect(self):#显示检测
        pass
    
        

if __name__=='__main__':
    app=QApplication(sys.argv)
    # w=QMainWindow()
    # main=Ui_MainWindow()
    # main.setupUi(w)
    w=My_window()
    
    w.show()
    sys.exit(app.exec_())
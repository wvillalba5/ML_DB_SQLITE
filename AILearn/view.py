
import os
from tkinter.font import BOLD
from PyQt6.QtWidgets import QMainWindow, QFileDialog,QTableWidgetItem,QHeaderView
from PyQt6.QtGui import QAction,QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from configuration import config
from Linear_Matplot import*

from comm_db import communication_db




class View(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.theta0_Qline.setReadOnly(True)
        self.ui.theta1_Qline.setReadOnly(True)
        self.ui.Cost_QLine.setReadOnly(True)
        self.ui.Value_predicted.setReadOnly(True)
        self.ui.Qline_mean.setReadOnly(True)
        self.ui.Qline_std.setReadOnly(True)
        self.ui.Qline_variace.setReadOnly(True)
        self.ui.Qline_max.setReadOnly(True)
        self.ui.Qline_min.setReadOnly(True)
        self.ui.Graph_cboBox.addItems(["Scatter", "Line"])
        self.ui.theta_0.setPlaceholderText('Enter a integer')
        self.ui.theta_1.setPlaceholderText('Enter a integer')
        self.ui.value_iterations.setPlaceholderText('Enter a integer')
        self.ui.Alpha.setPlaceholderText('from 0.001 to 0.02')
        self.ui.axe_x_Qline.setPlaceholderText('Name "X" axe')
        self.ui.axe_y_Qline.setPlaceholderText('Name "Y" axe')
        self.ui.PValue_lineEdit.setPlaceholderText('Enter a float')
        self.font = QtGui.QFont()
        self.font.setBold(True)
        self.font.setPointSize(14)
        self.data_base = communication_db()
        self.layaut_home()




    def show_dialog(self):
        file_filter = 'Data File (*.txt)'
        self.path_file_txt = QFileDialog.getOpenFileName(parent=self, caption='Select data file',directory=os.getcwd(),
        filter=file_filter) 
        return self.path_file_txt[0]
        

    def call_canvas_scatter(self,X,y,x_graph_label,y_graph_label):
        self.scatter = Canvas_scatter(X,y,x_graph_label,y_graph_label)
        self.ui.scatter_VLayout.addWidget(self.scatter)
        self.ui.stackedWidget.setCurrentIndex(0)
      

    def call_canvas_Linear(self,X,y,X1,theta_m,x_graph_label,y_graph_label):
        self.Linear = Canvas_Linear(X,y,X1,theta_m,x_graph_label,y_graph_label)
        self.ui.line_VLayout.addWidget(self.Linear)
        self.ui.stackedWidget.setCurrentIndex(1)

    def call_canvas_bar(self,y):
        X = ["Mean", "std", "variance","Max","Min"]
        x_label = self.list_cbx[self.index1]
        self.bar = Canvas_Bar(X,y,x_label)
        self.ui.Bar_graph.addWidget(self.bar)
        


    def clear_canvas(self):
        self.ui.scatter_VLayout.takeAt(0)
        self.ui.line_VLayout.takeAt(0)
        self.ui.Bar_graph.takeAt(0)

    def Change_Widget(self):
        widget = self.ui.Graph_cboBox.currentIndex()
        self.ui.stackedWidget.setCurrentIndex(widget)
        
    
    

    def layaut_home(self):
        self.ui.main_stackedWidget.setCurrentIndex(1)
    
    def layaut_Linear_regression(self):
        self.ui.main_stackedWidget.setCurrentIndex(0)

    def layaut_database(self):
        self.ui.main_stackedWidget.setCurrentIndex(2)

    def layaut_AI(self):
        self.ui.main_stackedWidget.setCurrentIndex(3)

            

    def table_popupation(self):
        self.table = "world_population"
        self.ui.Label_reference_table.setText(self.table)
        self.ui.Label_reference_table.setFont(self.font)
        self.ui.cbx_insert.clear()
        self.show_tables(self.table)

    def table_economy(self):
        self.table = "world_economy"
        self.ui.Label_reference_table.setText(self.table)
        self.ui.Label_reference_table.setFont(self.font)
        self.ui.cbx_insert.clear()
        self.show_tables(self.table)

        
    def table_ecuador(self):
        self.table = "ecuador"
        self.ui.Label_reference_table.setText(self.table)
        self.ui.Label_reference_table.setFont(self.font)
        self.ui.cbx_insert.clear()
        self.show_tables(self.table)

    def show_tables(self, table):
        
        [self.datos,self.title,self.num_rows,self.num_columns] = self.data_base.read_table(table)
      
      
        self.ui.tableWidgetDB.setRowCount(self.num_rows)
        self.ui.tableWidgetDB.setColumnCount(self.num_columns)
        self.ui.cbx_insert.addItems(self.title)
        tablerow = 0
        for row in self.datos:
            for column in range(self.num_columns):
                self.ui.tableWidgetDB.setColumnWidth(column, 300)
                self.ui.tableWidgetDB.setHorizontalHeaderLabels(self.title)
                self.ui.tableWidgetDB.setItem(tablerow,column,QTableWidgetItem(str(row[column]).replace(",",".")))
            tablerow += 1
        
        
        
        

    def search_country_in_table(self):
        try:
            table = self.ui.Label_reference_table.text()
            country_name = self.ui.Qline_country_search.text()
            country_name = str("'" + country_name + "'")

            [self.datos,self.title,self.num_rows,self.num_columns] = self.data_base.search_country(table,country_name)

            self.ui.tableWidgetDB.setHorizontalHeaderLabels(self.title)
            self.ui.tableWidgetDB.setRowCount(self.num_rows)
            self.ui.tableWidgetDB.setColumnCount(self.num_columns)
      
        
            tablerow = 0
            for row in self.datos:
                for column in range(self.num_columns):
                    self.ui.tableWidgetDB.setColumnWidth(column, 300)
                    self.ui.tableWidgetDB.setHorizontalHeaderLabels(self.title)
                    self.ui.tableWidgetDB.setItem(tablerow,column,QTableWidgetItem(str(row[column])))
                tablerow += 1
        except IndexError:
            print("The country is not in table")
        

    def update_item(self):
        try:
            table = self.table
            if table != "ecuador":
                title = self.title
                self.index = self.ui.cbx_insert.currentIndex()
                head_title = title[self.index]
        
                self.insert_data = self.ui.Qline_update.text()
                self.country_full_name = self.ui.Qline_country_update.text()
                self.data_base.update_data(table,head_title,self.insert_data,self.country_full_name)
                self.ui.Qline_update.clear()
                self.ui.Qline_country_update.clear()
            else:
                pass
        except IndexError:
            print("The country is not in table")
      
    def delete_item(self):
        try:
            table = self.table
            self.delete_register = self.ui.Qline_delete_country.text()
            self.data_base.delete_data(table,self.delete_register)
            self.ui.Qline_delete_country.clear()

        except IndexError:
            print("The country is not in table")   


    def table_ecu(self):
        table = "ecuador"
        [self.datos,self.title,self.num_rows,self.num_columns] = self.data_base.read_table(table)
        self.ui.ecu_tablewidget.setRowCount(self.num_rows)
        self.ui.ecu_tablewidget.setColumnCount(self.num_columns)
        
        self.list_cbx = ["Crecimiento del PIB per capita (% anual)",
             "Balanza comercial de bienes y servicios (% del PIB)",
             "Exportaciones de bienes y servicios (US$ a precios actuales)",
             "Gasto de consumo final de los hogares por crecimiento per capita (% anual)",
             "Gasto militar (% del PIB)",
             "Credito interno al sector privado (% del PIB)",
             "Inversion extranjera directa, entrada neta de capital (% del PIB)",
             "Renta del gas natural (% del PIB)",
             "Industria, valor agregado (% del PIB)",
             "PIB per capita (US$ a precios constantes de 2010)",
             "Ahorro interno bruto (% del PIB)",
             "Crecimiento del PIB (% anual)",
             "Masa monetaria (% del PIB)",
             "Rentas totales de los recursos naturales (% del PIB)",
             "Industrializacion, valor agregado (% del PIB)",
             "Comercio (% del PIB)",
             "Comercio de mercaderias (% del PIB)",
             "Rentas mineras  (% del PIB)"]  
    
        self.ui.Cbx_item_x.addItems(self.list_cbx)
        # self.ui.Cbx_item_y.addItems(list_cbx)
       
        tablerow = 0
        for row in self.datos:
            for column in range(self.num_columns):
                self.ui.ecu_tablewidget.setColumnWidth(column, 300)
                self.ui.ecu_tablewidget.setHorizontalHeaderLabels(self.title)
                self.ui.ecu_tablewidget.setItem(tablerow,column,QTableWidgetItem(str(row[column]).replace(",",".")))
            tablerow += 1

        

    def load_Stadistic_Item(self):
        self.index1 = self.ui.Cbx_item_x.currentIndex()
        var_x = list(self.datos[self.index1][:])
        data_x = var_x[2::]
        list_x= []
        for k in data_x:
            x = str(k).replace(",",".")
            list_x.append(float(x))
        return (list_x)


    def status_bar(self):
        sender = self.sender()
        message_toolbar = f'Event: "{sender.text()}" has been selected'
        self.statusBar().showMessage(message_toolbar)


    def close_window(self):
        self.close() 
       
class Canvas_scatter(FigureCanvas):
    
    def __init__(self, X , y,x_graph_label,y_graph_label): 
        plt.close('all')
        figure , ax = plt.subplots(1, dpi=100, figsize=(5, 5), 
            sharey=True, facecolor='white')
        super().__init__(figure)
        
        ax.plot(X,y,'o',color = 'tab:blue', markersize=7)

        ax.set_xlabel(x_graph_label, fontdict = {'fontsize':10, 'fontweight':'bold', 'color':'tab:blue'})
        ax.set_ylabel(y_graph_label)
        # ax.set_xlim([4,25])
        ax.grid(axis = 'y', color = 'gray', linestyle = 'dashed')
        ax.grid(axis = 'x', color = 'gray', linestyle = 'dashed')
        figure.suptitle('Scatter Plot', size=12, fontweight=BOLD)
        

class Canvas_Linear(FigureCanvas):
    
    def __init__(self, X,y,X1,theta_m,x_graph_label,y_graph_label):
        plt.close('all')     
        self.fig , self.ax = plt.subplots(1,dpi=100, figsize=(5, 5), 
            sharey=True, facecolor='white')
        super().__init__(self.fig) 
        self.ax.plot(X,y,'o',color = 'tab:gray', markersize=7)
        self.ax.plot(X,X1 @ theta_m, ':r')
        self.ax.set_xlabel(x_graph_label, fontdict = {'fontsize':10, 'fontweight':'bold', 'color':'tab:blue'})
        self.ax.set_ylabel(y_graph_label)
        self.ax.set_xlim([4,25])
        self.ax.grid(axis = 'y', color = 'gray', linestyle = 'dashed')
        self.ax.grid(axis = 'x', color = 'gray', linestyle = 'dashed')
        self.fig.suptitle(' Adjusted Line',size=12, fontweight=BOLD)
        


class Canvas_Bar(FigureCanvas):
    
    def __init__(self, X,y,x_label):
        plt.close('all')     
        self.fig , self.ax = plt.subplots(1,dpi=100, figsize=(5, 5), 
            sharey=True, facecolor='white')
        super().__init__(self.fig) 
        self.ax.bar(X,y)
        self.ax.set_xlabel(x_label, fontdict = {'fontsize':10, 'fontweight':'bold', 'color':'tab:blue'})
        
        self.ax.grid(axis = 'y', color = 'gray', linestyle = 'dashed')
        self.ax.grid(axis = 'x', color = 'gray', linestyle = 'dashed')
        self.fig.suptitle('Statistics per Indicator [2010 - 2020]',size=12, fontweight=BOLD)
import sys
import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView,
                             QComboBox, QPushButton, QLabel, QLineEdit, QFormLayout, 
                             QMessageBox, QFileDialog, QGroupBox)
from PySide6.QtCore import Qt
import data_manager
from chart_widget import DashboardChart

class DashboardApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dashboard Visualisasi Data Penjualan (T7-Week12)")
        self.resize(1100, 700)
        
        data_manager.init_database()
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        
        left_panel = QVBoxLayout()
        main_layout.addLayout(left_panel, stretch=2)
        
        form_group = QGroupBox("Tambah Data Penjualan")
        form_layout = QFormLayout()
        self.input_tgl = QLineEdit()
        self.input_tgl.setPlaceholderText("YYYY-MM-DD")
        self.input_kat = QComboBox()
        self.input_kat.addItems(['Elektronik', 'Fashion', 'Makanan', 'Kesehatan', 'Otomotif'])
        self.input_prod = QLineEdit()
        self.input_jml = QLineEdit()
        self.input_hrg = QLineEdit()
        
        form_layout.addRow("Tanggal:", self.input_tgl)
        form_layout.addRow("Kategori:", self.input_kat)
        form_layout.addRow("Nama Produk:", self.input_prod)
        form_layout.addRow("Jumlah:", self.input_jml)
        form_layout.addRow("Harga Satuan:", self.input_hrg)
        
        btn_add = QPushButton("Simpan Data")
        btn_add.setStyleSheet("background-color: #2ecc71; color: white; font-weight: bold;")
        btn_add.clicked.connect(self.add_data_handler)
        form_layout.addRow(btn_add)
        form_group.setLayout(form_layout)
        left_panel.addWidget(form_group)
        
        control_group = QGroupBox("Kontrol Data & Filter")
        control_layout = QVBoxLayout()
        
        control_layout.addWidget(QLabel("Filter Kategori Chart & Tabel:"))
        self.filter_combobox = QComboBox()
        self.filter_combobox.addItems(["Semua Kategori", "Elektronik", "Fashion", "Makanan", "Kesehatan", "Otomotif"])
        self.filter_combobox.currentTextChanged.connect(self.refresh_dashboard)
        control_layout.addWidget(self.filter_combobox)
        
        control_layout.addWidget(QLabel("Tipe Tampilan Grafik:"))
        self.chart_type_combobox = QComboBox()
        self.chart_type_combobox.addItems(["Bar + Pie", "Tren Garis (Line)"])
        self.chart_type_combobox.currentTextChanged.connect(self.refresh_dashboard)
        control_layout.addWidget(self.chart_type_combobox)
        
        btn_delete = QPushButton("Hapus Baris Terpilih (CRUD - Delete)")
        btn_delete.setStyleSheet("background-color: #e74c3c; color: white;")
        btn_delete.clicked.connect(self.delete_data_handler)
        control_layout.addWidget(btn_delete)
        
        btn_refresh = QPushButton("Refresh Dashboard")
        btn_refresh.clicked.connect(self.refresh_dashboard)
        control_layout.addWidget(btn_refresh)
        
        btn_export = QPushButton("Export Chart ke PNG")
        btn_export.setStyleSheet("background-color: #34495e; color: white;")
        btn_export.clicked.connect(self.export_chart_handler)
        control_layout.addWidget(btn_export)
        
        control_group.setLayout(control_layout)
        left_panel.addWidget(control_group)
        
        right_panel = QVBoxLayout()
        main_layout.addLayout(right_panel, stretch=3)
        
        right_panel.addWidget(QLabel("Data Mentah (SQLite):"))
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(7)
        self.table_widget.setHorizontalHeaderLabels(["ID", "Tanggal", "Kategori", "Produk", "Jumlah", "Harga", "Total"])
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        right_panel.addWidget(self.table_widget)
        
        right_panel.addWidget(QLabel("Visualisasi Chart Interaktif (Matplotlib):"))
        self.canvas = DashboardChart(self, width=6, height=4, dpi=100)
        right_panel.addWidget(self.canvas)
        
        self.refresh_dashboard()
        
    def refresh_dashboard(self):
        selected_filter = self.filter_combobox.currentText()
        selected_chart = self.chart_type_combobox.currentText()
        
        df = data_manager.get_all_data(selected_filter)
        
        self.table_widget.setRowCount(0)
        for index, row in df.iterrows():
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            self.table_widget.setItem(row_position, 0, QTableWidgetItem(str(row['id'])))
            self.table_widget.setItem(row_position, 1, QTableWidgetItem(str(row['tanggal'])))
            self.table_widget.setItem(row_position, 2, QTableWidgetItem(str(row['kategori'])))
            self.table_widget.setItem(row_position, 3, QTableWidgetItem(str(row['produk'])))
            self.table_widget.setItem(row_position, 4, QTableWidgetItem(str(row['jumlah'])))
            self.table_widget.setItem(row_position, 5, QTableWidgetItem(f"Rp {row['harga']:.0f}"))
            self.table_widget.setItem(row_position, 6, QTableWidgetItem(f"Rp {row['total']:.0f}"))
            
        self.canvas.update_charts(df, selected_chart)

    def add_data_handler(self):
        tgl = self.input_tgl.text().strip()
        kat = self.input_kat.currentText()
        prod = self.input_prod.text().strip()
        jml = self.input_jml.text().strip()
        hrg = self.input_hrg.text().strip()
        
        if not (tgl and prod and jml and hrg):
            QMessageBox.warning(self, "Input Error", "Semua kolom form input wajib diisi!")
            return
            
        try:
            data_manager.insert_data(tgl, kat, prod, int(jml), float(hrg))
            QMessageBox.information(self, "Sukses", "Data berhasil ditambahkan ke database!")
            self.refresh_dashboard()
            self.input_tgl.clear()
            self.input_prod.clear()
            self.input_jml.clear()
            self.input_hrg.clear()
        except Exception as e:
            QMessageBox.critical(self, "Error Database", f"Gagal menyimpan data: {str(e)}")

    def delete_data_handler(self):
        current_row = self.table_widget.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Pilih Baris", "Silakan klik baris pada tabel yang ingin dihapus terlebih dahulu.")
            return
            
        data_id = self.table_widget.item(current_row, 0).text()
        confirm = QMessageBox.question(self, "Konfirmasi Hapus", f"Apakah Anda yakin ingin menghapus data dengan ID {data_id}?",
                                     QMessageBox.Yes | QMessageBox.No)
        
        if confirm == QMessageBox.Yes:
            data_manager.delete_data(int(data_id))
            self.refresh_dashboard()
            QMessageBox.information(self, "Sukses", "Data berhasil dihapus dari database!")

    def export_chart_handler(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Chart Image", os.getcwd(), "PNG Files (*.png)")
        if file_path:
            self.canvas.fig.savefig(file_path, dpi=300)
            QMessageBox.information(self, "Export Sukses", f"Grafik dashboard berhasil disimpan ke:\n{file_path}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DashboardApp()
    window.show()
    sys.exit(app.exec())
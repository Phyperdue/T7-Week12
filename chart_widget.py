import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class DashboardChart(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)
        self.setParent(parent)
        
    def update_charts(self, df, chart_type="Bar + Pie"):
        self.fig.clear()
        
        if df.empty:
            ax = self.fig.add_subplot(111)
            ax.text(0.5, 0.5, 'Tidak ada data untuk visualisasi', ha='center', va='center')
            self.draw()
            return

        if chart_type == "Bar + Pie":
            ax1 = self.fig.add_subplot(121)
            ax2 = self.fig.add_subplot(122)
            
            kat_summary = df.groupby('kategori')['total'].sum()
            kat_summary.plot(kind='bar', ax=ax1, color='#3498db')
            ax1.set_title("Total Penjualan / Kategori")
            ax1.set_xlabel("Kategori")
            ax1.set_ylabel("Total (Rp)")
            ax1.tick_params(axis='x', rotation=45)
            
            prod_summary = df.groupby('kategori')['jumlah'].sum()
            prod_summary.plot(kind='pie', ax=ax2, autopct='%1.1f%%', startangle=90, 
                             colors=['#2ecc71','#e74c3c','#f1c40f','#9b59b6','#34495e'])
            ax2.set_title("Proporsi Kuantitas Item")
            ax2.set_ylabel("")
            
        elif chart_type == "Tren Garis (Line)":
            ax = self.fig.add_subplot(111)
            df['tanggal'] = df['tanggal'].astype(str)
            tren_summary = df.groupby('tanggal')['total'].sum().sort_index()
            tren_summary.plot(kind='line', ax=ax, marker='o', color='#e67e22', linewidth=2)
            ax.set_title("Tren Penjualan Harian")
            ax.set_xlabel("Tanggal")
            ax.set_ylabel("Total Pendapatan")
            ax.grid(True, linestyle='--', alpha=0.6)
            ax.tick_params(axis='x', rotation=45)
            
        self.fig.tight_layout()
        self.draw()
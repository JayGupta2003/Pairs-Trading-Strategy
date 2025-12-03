from fpdf import FPDF # type: ignore
from datetime import datetime
import pandas as pd

class PDFReport(FPDF):
    def header(self):
        # Logo or Brand Name
        self.set_font('Helvetica', 'B', 20)
        self.cell(0, 10, 'Pairs-Trading Strategy Daily Briefing', border=False, ln=True, align='L')
        
        # Date
        self.set_font('Helvetica', 'I', 10)
        self.cell(0, 10, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}', ln=True, align='L')
        self.ln(5) # Line break

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

def create_daily_report(opportunities):
    """
    opportunities: List of dictionaries containing signal details and chart paths.
    """
    if not opportunities:
        print("No opportunities to report.")
        return

    pdf = PDFReport()
    pdf.set_auto_page_break(auto=True, margin=15)

    # --- PAGE 1: EXECUTIVE SUMMARY ---
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 16)
    pdf.cell(0, 10, f'Executive Summary: {len(opportunities)} Active Signals', ln=True)
    pdf.ln(5)

    # Summary Table Header
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_fill_color(200, 200, 200) # Grey background
    
    # Cols: Pair, Sector, Z-Score, Hist Sharpe, Action
    pdf.cell(30, 10, 'Pair', 1, 0, 'C', fill=True)
    pdf.cell(40, 10, 'Sector', 1, 0, 'C', fill=True)
    pdf.cell(25, 10, 'Z-Score', 1, 0, 'C', fill=True)
    pdf.cell(30, 10, 'Hist. Sharpe', 1, 0, 'C', fill=True)
    pdf.cell(35, 10, 'Action', 1, 1, 'C', fill=True) # ln=1 moves to next line

    # Table Rows
    pdf.set_font('Helvetica', '', 10)
    for op in opportunities:
        pdf.cell(30, 10, f"{op['Stock A']}-{op['Stock B']}", 1)
        pdf.cell(40, 10, op['Sector'][:15], 1) # Truncate long sectors
        
        # Color the Z-Score
        z = op['Z-Score']
        pdf.set_text_color(0, 100, 0) if z < 0 else pdf.set_text_color(200, 0, 0)
        pdf.cell(25, 10, f"{z:.2f}", 1, 0, 'C')
        pdf.set_text_color(0, 0, 0) # Reset color
        
        pdf.cell(30, 10, f"{op['Sharpe']:.2f}", 1, 0, 'C')
        pdf.cell(35, 10, op['Signal_Type'], 1, 1, 'C')

    # --- PAGE 2+: DEEP DIVES ---
    for op in opportunities:
        pdf.add_page()
        
        # Title
        pdf.set_font('Helvetica', 'B', 16)
        pdf.cell(0, 10, f"Deep Dive: {op['Stock A']} vs {op['Stock B']}", ln=True)
        
        # Metrics Row
        pdf.set_font('Helvetica', '', 12)
        pdf.cell(0, 8, f"Sector: {op['Sector']} | Hedge Ratio: {op['Ratio']:.3f}", ln=True)
        pdf.cell(0, 8, f"Action: {op['Signal_Type']} | Historical Sharpe: {op['Sharpe']:.2f}", ln=True)
        pdf.ln(5)
        
        # Insert Chart
        # Width 190mm fits nicely on A4
        if op['Chart_Path']:
            try:
                pdf.image(op['Chart_Path'], x=10, y=pdf.get_y(), w=190)
            except Exception as e:
                pdf.cell(0, 10, f"Error loading chart: {e}", ln=True)

    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"../reports/Daily_Brief_{date_str}.pdf"
    pdf.output(filename)
    print(f"\n✅ PDF Report generated: {filename}")
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape, ELEVENSEVENTEEN
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import pandas as pd

class ReportGenerator:
    def __init__(self, filename="downtime_report.pdf"):
        self.filename = filename
        self.doc = SimpleDocTemplate(
            filename,
            pagesize=landscape(ELEVENSEVENTEEN),
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
    def generate_report(self, df):
        """
        Generate a PDF report from a pandas DataFrame
        
        Args:
            df (pandas.DataFrame): DataFrame containing the downtime data
        """
        # Convert DataFrame to a list of lists for ReportLab
        data = [df.columns.tolist()]  # Header row
        data.extend(df.values.tolist())
        
        # Create the table
        table = Table(data)
        
        # Add basic table styling
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        # Build the PDF
        self.doc.build([table])
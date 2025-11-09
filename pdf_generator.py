
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os
from datetime import datetime

class MazePDFGenerator:
    def __init__(self, output_dir, logger=None):
        self.output_dir = output_dir
        self.logger = logger

    def save_pdf(self, maze_img, solution_img, filename=None):
        os.makedirs(self.output_dir, exist_ok=True)
        if not filename:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"maze_{ts}.pdf"
        pdf_path = os.path.join(self.output_dir, filename)
        c = canvas.Canvas(pdf_path, pagesize=letter)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(220, 760, "Maze Puzzle")
        c.drawImage(maze_img, 50, 200, width=500, height=500)
        c.showPage()
        c.setFont("Helvetica-Bold", 16)
        c.drawString(220, 760, "Maze Solution")
        c.drawImage(solution_img, 50, 200, width=500, height=500)
        c.save()
        if self.logger: self.logger.info(f"PDF saved to {pdf_path}")
        return pdf_path

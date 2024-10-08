import wikipedia
import queue
import sys
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


from backend.tools.paraphraser import paraphrase

from wikipedia.exceptions import DisambiguationError, PageError
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pdfs_folder = os.path.join(base_dir, 'pdfs')  

    
def check_folder():
    if not os.path.exists(pdfs_folder):
        os.makedirs(pdfs_folder)

def pdfHandler(num_pages: int) -> list: # Type safe   
    paths = []
    check_folder()
    
    if not (0 <= num_pages <= 5):
        raise ValueError("Value must be an integer between 0 and 5 (inclusive).")
    
    for i in range(0, num_pages):
        page = None
        while not page:
            try:
                page = wikipedia.page(wikipedia.random())
                logger.info(f"Page: {page.title}")
            except DisambiguationError as e:
                logger.error(f"DisambiguationError: {e}, trying another page")
                page = None  # Retry on disambiguation error
        
        if page != None:
            pdfContent = queue.Queue()
            content = page.content.strip()
            content = page.content.split('\n')

            temp = ""
            for i in range(len(content)):
                if "==" in content[i]:
                    pdfContent.put((temp, 2))
                    pdfContent.put((content[i], 1))
                else:
                    temp = temp + content[i]

            yCoordinate = 750
            c = canvas.Canvas(f"pdfs/{page.title}.pdf", pagesize=letter)

            max_y_coordinate = 750  
            min_y_coordinate = 50  

            
            while not pdfContent.empty():
                result = pdfContent.get()
                
                if result[1] == 1:
                    c.setFont("Helvetica-Bold", 14) 
                elif result[1] == 2 and result[0] != '':
                    c.setFont("Helvetica", 12)  
                    result = (paraphrase(result[0]), result[1])
                
                text = result[0]
                words = text.split(' ')
                current_line = ''
                
                for word in words:
                    if len(current_line) + len(word) + 1 > 80:
                        if yCoordinate < min_y_coordinate:
                            c.showPage()
                            c.setFont("Helvetica-Bold", 14) if result[1] == 1 else c.setFont("Helvetica", 12)
                            yCoordinate = max_y_coordinate
                        
                        c.drawString(50, yCoordinate, current_line)
                        current_line = word
                        yCoordinate -= 20
                    else:
                        if current_line:
                            current_line += ' '
                        current_line += word
                
                if current_line:
                    if yCoordinate < min_y_coordinate:
                        c.showPage()
                        c.setFont("Helvetica-Bold", 14) if result[1] == 1 else c.setFont("Helvetica", 12)
                        yCoordinate = max_y_coordinate

                    c.drawString(50, yCoordinate, current_line)

                yCoordinate -= 20 
        
            c.save()
            logger.info(f"PDF created for {page.title}")
            pdfPath = os.path.join(f"{pdfs_folder}", f"{page.title}.pdf")
            paths.append(pdfPath)

    return paths
        
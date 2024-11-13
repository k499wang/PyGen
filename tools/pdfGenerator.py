import wikipedia
import queue
import argparse
import logging
from tools.utils import check_folder

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PyGen")

from tools.paraphraser import paraphrase
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from wikipedia import DisambiguationError

folder_path = "pdfs/"


def pdfGenerate(num_pages: int) -> None: # Type safe   
    logger.info(f"Creating directory '{folder_path}' to store the PDFs.")
    check_folder(folder_path)

    for i in range(0, num_pages):
        page = None
        
        while not page:
            try:
                page = wikipedia.page(wikipedia.random())
                                
                try:                     
                    pdfContent = queue.Queue() # Queue to store the content of the page
                    content = page.content.strip()
                    content = page.content.split('\n')
                    

                    temp = ""
                    for i in range(len(content)):
                        if "==" in content[i] and "external links".lower() not in content[i].lower(): # A title will have "==" in it
                            if temp:
                                pdfContent.put((temp.replace("==", ""), 2))  # Store the content in the queue
                            pdfContent.put((content[i], 1))
                            temp = ""
                        else:
                            temp = temp + content[i]
                            
                            

                    yCoordinate = 750
                    c = canvas.Canvas(f"pdfs/{page.title}.pdf", pagesize=letter)

                    max_y_coordinate = 750  
                    min_y_coordinate = 50  

                    c.setFont("Helvetica-Bold", 24)
                    title_width = c.stringWidth(page.title, "Helvetica-Bold", 24)
                    page_width = letter[0]
                    page_height = letter[1]
                    x_centered = (page_width - title_width) / 2
                    y_centered = page_height - 50  # Place near top of page, adjust 50 as needed
                    c.drawString(x_centered, y_centered, page.title)
                    
                    c.setFont("Helvetica-Bold", 14)
                    c.drawString(50, y_centered-50, "Summary")
                    
                    c.setFont("Helvetica", 12)
                    
                    ySumm = y_centered-100
                    summLine = ""
                    summ = page.summary.split(' ')
                    for word in summ:
                        if len(summLine) + len(word) + 1 > 80:
                            c.drawString(50, ySumm, summLine)
                            summLine = word
                            ySumm -= 20
                        else:
                            if summLine:
                                summLine += ' '
                            summLine += word
                            
                    if summLine:  # Draw the last line
                        c.drawString(50, ySumm, summLine)                           
                        
                            
                        
                    
                    c.showPage()
                    
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
                            if len(current_line) + len(word) + 1 > 80: # 80 characters per line, wrap text
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
                            if yCoordinate < min_y_coordinate: # If the text goes beyond the page, create a new page
                                c.showPage()
                                c.setFont("Helvetica-Bold", 14) if result[1] == 1 else c.setFont("Helvetica", 12)
                                yCoordinate = max_y_coordinate

                            c.drawString(50, yCoordinate, current_line)

                        yCoordinate -= 20 
                
                    c.showPage()
                    
                    c.setFont("Helvetica-Bold", 24)
                    c.drawString(50, 750 , "External Links")
                    
                    yRef = 720
                    
                    for link in page.links:
                        if yRef < min_y_coordinate: # doubt links will be bigger than one page, but fills in stuff
                            c.showPage()
                            c.setFont("Helvetica-Bold", 14)
                            yRef = max_y_coordinate
                            
                        c.setFont("Helvetica", 12)
                        c.drawString(50, yRef, link)
                        yRef -= 20
                    
                    c.save()
                    logger.info(f"PDF created for {page.title}")
                
                except Exception as e:
                    print("ERROR: ", e)
                    print("Trying another page")
                    page = None


            except DisambiguationError as e:
                logger.error(f"DisambiguationError: {e}, trying another page")
                page = None  # Retry on disambiguation error
            except Exception as e:
                logger.error(f"Error: {e}, trying another page")
                page = None  # Retry on any other error
        
        
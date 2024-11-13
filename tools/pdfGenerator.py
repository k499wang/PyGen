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
                                
                # try:                     
                #     pdfContent = queue.Queue() # Queue to store the content of the page
                #     pageTitle = page.title
                #     sections = page.sections
                            
                            

                #     yCoordinate = 750
                #     c = canvas.Canvas(f"pdfs/{page.title}.pdf", pagesize=letter)

                #     max_y_coordinate = 750  
                #     min_y_coordinate = 50  

                    
                #     while not pdfContent.empty():
                #         result = pdfContent.get()
                        
                #         if result[1] == 1:
                #             c.setFont("Helvetica-Bold", 14) 
                #         elif result[1] == 2 and result[0] != '':
                #             c.setFont("Helvetica", 12)  
                #             result = (paraphrase(result[0]), result[1])
                        
                #         text = result[0]
                #         words = text.split(' ')
                #         current_line = ''
                        
                #         for word in words:
                #             if len(current_line) + len(word) + 1 > 80: # 80 characters per line, wrap text
                #                 if yCoordinate < min_y_coordinate:
                #                     c.showPage()
                #                     c.setFont("Helvetica-Bold", 14) if result[1] == 1 else c.setFont("Helvetica", 12)
                #                     yCoordinate = max_y_coordinate
                                
                #                 c.drawString(50, yCoordinate, current_line)
                #                 current_line = word
                #                 yCoordinate -= 20
                #             else:
                #                 if current_line:
                #                     current_line += ' '
                #                 current_line += word
                        
                #         if current_line:
                #             if yCoordinate < min_y_coordinate: # If the text goes beyond the page, create a new page
                #                 c.showPage()
                #                 c.setFont("Helvetica-Bold", 14) if result[1] == 1 else c.setFont("Helvetica", 12)
                #                 yCoordinate = max_y_coordinate

                #             c.drawString(50, yCoordinate, current_line)

                #         yCoordinate -= 20 
                
                #     c.save()
                #     logger.info(f"PDF created for {page.title}")
                
                # except Exception as e:
                #     print("ERROR: ", e)
                #     print("Trying another page")
                #     page = None


            except DisambiguationError as e:
                logger.error(f"DisambiguationError: {e}, trying another page")
                page = None  # Retry on disambiguation error
            except Exception as e:
                logger.error(f"Error: {e}, trying another page")
                page = None  # Retry on any other error
        
       
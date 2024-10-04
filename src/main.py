import wikipedia
import sys
import queue
import os


from src.paraphraser import paraphrase
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
folder_path = "pdfs/"

if __name__ == "__main__":
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Directory '{folder_path}' created.")
    else:
        print(f"Directory '{folder_path}' already exists.")
    
    
    for i in range(0,1):
        try:
            page = wikipedia.page(wikipedia.random())
            print(page.title)
        except wikipedia.exceptions.PageError as e:
            print(e)

        pdfContent = queue.Queue()
        content = page.content.strip()
        content = page.content.split('\n')

        print(page.content)

        for i in range(len(content)):
            if "==" in content[i]:
                pdfContent.put((content[i], 1))
            else:
                pdfContent.put((content[i], 2))

        yCoordinate = 750
        c = canvas.Canvas(folder_path + page.title + ".pdf", pagesize=letter)

        max_y_coordinate = 750  
        min_y_coordinate = 50  

        while not pdfContent.empty():
            result = pdfContent.get()

            if result[1] == 1:
                c.setFont("Helvetica-Bold", 14) 
            else:
                c.setFont("Helvetica", 12)  
            
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

            




        

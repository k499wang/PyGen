import wikipedia
import queue
import os
import argparse

from tools.paraphraser import paraphrase
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


folder_path = "pdfs/"

def main(pages_count):
    
    ## Create a directory to store the PDFs
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Directory '{folder_path}' created.")
    else:
        print(f"Directory '{folder_path}' already exists.")

    ## Fetch random Wikipedia pages and generate PDFs
    for i in range(pages_count):
        try:
            page = wikipedia.page(wikipedia.random())
            print(page.title)
        except wikipedia.exceptions.PageError as e:
            print(e)
            break

        pdfContent = queue.Queue()
        content = page.content.strip().split('\n')

        for line in content:
            if "==" in line:
                pdfContent.put((line, 1))
            elif line.strip() != '':
                pdfContent.put((line, 2))

        yCoordinate = 750
        c = canvas.Canvas(folder_path + page.title + ".pdf", pagesize=letter)

        max_y_coordinate = 750  
        min_y_coordinate = 50  

        while not pdfContent.empty():
            result = pdfContent.get()
            print(result[0])

            if result[1] == 1:
                c.setFont("Helvetica-Bold", 14)
            elif result[1] == 2:
                c.setFont("Helvetica", 12)
                result = (paraphrase(result[0]), result[1])

            text = result[0]
            words = text.split(' ')
            current_line = ''

            for word in words:
                if len(current_line) + len(word) + 1 > 80:
                    if yCoordinate < min_y_coordinate: ## Move to the next page
                        c.showPage()
                        c.setFont("Helvetica-Bold", 14) if result[1] == 1 else c.setFont("Helvetica", 12)
                        yCoordinate = max_y_coordinate
                    
                    c.drawString(50, yCoordinate, current_line)
                    current_line = word
                    yCoordinate -= 20
                else: ## Add the word to the current line
                    if current_line:
                        current_line += ' '
                    current_line += word 

            ## Print the last line
            if current_line:
                if yCoordinate < min_y_coordinate:
                    c.showPage()
                    c.setFont("Helvetica-Bold", 14) if result[1] == 1 else c.setFont("Helvetica", 12)
                    yCoordinate = max_y_coordinate

                c.drawString(50, yCoordinate, current_line)

            yCoordinate -= 20

        c.save()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate PDFs from random Wikipedia pages.")
    parser.add_argument("pages", type=int, help="Number of random Wikipedia pages to fetch.")
    args = parser.parse_args()
    main(args.pages)

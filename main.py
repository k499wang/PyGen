from tools.pdfGenerator import pdfGenerate

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate PDFs from random Wikipedia pages.")
    parser.add_argument("pages", type=int, help="Number of random Wikipedia pages to fetch.")
    args = parser.parse_args()
    pdfGenerate(args.pages)

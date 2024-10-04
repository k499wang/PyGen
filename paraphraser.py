import google.generativeai as genai
import os

def paraphrase(text):
    paraphraser = genai.Paraphraser()
    paraphrase = paraphraser.paraphrase(text)
    return paraphrase


    


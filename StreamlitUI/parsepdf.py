import pdftotext
class PdfParse:
    def parser(self):   
        with open("final.pdf", "rb") as f:
            pdf = pdftotext.PDF(f)
        finalpg=[]
        for page in pdf:
            pg=page.strip()
            finalpg.append(pg)
        return type(finalpg)
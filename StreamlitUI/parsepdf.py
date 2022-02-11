import pdftotext
class PdfParse:
    def parser(self,file):   
        with open(file, "rb") as f:
            pdf = pdftotext.PDF(f)
        finalpg=[]
        for page in pdf:
            pg=page.strip()
            finalpg.append(pg)
        return finalpg
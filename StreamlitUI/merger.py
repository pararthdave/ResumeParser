path='/content/dataset' #file path for corpus
files = [os.path.join (path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
pdfs = []
for i in files:
    pdfs.append(i)

merger = PyPDF2.PdfFileMerger(strict=False)

for pdf in pdfs:
    merger.append(pdf)

merger.write("final.pdf")

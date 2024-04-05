import PyPDF2 

def juntar_pdf(arquivos, novo):
    pdf_writer = PyPDF2.PdfWriter()

    for arquivo in arquivos:
        pdf_reader = PyPDF2.PdfReader(arquivo)
        PyPDF2.PdfMerger()
        
        
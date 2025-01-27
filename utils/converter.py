import fitz 
import os
import tempfile

def converter_arquivos(caminho_arquivo):
    print(f"Processando arquivo: {caminho_arquivo}")
    
    
    pdf_path = caminho_arquivo
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    doc = fitz.open(pdf_path)
    
    
    png_files = []

   
    zoom_x = 1.5  
    zoom_y = 1.5  
    mat = fitz.Matrix(zoom_x, zoom_y)

    
    temp_dir = tempfile.gettempdir()

    for i, page in enumerate(doc):
        
        pix = page.get_pixmap(matrix=mat)
        
        png_file_path = os.path.join(temp_dir, f"{base_name}_pagina_{i}.png")
        
        pix.save(png_file_path)
        
        png_files.append(png_file_path)

    doc.close()

    
    return png_files

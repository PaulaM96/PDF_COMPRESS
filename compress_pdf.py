import fitz  # PyMuPDF
import shutil

# Caminho do PDF de entrada
input_pdf_path = r'\\servidor\ex.pdf'
# Caminho do PDF de saída temporário
output_pdf_path = r'\\servidor\comp.pdf'
# Caminho do PDF de saída final
final_output_path = r'\\sservidor\excomp.pdf'

# Função para comprimir uma imagem (usando Pillow)
def compress_image(img_data, quality=75):
    from PIL import Image
    import io
    
    # Carregar imagem usando Pillow
    img = Image.open(io.BytesIO(img_data))
    
    # Comprimir a imagem
    output = io.BytesIO()
    img.save(output, format='JPEG', quality=quality)
    return output.getvalue()

# Abrir o PDF de entrada
pdf_document = fitz.open(input_pdf_path)

# Otimizar e comprimir o PDF
for page in pdf_document:
    images = page.get_images(full=True)
    for img_index, img_info in enumerate(images.items()):
        xref, img_props = img_info
        
        # Extrair imagem
        base_image = pdf_document.extract_image(xref)
        image_bytes = base_image["image"]

        # Comprimir a imagem
        compressed_data = compress_image(image_bytes)

        # Substituir imagem original com a comprimida
        pix = fitz.Pixmap(compressed_data)
        pdf_document.update_image(xref, pix)

# Salvar o PDF otimizado
pdf_document.save(output_pdf_path, deflate=True)
pdf_document.close()

# Mover o PDF comprimido para o caminho final
shutil.move(output_pdf_path, final_output_path)

print(f"PDF comprimido salvo em: {final_output_path}")


# Mover o PDF comprimido para o caminho final
shutil.move(output_pdf_path, final_output_path)

print(f"PDF comprimido salvo em: {final_output_path}")

import os
import hashlib
import json
from datetime import datetime
from PIL import Image
import piexif

def calculate_sha256(filepath):
    """Calcula o hash SHA-256 de um arquivo."""
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def prepare_xmp(template_path, image_path, record_link="https://github.com/christianmontgomery220-svg/anonymo-hybrid-image"):
    """Lê o template XMP, preenche os placeholders e retorna a string XMP."""
    with open(template_path, 'r', encoding='utf-8') as f:
        xmp_content = f.read()
    
    # Calcular hash da imagem original (antes de injetar XMP)
    image_hash = calculate_sha256(image_path)
    
    # Preencher placeholders
    xmp_content = xmp_content.replace("[INSERT_SHA256_HASH]", image_hash)
    xmp_content = xmp_content.replace("[INSERT_DOI_OR_RECORD_LINK]", record_link)
    
    # Atualizar datas para o momento atual
    current_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S-03:00")
    xmp_content = xmp_content.replace('xmp:CreateDate="2026-03-23T00:00:00-03:00"', f'xmp:CreateDate="{current_time}"')
    xmp_content = xmp_content.replace('xmp:ModifyDate="2026-03-23T00:00:00-03:00"', f'xmp:ModifyDate="{current_time}"')
    
    return xmp_content, image_hash

def embed_xmp_to_image(image_path, xmp_content, output_path):
    """Injeta o conteúdo XMP em uma imagem JPEG ou PNG."""
    # Para JPEG, podemos usar piexif ou PIL
    # O PIL suporta salvar XMP diretamente em JPEGs e PNGs
    
    img = Image.open(image_path)
    
    # Preparar metadados EXIF básicos se não existirem
    exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}
    try:
        if "exif" in img.info:
            exif_dict = piexif.load(img.info["exif"])
    except Exception:
        pass
        
    # Inserir um comentário básico no EXIF indicando a presença do XMP
    exif_dict["0th"][piexif.ImageIFD.ImageDescription] = b"Anonymo AI / TCF-TFB Visual Asset - Hybrid Provenance"
    exif_bytes = piexif.dump(exif_dict)
    
    # Salvar a imagem com o XMP
    img.save(output_path, "jpeg", exif=exif_bytes, xmp=xmp_content.encode('utf-8'))
    print(f"✅ Imagem salva com sucesso em: {output_path}")
    print(f"✅ Metadados XMP injetados com sucesso!")

def update_manifest_and_metadata(metadata_path, manifest_path, image_filename, image_hash, record_link):
    """Atualiza os arquivos JSON com os dados reais da imagem."""
    # Atualizar metadata.json
    with open(metadata_path, 'r', encoding='utf-8') as f:
        metadata = json.load(f)
    
    metadata["asset_filename"] = image_filename
    metadata["asset_hash"] = image_hash
    metadata["record_link"] = record_link
    metadata["date_created"] = datetime.now().strftime("%Y-%m-%d")
    
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)
        
    # Atualizar manifest.json
    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest = json.load(f)
        
    manifest["integrity"]["file"] = image_filename
    manifest["integrity"]["hash"] = image_hash
    manifest["links"]["registry"] = record_link
    manifest["status"] = "final_asset_embedded"
    
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2)
        
    print("✅ Arquivos metadata.json e manifest.json atualizados com sucesso!")

if __name__ == "__main__":
    # Configurações
    base_dir = "/home/ubuntu/anonymo-hybrid-image"
    template_path = os.path.join(base_dir, "TEMPLATE_XMP.xml")
    input_image = os.path.join(base_dir, "sample_hybrid_image.jpg")
    output_image = os.path.join(base_dir, "sample_hybrid_image_with_xmp.jpg")
    metadata_path = os.path.join(base_dir, "metadata.json")
    manifest_path = os.path.join(base_dir, "manifest.json")
    
    # Criar uma imagem de exemplo simples se não existir
    if not os.path.exists(input_image):
        print("Criando imagem de exemplo...")
        img = Image.new('RGB', (800, 600), color = (73, 109, 137))
        img.save(input_image)
    
    print("1. Preparando XMP a partir do template...")
    xmp_content, image_hash = prepare_xmp(template_path, input_image)
    print(f"   Hash SHA-256 da imagem original: {image_hash}")
    
    print("\n2. Injetando XMP na imagem...")
    embed_xmp_to_image(input_image, xmp_content, output_image)
    
    print("\n3. Atualizando manifestos JSON...")
    update_manifest_and_metadata(
        metadata_path, 
        manifest_path, 
        "sample_hybrid_image_with_xmp.jpg", 
        image_hash, 
        "https://github.com/christianmontgomery220-svg/anonymo-hybrid-image"
    )
    
    print("\nProcesso concluído com sucesso! A imagem híbrida agora contém a prova de existência embutida.")

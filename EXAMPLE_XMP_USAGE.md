# Exemplo de Uso: `TEMPLATE_XMP.xml` em Imagem Híbrida

Este documento descreve como utilizar o `TEMPLATE_XMP.xml` para incorporar metadados de proveniência em imagens criadas sob o framework **Anonymo AI / TCF-TFB**, declarando autoria híbrida (humano + IA).

---

## O que é XMP e por que usá-lo?

**XMP (Extensible Metadata Platform)** é um padrão ISO (ISO 16684-1) criado pela Adobe que permite embutir metadados estruturados diretamente no binário de arquivos de imagem (JPEG, PNG, TIFF, etc.) usando RDF/XML. Diferentemente de metadados externos (como arquivos `.json` separados), o XMP viaja junto com a imagem — ela carrega sua própria prova de existência e autoria.

Para imagens híbridas (criadas com participação humana e assistência de IA), o XMP é especialmente valioso porque:

- Registra de forma permanente e verificável **quem criou**, **como foi criado** e **sob qual framework intelectual**;
- Suporta **namespaces customizados** (como o `anonymo:` deste pacote), permitindo campos específicos do framework TCF/TFB;
- É lido nativamente por ferramentas como Adobe Bridge, Lightroom, ExifTool e qualquer software compatível com o padrão.

---

## Estrutura do Template

O `TEMPLATE_XMP.xml` utiliza os seguintes namespaces:

| Namespace | Prefixo | Finalidade |
|---|---|---|
| Dublin Core | `dc:` | Título, criador, direitos, descrição, assuntos |
| XMP Basic | `xmp:` | Datas de criação/modificação, ferramenta criadora |
| XMP Rights | `xmpRights:` | Marcação de direitos e URL de declaração |
| Photoshop | `photoshop:` | Crédito do autor |
| IPTC Core | `Iptc4xmpCore:` | Informações de contato (ORCID) |
| **Anonymo** | `anonymo:` | **Namespace customizado** — campos exclusivos do framework TCF/TFB |

### Campos do namespace `anonymo:`

| Campo | Valor no template | Descrição |
|---|---|---|
| `anonymo:OriginalAuthorship` | `Human` | Declara que a autoria original é humana |
| `anonymo:CreationType` | `Human-AI Hybrid` | Tipo de criação |
| `anonymo:AIAssistance` | `Yes` | Indica uso de IA no workflow |
| `anonymo:IntellectualFramework` | `TCF/TFB` | Framework intelectual aplicado |
| `anonymo:Project` | `Anonymo AI` | Nome do projeto |
| `anonymo:ORCID` | `0009-0009-5364-249X` | Identificador do autor |
| `anonymo:IntegrityHash` | `[INSERT_SHA256_HASH]` | **Placeholder** — hash SHA-256 da imagem |
| `anonymo:RecordLink` | `[INSERT_DOI_OR_RECORD_LINK]` | **Placeholder** — DOI ou link de registro público |

---

## Pré-requisitos

```bash
pip install Pillow piexif
```

---

## Como usar o script `embed_xmp.py`

O script `embed_xmp.py` automatiza todo o processo em três etapas:

### 1. Calcular o hash SHA-256 da imagem original

Antes de qualquer modificação, o hash é calculado sobre o arquivo original. Isso garante que o hash registrado no XMP corresponde ao conteúdo visual real, não à versão já modificada.

```python
def calculate_sha256(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()
```

### 2. Preencher os placeholders do template

O template é lido como texto e os dois placeholders são substituídos pelos valores reais:

```python
xmp_content = xmp_content.replace("[INSERT_SHA256_HASH]", image_hash)
xmp_content = xmp_content.replace("[INSERT_DOI_OR_RECORD_LINK]", record_link)
```

### 3. Injetar o XMP na imagem

O Pillow suporta o parâmetro `xmp=` ao salvar imagens JPEG, injetando o bloco XMP diretamente no APP1 marker do arquivo:

```python
img.save(output_path, "jpeg", exif=exif_bytes, xmp=xmp_content.encode('utf-8'))
```

---

## Executando o exemplo

```bash
python3 embed_xmp.py
```

**Saída esperada:**

```
1. Preparando XMP a partir do template...
   Hash SHA-256 da imagem original: e0f5497c1068013466a9ffaf2c0f658002f6078aaa1c736b9b4fb7ff48a3e6db

2. Injetando XMP na imagem...
✅ Imagem salva com sucesso em: sample_hybrid_image_with_xmp.jpg
✅ Metadados XMP injetados com sucesso!

3. Atualizando manifestos JSON...
✅ Arquivos metadata.json e manifest.json atualizados com sucesso!
```

---

## Verificando os metadados embutidos

### Via Python

```python
from PIL import Image

img = Image.open("sample_hybrid_image_with_xmp.jpg")
xmp_data = img.info.get("xmp")
if xmp_data:
    print(xmp_data.decode("utf-8"))
```

### Via ExifTool (linha de comando)

```bash
exiftool -XMP:all sample_hybrid_image_with_xmp.jpg
```

---

## Resultado da validação

Após a execução, a imagem `sample_hybrid_image_with_xmp.jpg` contém o seguinte bloco XMP embutido (trecho dos campos-chave):

```xml
<anonymo:OriginalAuthorship>Human</anonymo:OriginalAuthorship>
<anonymo:CreationType>Human-AI Hybrid</anonymo:CreationType>
<anonymo:AIAssistance>Yes</anonymo:AIAssistance>
<anonymo:IntellectualFramework>TCF/TFB</anonymo:IntellectualFramework>
<anonymo:IntegrityHash>e0f5497c1068013466a9ffaf2c0f658002f6078aaa1c736b9b4fb7ff48a3e6db</anonymo:IntegrityHash>
<anonymo:RecordLink>https://github.com/christianmontgomery220-svg/anonymo-hybrid-image</anonymo:RecordLink>
```

---

## Fluxo completo de proveniência

```
[Imagem original]
       │
       ▼
 Calcular SHA-256  ──────────────────────────────────────────────┐
       │                                                          │
       ▼                                                          │
 Preencher TEMPLATE_XMP.xml                                       │
 (substituir placeholders)                                        │
       │                                                          │
       ▼                                                          │
 Injetar XMP na imagem ◄──── hash embutido no campo anonymo: ────┘
       │
       ▼
 Atualizar metadata.json + manifest.json
       │
       ▼
 Commit no repositório público (GitHub)
       │
       ▼
 [Prova de existência pública e verificável]
```

---

## Referências

- [XMP Specification Part 1 — ISO 16684-1](https://www.adobe.com/devnet/xmp.html)
- [Dublin Core Metadata Initiative](https://www.dublincore.org/)
- [IPTC Photo Metadata Standard](https://www.iptc.org/std/photometadata/specification/)
- [Anonymo AI Documentation](https://anonymodocs.com/)
- [TCF/TFB Theory](https://tfbtheory.com/)
- [Repositório público — anonymo-hybrid-image](https://github.com/christianmontgomery220-svg/anonymo-hybrid-image)

from docx import Document

doc = Document("TemplateNezasaAttributesV2.docx")

print("Paragraph styles in this document:")
for style in doc.styles:
    if style.type == 1:  # paragraph styles
        print("-", style.name)

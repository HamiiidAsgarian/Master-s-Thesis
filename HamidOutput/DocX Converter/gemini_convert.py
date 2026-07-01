import pypandoc
import os

# Define file paths
input_md = 'thesis.md'
output_docx = 'thesis.docx'
template_docx = 'template.docx'

# Verify template exists
if not os.path.exists(template_docx):
    raise FileNotFoundError(f"Missing {template_docx}! Put the university template in this folder.")

print("Starting conversion... This converts LaTeX math to native Word equations.")

# Pandoc arguments optimized for Farsi RTL and Academic Layouts
arguments = [
    f'--reference-doc={template_docx}',
    '--metadata', 'dir=rtl',
    '--metadata', 'lang=fa',
    '--from=markdown+complex_tex', # Ensures advanced LaTeX formatting blocks are caught
    '--to=docx'
]

try:
    pypandoc.convert_file(input_md, 'docx', outputfile=output_docx, extra_args=arguments)
    print(f"Success! Your thesis has been compiled to: {output_docx}")
except Exception as e:
    print(f"Conversion failed: {e}")
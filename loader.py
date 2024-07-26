import pdfplumber, re
from pypdf import PdfReader 
from docx import Document

class PDFLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def extract_plumber_text(self):
        text = ""
        with pdfplumber.open(self.file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text(x_tolerance=3, x_tolerance_ratio=None, y_tolerance=3, layout=False, x_density=7.25, y_density=13, line_dir_render=None, char_dir_render=None) + " "
        return text
        # return page.extract_words(x_tolerance=3, x_tolerance_ratio=None, y_tolerance=3, keep_blank_chars=False, use_text_flow=False, line_dir="ttb", char_dir="ltr", line_dir_rotated="ttb", char_dir_rotated="ltr", extra_attrs=[], split_at_punctuation=False, expand_ligatures=True)

    def extract_table(self):
        tables = []
        with pdfplumber.open(self.file_path) as pdf:
            for page in pdf.pages:
                tables += page.extract_tables(table_settings={})
        return tables
    
    def extract_reader_text(self):
        reader = PdfReader(self.file_path) 
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        return text

    def parse_data(self):
        data_reader = self.extract_reader_text()
        data_plumber = self.extract_plumber_text()
        # len (more), chars [#,>,\n] (less)
        def count_chars(input_string):
            return len(re.findall(r'[!@#$%^&*()_+{}\[\]:;<>,.?\\/-]', input_string))
        reader_chars, plumber_chars = count_chars(data_reader),count_chars(data_plumber)
        if abs(reader_chars-plumber_chars) <= 20:
            if len(data_plumber)<len(data_reader):
                return data_reader 
            else:
                return data_plumber
        if reader_chars > plumber_chars:
            return data_reader
        else:
            return data_plumber
                 
class DOCLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.document = Document(file_path)
        
    def get_text(self):
        text_list = [para.text for para in self.document.paragraphs]
        text = ''
        for i in text_list:
            text += i + '\n'
        return text

    def get_table(self):
        # Initialize a list to hold all tables
        tables_data = []
        
        # Iterate through each table in the document
        for table in self.document.tables:
            table_data = []
            for row in table.rows:
                row_data = [cell.text.strip() for cell in row.cells]
                table_data.append(row_data)
            tables_data.append(table_data)
        
        return tables_data

        
            
        






# Example usage
file_path = 'data/gurgaon.pdf'
pdf_loader = PDFLoader(file_path)
pdf_loader.parse_data()
# # Extract text
# # text = pdf_loader.extract_plumber_text()
# text = pdf_loader.extract_reader_text()
# print("Extracted Text:")
# print(text)

# # Extract table
tables = pdf_loader.extract_table()
for i in tables:
    print(i)

# file_path = 'data/Transcript -   Understanding your Electricity Bills.docx'
# doc_loader = DOCLoader(file_path)
# # print(doc_loader.get_text())
# tables = doc_loader.get_table()
# for i in tables:
#     print(i)
from pypdf import PdfReader 
import pdfplumber
from spire.doc import *
from spire.doc.common import *
import io, re, math

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
        self.document = Document()
        self.document.LoadFromFile(self.file_path)
        
    def get_text(self):
        return self.document.GetText()

    def get_table(self): #FIXME: The table extraction is not working with this library, might need to change it to find one that works and will have to switch text extraction to that module as well.
        tables_data = []
        for section in range(self.document.Sections.Count):
            for table in range(self.document.Sections[section].Tables.Count):
                temporary_table = []
                for row in range(self.document.Sections[section].Tables[table].Rows.Count):
                    print(self.document.Sections[section].Tables[table].Rows[row].Cells[0])

            
        






# # Example usage
# file_path = 'data/Selections.pdf'
# pdf_loader = PDFLoader(file_path)
# pdf_loader.parse_data()
# # Extract text
# # text = pdf_loader.extract_plumber_text()
# text = pdf_loader.extract_reader_text()
# print("Extracted Text:")
# print(text)

# # Extract table
# table = pdf_loader.extract_table()
# print("Extracted Table:")
# print(table[0])

# file_path = 'data/Transcript -   Understanding your Electricity Bills.docx'
# doc_loader = DOCLoader(file_path)
# print(doc_loader.get_text())
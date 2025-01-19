import pikepdf


class Utils:
    
    @staticmethod
    def remove_pdf_password(input_pdf, output_pdf, password):
        with pikepdf.open(input_pdf, password=password) as pdf:
            pdf.save(output_pdf)

    @staticmethod
    def safe_file_name(file_name):
        return file_name.replace(" ", "_").replace("/", "_").replace("\\", "_").replace(":", "_").replace("*", "_").replace("?", "_").replace("\"", "_").replace("<", "_").replace(">", "_").replace("|", "_")
    

class MarkdownFile:

    def __init__(self, filepath="results.md"):
        self.filepath = filepath
        self._create_file(self.filepath)
        self._write_title("Results")
        self.write_newline()

    def _create_file(self, filepath):
        f = open(filepath, "w")
        f.close()

    def _write_title(self, title):
        f = open(self.filepath, "a")
        f.write("# {}\n".format(title))
        f.close()

    def write_heading(self, heading):
        f = open(self.filepath, "a")
        f.write("## {}\n\n".format(heading))
        f.close()
    
    def write_subheading(self, subheading):
        f = open(self.filepath, "a")
        f.write("### {}\n\n".format(subheading))
        f.close()
    
    def write_text(self, text):
        f = open(self.filepath, "a")
        f.write("{}\n\n".format(text))
        f.close()
    
    def write_line(self):
        f = open(self.filepath, "a")
        f.write("---\n\n")
        f.close()
    
    def write_newline(self):
        f = open(self.filepath, "a")
        f.write("\n")
        f.close()

    def write_image(self, image_path, image_size=400):
        f = open(self.filepath, "a")
        # f.write("![IMAGE]({})\n".format(image_path))
        f.write('<img src="{}" alt="drawing" style="width:{}px;"/>\n\n'.format(image_path, image_size))
        f.close()
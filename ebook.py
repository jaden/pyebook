import argparse
import json
import os
import sys
import urllib
from pprint import pprint
from subprocess import call

# Referenced this method: http://chase-seibert.github.io/blog/2014/03/21/python-multilevel-argparse.html

class Ebook(object):

    ebook_json = 'ebook.json'
    json_obj = None
    
    build_dir = 'output'
    
    # JSON fields
    name = None
    cover_image = None
    template_file = None

    def __init__(self):
        parser = argparse.ArgumentParser(
            description='Manage building ebooks with Pandoc',
            usage='''ebook <command> [<options>]
            
Commands:
    doc             Build the ebook as a Microsoft Word document
    epub            Build the ebook as an ePub file
    help            Display help information about ebook
    html            Build the ebook as an HTML file
    init            Interactively create an ebook.json file
    mobi            Build the ebook as a Mobi file
    odt             Build the ebook as a LibreOffice document
    pdf             Build the ebook as a PDF document
    tex             Build the ebook as a TeX document
    txt             Build the ebook as a text document
''')

        parser.add_argument('command', help="The command to run")
        parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
        
        # Need to exclude remaining arguments for validation to work
        args = parser.parse_args(sys.argv[1:2])
        
        if os.path.isfile(self.ebook_json):
            self.load_json()
        
        if args.command == 'help':
            parser.print_help()
            exit(1)
            
        if not hasattr(self, args.command):
            print "Error: %s is not a valid command\n" % args.command
            parser.print_help()
            exit(1)
        
        getattr(self, args.command)()

    def doc(self):
        self.pandoc(["-s", "-S", "%s.md" % self.name, "-o", "%s/%s.docx" % (self.build_dir, self.name)])
        
    def epub(self):
        self.pandoc(["--epub-cover-image", self.cover_image, "%s.md" % self.name, "-o",
            "%s/%s.epub" % (self.build_dir, self.name)])
        
    def html(self):
        self.pandoc(["-s", "-S", "--toc", "%s.md" % self.name, "-o", "%s/%s.html" % (self.build_dir, self.name)])
        
    def init(self):
    
        if os.path.isfile(self.ebook_json):
            print "Error: %s already exists" % self.ebook_json
            exit(1)
            
        name = raw_input("Base name: ")
        
        template_file = raw_input("TeX Template (leave blank to download the default template): ")
        if not template_file:
            urllib.urlretrieve('https://github.com/jaden/ebooks/raw/master/pdf-template.tex', 'pdf-template.tex')
            template_file = 'pdf-template.tex'
        
        cover_image = raw_input("Cover image (default: cover.jpg): ")
        if not cover_image: cover_image = 'cover.jpg'
        
        with open(self.ebook_json, 'w') as fp:
            obj = {'name':name, 'template_file':template_file, 'cover_image': cover_image}
            json.dump(obj, fp, indent=4)
            
        os.mkdir(self.build_dir)
        
    def mobi(self):
        self.epub()
        call(["kindlegen.exe", "%s/%s.epub" % (self.build_dir, self.name), "-o", "%s.mobi" % self.name])
        
    def pdf(self):
        self.build_pdf_or_tex('pdf')
        
    def odt(self):
        self.pandoc(["%s.md" % self.name, "-o", "%s/%s.odt" % (self.build_dir, self.name)])

    def tex(self):
        self.build_pdf_or_tex('tex')
        
    def txt(self):
        self.pandoc(["%s.md" % self.name, "-o", "%s/%s.txt" % (self.build_dir, self.name)])
        
    def pandoc(self, opts):
        call(['pandoc'] + opts)
        
    def build_pdf_or_tex(self, type):
        self.pandoc(["--latex-engine", "xelatex", "--template", self.template_file, "%s.md" % self.name,
            "-o", "%s/%s.%s" % (self.build_dir, self.name, type)])
        
    def load_json(self):
        with open(self.ebook_json) as fp:
            self.json_obj = json.load(fp)
            self.name = self.json_obj.get('name')
            self.cover_image = self.json_obj.get('cover_image')
            self.template_file = self.json_obj.get('template_file')
            
if __name__ == '__main__':
    Ebook()
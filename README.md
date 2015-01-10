# pyEbook

A cross-platform Python command-line frontend to Pandoc for building an Ebook from Markdown and generating PDFs, ePubs, Mobis and more.

## Installation

Install [Python](https://www.python.org/)

Install [Pandoc](http://johnmacfarlane.net/pandoc/) and LaTeX using Pandoc's [installation page](http://johnmacfarlane.net/pandoc/installing.html) for the version of LaTeX to use for your operating system.

On Windows, I use:

- [MiKTeX](http://miktex.org/) to create PDFs
- [KindleGen](http://www.amazon.com/gp/feature.html?docId=1000765211) to create Mobi files

## Quickstart Guide

### Step 1
Add the directory holding ebook.py to your PATH or copy all three ebook.* files to somewhere that's already in your path. On Linux, set the executable bit on ebook, like so:

	chmod 700 ebook

### Step 2

Initialize your ebook directory

Create a new directory for your ebook and run:

	ebook init

You'll be prompted for the following three values that will be stored in ebook.json.

**Base name** - This is the filename of your Markdown file (without the .md extension) as well as the name that will be used for all of the output files.

**TeX template file**	- The TeX template file that Pandoc will use to build a PDF of your ebook. This is an initial version to start with, but that you can modify. It is hard coded to use cover.jpg for the cover image. Fonts may need to be adjusted for different operating systems.

**Cover image filename** - If you change it to something other than cover.jpg, update the default TeX template if necessary.

## Step 3

Write your book in Markdown (the file should be the value you chose for basename with a suffix of .md, e.g. if your base name is "my_ebook", the file would be my_ebook.md)

## Generate your desired format

For example...

to create a PDF of your ebook:

	ebook pdf

to create an ePub:
	
	ebook epub

to create a Mobi using [KindleGen](https://kindlegen.s3.amazonaws.com/Readme.txt):

	ebook mobi

Run ebook without any arguments to see all of the possible formats.

Take a look at the examples directory to see an eBook I created in a few minutes from a [Project Gutenberg](https://www.gutenberg.org/) text file.

Use Amazon's Kindle Previewer to emulate different Kindle Devices
rm data/latex/$1.web.tex
rm data/latex/$1.pdf.tex
rm pageflipper/pdfs/$1.pdf
rm pageflipper/$1.html
rm -r pageflipper/pages/$1
./generate_novels.py

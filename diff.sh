latexdiff --flatten main-old.tex main.tex > main-diff.tex
pdflatex main-diff.tex
open main-diff.pdf

# latex Makefile
texpath=/usr/texbin/
PDFLATEX=${texpath}pdflatex -halt-on-error -synctex=1 --interaction=nonstopmode
LATEX=${PDFLATEX}
BIBTEX=bibtex
DVIPS=dvips
PS2PDF=ps2pdf

all: orionGEMS

orionGEMS:  
	@rm -f orionGEMS*.aux orionGEMS*.bbl orionGEMS*.blg orionGEMS*.dvi orionGEMS*.log orionGEMS*.lot orionGEMS*.lof
	${LATEX} orionGEMS.tex
	${BIBTEX} orionGEMS
	${LATEX} orionGEMS.tex
	${BIBTEX} orionGEMS
	${LATEX} orionGEMS.tex
	gs -dSAFER -dBATCH -dNOPAUSE  -sDEVICE=pdfwrite -sOutputFile=OrionGEMS_small.pdf orionGEMS.pdf


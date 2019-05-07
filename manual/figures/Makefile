#asdfa
#
#
template := 'template.pgs'
files := $(shell ls *.tex)
pdfs := $(files:.tex=.pdf)

all: ${pdfs}
	echo "generated all files"

evaluation%.pdf: evaluation%.tex simulation_plots.pgs	
	pdflatex $<
	
%.pdf: %.tex
	sed 's/<>/\\\input{$<}/' < ${template} > $<.tmp
	pdflatex $<.tmp
	mv $<.pdf $@
	rm $<.*

clean:
	rm -f *.pdf *.aux *.log *.bbl *.blg *.tmp *.dvi *.synctex.gz


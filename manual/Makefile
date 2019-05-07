pdflatexoptions = --shell-escape

all:
	pdflatex ${pdflatexoptions} manual
	bibtex manual
	pdflatex ${pdflatexoptions}  manual
	pdflatex ${pdflatexoptions}  manual

reallyall:	figures
	pdflatex ${pdflatexoptions}  manual
	bibtex manual
	pdflatex ${pdflatexoptions}  manual
	pdflatex ${pdflatexoptions}  manual

quick:
	pdflatex ${pdflatexoptions}  manual

clean:
	rm -rf *.aux *.bbl *.blg *.dvi *.log *.listing *.out *.bak *.toc *synctec.gz

cleanall:
	make clean -C ./figures

figures:
	make -C ./figures

.PHONY: figures

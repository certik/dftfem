F=doc

all:$(F).ps 

$(F).ps:$(F).dvi
	dvips $(F).dvi -o
$(F).dvi:$(F).tex
	tex -fmt=csplain $(F).tex 
	tex -fmt=csplain $(F).tex 
#	pdftex -fmt=pdfcsplain $(F).tex
clean:
	rm -f $(F).dvi $(F).ps $(F).pdf $(F).log $(F).te~ $(F).toc $(F).aux $(F).bbl $(F).blg

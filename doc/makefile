MAIN_NAME = lecture_notes
HELPER_NAME = helper_table

all :
	pdflatex --shell-escape ${MAIN_NAME}.tex

helpers :
	pdflatex ${HELPER_NAME}.tex

run :
	evince ${MAIN_NAME}.pdf

clean :
	rm -f ${MAIN_NAME}.pdf ${HELPER_NAME}.pdf
	rm -f *.aux *.log *.toc *.py.err *.py.out *.rc *.py
	rm -rf ch*/*.aux ch*/*.log ch*/*.toc

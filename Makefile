.PHONY: run_multi_page

run_multi_page:
	@# streamlit will only hot reload things in the app folder or on the pythonpath
	@PYTHONPATH=`pwd`:$PYTHONPATH \
		streamlit run ./examples/multi-page/01_PageOne.py

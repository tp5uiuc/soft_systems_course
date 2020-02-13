clean_notebooks:
    # This finds Ipython jupyter notebooks in the code
    # base and cleans only its output results. This
    # results in 
	@jupyter nbconvert --version
	@find . -maxdepth 5 -name '*.ipynb'\
		| while read -r src; do jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace "$$src"; done



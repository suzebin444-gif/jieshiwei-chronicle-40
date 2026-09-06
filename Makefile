.PHONY: validate site

validate:
	python3 scripts/validate_project.py

site:
	python3 scripts/build_site_data.py


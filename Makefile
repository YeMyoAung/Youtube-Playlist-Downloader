playlist_downloader:
	@python3 -m venv .venv && source .venv/bin/activate
	@python3 main.py

setup:
	@python3 -m venv .venv && source .venv/bin/activate
	@pip3 install -r requirements.txt
	
.PHONY:
	playlist_downloader	setup
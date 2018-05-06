install:
	wget https://github.com/WorksApplications/Sudachi/releases/download/v0.1.0/sudachi-0.1.0-dictionary-full.zip
	unzip sudachi-0.1.0-dictionary-full.zip
	mv system_full.dic resources/system.dic
	rm sudachi-0.1.0-dictionary-full.zip
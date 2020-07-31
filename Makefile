all: clean
	pyinstaller --onefile --windowed --add-data './pcb/:./pcb' ./main.py
	echo -e "\x1b[1m\x1b[32mExecutable built in dist directory.\x1b[0m"

clean:
	rm -rf ./build ./dist

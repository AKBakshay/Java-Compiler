all:
	chmod 777 ./src/init.sh
	./src/init.sh
	cp ./src/main.py final.py
	chmod 777 final.py
	mv final.py myASTGenerator 
	
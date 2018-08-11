#!/bin/bash

INSTALL="0"
CREATE="0"
HOST="localhost"
FILE="host"
PUBLISH="0"

for arg in "$@"; do
case "$arg" in
    "-i"|"--install")
    INSTALL="1"
    ;;
    "-p")
    PUBLISH="1"
    ;;
    "-c"|"--create")
    CREATE="1"
    ;;
    --host=*)
    HOST="${arg#*=}" # split string
    ;;
    --file=*)
    HOST="${arg#*=}" # split string
    ;;
    #-l=*|--lib=*)
    #LIBPATH="${arg#*=}" # split string
    #;;
    --default)
    ;;
    *) # unknown option
    ;;
esac
done

if [ "$INSTALL" -eq "1" ]; then
	sudo apt-get install expect
    sudo apt-get install openssl -y
    sudo apt-get install libnss3-tools -y
    sudo chmod +x create.sh
fi

if [ "$CREATE" -eq "1" ]; then
	"${0%/*}"/create.sh "${0%/*}" "$HOST" "$FILE"
	sudo cp "${0%/*}/$FILE".crt /etc/ssl/certs/$FILE.crt
	sudo cp "${0%/*}/$FILE".key /etc/ssl/private/$FILE.key
fi

if [ "$PUBLISH" -eq "1" ]; then
	certutil -d sql:$HOME/.pki/nssdb -A -t "P,," -n "$HOST" -i "${0%/*}/$FILE".crt
fi

exit


# https://www.humankode.com/ssl/create-a-selfsigned-certificate-for-nginx-in-5-minutes
# openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout localhost.key -out localhost.crt -config localhost.conf
# sudo cp localhost.crt /etc/ssl/certs/localhost.crt
# sudo cp localhost.key /etc/ssl/private/localhost.key
# certutil -d sql:$HOME/.pki/nssdb -A -t "P,," -n "localhost" -i localhost.crt

#!/usr/bin/expect -f
set ROOT [lindex $argv 0]
if {$ROOT eq ""} {set ROOT ""}
set HOST [lindex $argv 1]
if {$HOST eq ""} {set HOST "localhost"}
set FILE [lindex $argv 2]
if {$FILE eq ""} {set FILE "localhost"}

spawn openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout $ROOT/$FILE.key -out $ROOT/$FILE.crt -config $ROOT/ssl.conf
expect ":"
send  "DE\r"
expect ":"
send  "BW\r"
expect ":"
send  "RV\r"
expect ":"
send  "$HOST\r"
expect ":"
send "vog3lm.development\r"
expect ":"
send  "$HOST\r"
interact
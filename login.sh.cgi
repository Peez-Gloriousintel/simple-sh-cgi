#!/bin/sh

# @name: A Simple Login CGI
# @author: pj4dev.mit@gmail.com
# @last_modified: 09/11/2015

Header() {
	COOKIE=$1
	echo "Content-type: text/html"
	if [ "$COOKIE" != "" ]; then
		echo "Set-cookie: $COOKIE"
	fi
	echo
}

StartHTML() {
	echo <<EOF
<html>
<head><title>Shell CGI Authen</title></head>
<body>
EOF
}

EndHTML() {
	echo "</body>"
	echo "</html>" 
}

PrintLogin() {
	echo "
	<form action='login.sh.cgi' method='POST'>
	Username: <input type='text' name='username'/>
	Password: <input type='text' name='password' />
	<input type='submit' name='submit' value='Login'/>
	</form>"
}

PrintLogout() {
	echo "
	<form method='POST' action='?action=logout'>
	<input type='submit' name='logout' value='Logout'/>
	</form>
	"
}

POST=`cat`
username=`echo $POST | egrep -o 'username=([^&=]+)' | sed 's/^username=//g'`
password=`echo $POST | egrep -o 'password=([^&=]+)' | sed 's/^password=//g'`
cookieuser=`echo $HTTP_COOKIE | egrep -o 'username=([^;]+)' | sed 's/^username=//g'`
action=`echo $QUERY_STRING | egrep -o 'action=([^&=]+)' | sed 's/^action=//g'`

if test "$action" = "logout" ; then
	Header "username="
	StartHTML
	PrintLogin
elif test "$cookieuser" != "" ; then
	Header "username=$cookieuser"
	StartHTML
	name=`cat accounts/$cookieuser/name`
	echo "You are authenticated. Welcome $name"
	PrintLogout
elif ! test "$username" = "" && ! test "$password" = "" ; then
	if test -f accounts/$username/password ; then
		chkpasswd=`cat accounts/$username/password`
		if test "$chkpasswd" = "$password" ; then
			name=`cat accounts/$username/name`
			Header "username=$username"
			StartHTML
			echo "You are authenticated. Welcome $name"
			PrintLogout
		else
			Header
			StartHTML
			echo "Incorrect password"
		fi
	else
		Header
		StartHTML
		echo "Username doesn't exist"
	fi
else
	Header
	StartHTML
	PrintLogin
fi

EndHTML

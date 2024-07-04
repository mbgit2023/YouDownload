

tail -1 $HOME/Downloads/$1 | awk -F " " '{ print $2 }'
#! /bin/sh

PWD=`pwd`

echo "
server.document-root = "\"$PWD/data\""

server.port = 3000

mimetype.assign = (
  \".html\" => \"text/html\", 
  \".txt\" => \"text/plain\",
  \".jpg\" => \"image/jpeg\",
  \".png\" => \"image/png\" 
)" > lighttpd.conf &

mkdir data

cd data; cat ../metric-script.fg | fg-metric 
cd data; cp better-index.html index.html






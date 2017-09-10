Go into the folder that has the Dockerfile and build the image, then the
container.

`cd craigslist`

`docker build -t eapen/craigslister:latest .`

`docker run -d --restart unless-stopped --name zen_ritchie -p IPADDRESS:9001:9001 -t craiglister`

OR

`docker run -d --restart unless-stopped -e SLACK_TOKEN={SLACK_TOKEN} --name zen_ritchie -p 9001 -t craiglister`


View details
`docker exec -it zen_ritchie /bin/bash`

`tail -f -n 100 /opt/wwc/logs/craigslister.log`

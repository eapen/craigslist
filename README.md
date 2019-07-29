Go into the folder that has the Dockerfile and build the image, then the
container.

`cd craigslist`

`docker build -t eapen/craigslister:latest .`

`docker run -d --restart unless-stopped --name craigslister -p IPADDRESS:8880:9001 -t eapen/craiglister`

OR

`docker run -d --restart unless-stopped -e SLACK_TOKEN={SLACK_TOKEN} --name craigslister -p 0.0.0.0:8880:9001 -t eapen/craiglister`


View details
`docker exec -it craigslister /bin/bash`

`tail -f -n 100 /opt/wwc/logs/craigslister.log`

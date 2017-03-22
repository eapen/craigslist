Go into the folder that has the Dockerfile and build the image, then the
container.

`cd craigslist`
`docker build -t craigslister .`
`docker run -d -e SLACK_TOKEN={SLACK_TOKEN} --name zen_ritchie -i -t craiglister`

View details
`docker exec -it zen_ritchie /bin/bash`

`tail -f -n 100 /opt/wwc/logs/craigslister.log`

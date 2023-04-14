# CodebaseExplained

This is a helpful too designed to funnel all information about another codebase into a format which GPT-4 can read. You can then ask GPT-4 about things about this codebase to accelerate you understanding of it.

## Parameters
Use --excludeFolders to exclude specific folders and --excludeFiles to exclude specifc files (of course). Default excludes are already hard coded. Start without using these flags, and if you find irrelevant content in your `output.txt`, then use these flags.

## Prompt Engineering:
The prompt fed to GPT-4 will look like this: 

You will be my developer assistant. I'm going to provide you with all the information about my codebase and your job is to help me understand it. After I provide all the information, you will respond to me by very briefly summarizing the technology and tech stack used. Then I will ask you further questions.

`FANTASTIC_REPO_NAME

|   docker-compose.yml

|   useless_folder

|   app

|   |   __init__.py

|   |   app.py`


All significant project files:

docker-compose.yml

blah

app/__init.py

bleh

app/app.py

bluh

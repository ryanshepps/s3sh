# S3SH

## Installation

```bash
pip install -r requirements.txt
```

## Running

Add an access key and access key ID for an account with permissions to do the actions you want to do with s3 to [S5-S3.conf](S5-S3.conf). See [Create an AWS access key](https://aws.amazon.com/premiumsupport/knowledge-center/create-access-key/) for help.

Run

```bash
python s3sh.py
```

## Features

Local File Functions

- [x] Passes all non-Cloud related commands to session shell
- [x] Copy local file to Cloud location (`locs3cp`)
- [x] Copy Cloud object to local file system (`s3loccp`)

Cloud Functions

- [x] Create a bucket (`create_bucket`)
- [x] Create directory/folder (`create_folder`)
- [x] Change direcotry (`chlocn`)
- [x] Current working directory or location (`cwlocn`)
- [x] List buckets, directories, objects (`list`)
- [x] Copy objects (`s3copy`)
- [x] Delete objects (`s3delete`)
- [x] Delete bucket (`delete_bucket`)

## Environments

- [x] Linux
- [x] Mac
- [ ] Windows

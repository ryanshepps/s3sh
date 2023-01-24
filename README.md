# S3SH

## Features

Local File Functions

- [x] Passes all non-Cloud related commands to session shell
- [x] Copy local file to Cloud location (`locs3cp`)
- [ ] Copy Cloud object to local file system (`s3loccp`)

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

## Bugs/Limitations

- Can't traverse up (`..`) more than one directory.
- `s3delete` does not tell you if an object you're trying to delete does not exist.
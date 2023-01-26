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

## Bugs

- Can't `chlocn` to a path more than one level deep when a folder more than one level deep is empty. For example when the folder `another_test_folder/` is empty in the path `test-bucket/test_folder/another_test_folder/`, `chlocn test_folder/another_test_folder/` will fail.
- `s3delete` silently fails when it tries to delete a file that does not exist. Deleting a file that does exist works fine.
- Deleting empty folders with `s3delete` does not work.

## Limitations

- Can't `s3loccp` without specifying a file name in the local file system. Ideally, if no file name is provided (just a folder location), `s3loccp` would use the same file name as the file in s3.
- Relative paths that go up a directory in all commands except `chlocn` do not work. For example `s3copy file.py ../` does not copy `file.py` up a directory.
# Bulletin Generator

This is a bulletin generator with the templates modified to exclude identifying information.

## Build

Currently, the styles and scripts can be compiled with the following Powershell commands and [YUI Compressor](https://yui.github.io/yuicompressor/):

```powershell
$OutputDirectory = "static"
$dev = "develop-scripts"

Get-Content $dev/js/*.js | java -jar $dev/yuicompressor.jar -o $dev/js/scripts.js --type js --charset utf-8
Get-Content $dev/css/*.css | java -jar $dev/yuicompressor.jar -o $dev/css/styles.css --type css --charset utf-8

Move-Item -Path $dev/js/scripts.js -Destination $OutputDirectory/scripts -Force
Move-Item -Path $dev/css/styles.css -Destination $OutputDirectory/css -Force
```

YUI Compressor appears to be a dead project however, so there are plans to move to other compressors such as the [Google's Closure Compiler](https://developers.google.com/closure/compiler/) for JS and something else for CSS.

Tests verifying inputs are excluded, and favicons are also excluded.

## Hosting

Hosting varies from server to server, but [Digital Ocean](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04) has a good tutorial for hosting it on Ubuntu Server.

## Configuration

A good CSRF key must be provided as an environment variable named `csrf_key`.

The Python version is 3.7+ and note that requirements will also need to be installed for the [venv](https://docs.python.org/3/tutorial/venv.html) using `pip install -r requirements.txt`.

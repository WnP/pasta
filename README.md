```
pasta(1)                             PASTA                             pasta(1)

NAME
    pasta: command line paste tool.

SYNOPSIS
    < command > | curl -F 'paste=<-' https://paste.steeve.io

DESCRIPTION
    add ?<lang> to resulting url for line numbers and syntax highlighting
    use this form to paste from a browser

EXAMPLES
    $ cat bin/ching | curl -F 'paste=<-' https://paste.steeve.io
       https://paste.steeve.io/aXZI
    $ firefox https://paste.steeve.io/aXZI?py
    $ curl https://paste.steeve.io/aXZI?raw

SEE ALSO
    http://github.com/WnP/pasta
```

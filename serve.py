#!/usr/bin/env python

from livereload import Server, shell

server = Server()
server.watch('blog', shell('python kiss.py', cwd='.'))
server.serve(root='public')

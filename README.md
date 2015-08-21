# Project-Bot
This bot allows for the easily scripted creation of project folders. Use the included templates, or make your own to minimize your setup time, and get to working!

Eventually this could be folded into a personal assistant bot, that you could use via voice commands.

## Example Use Cases
As a new user, I want to see a test drive!

This use case is the simplest of all, as Project-Bot has built-in defaults for all of its templates. To generate them is a simple command.
```python project-bot.py -e```
---
As a user, I want to see what arguments I can pass to Project-Bot.

Check out the help menu.
```python project-bot.py -h```
----
As a user, I want to see what Project-Bot is doing under the covers, because there might be an error, or I am just curious.

Ok you. To see under the covers, add -v flags until you can't stand it! You can pass 0-3 vs, or as many as you want, but I only care up to 2.
```python project-bot.py -e -vvv```
---
As a photographer, I want to have a certain folder structure to put my pictures in to work on them in other programs.

Project-Bot makes this use case as easy as listing the folder structure in the template (set it and forget it!), and for each project just specify the name and the template name.
```python project-bot.py "Smith Family Wedding" -t "Photography" ```

## Installation
No installation necessary! All you need do is put the files into your root project folder(s), and you're off to the races.
Currently the only external dependency is Git, which only works on Linux/Unix based systems (makes use of shell command). Users on those systems likely already have it, so no need to worry.

## Built-in Templates
There are several templates built in, and it is easy to add more, using the built-in ones as a starting point. The main thing to note is they use json, an easily readable, parsable, and lightweight object notation.

### Photography
Mostly aimed at the photography aficionados who enjoy editing and retouching their photos after taking them, this template provides a good deal of organization, as well as some stock photos from the author of Project-Bot to make sure the folders are preserved when importing to Lightroom [link a wiki page, or article on why].

Organization:
 Project Folder
   |- New Project 			Root of this project, named (likely) for the event you shot.
   | |- gallery				Folder where you export your best photos!
   | |- studio
   |   |- 01-top			Where your best photos will reside (I like to have a cutoff of about 30)
   |     |- 01.jpg
   |   |- 02-good			Where the rest of your good photos go. This could be empty if a small shoot.
   |     |- 02.jpg
   |   |- 03-funny			Often I find hilarious photos in there, and put them here if no place above.
   |     |- 03.jpg
   |   |- 04-bad			Self explanatory.
   |     |- 04.jpg
   |   |- 05-dump			I import all photos here, and move them to other folders such that it ends up empty.
   |     |- 05.jpg
   |   |- 06-panoramas		All panorama photos (or parts of) get divided into numbered folders to get stitched.
   |     |- 01
   |       |- 06.jpg
   |     |- 02
   |       |- 07.jpg
   | |- readme.md 			Can hold interesting information about the shoot, or notes about the process or event.









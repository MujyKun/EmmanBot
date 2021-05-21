# Emman Voice Bot in Python

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/274aa55b0dbc413f9fe3a957f944a326)](https://www.codacy.com/gh/MujyKun/EmmanBot/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=MujyKun/EmmanBot&amp;utm_campaign=Badge_Grade)

**[Become a Patron!](https://www.patreon.com/bePatron?u=38971435)**

## What is it?
EmmanBot is a simple bot that plays local audio files. It has volume changing, dictionary, and looping features. 

The purpose of this bot was originally just to say "Bruh" in a voice channel but has switched to a more  
customizable approach for allowing a lot of custom keywords so that users may use each others  
voice-lines to form sentences in a voice chat.

If you would like to test the bot before-hand, There is a version of the bot running 24/7, but do keep in mind that  
it was not designed for the general public, so there is no way to upload your own audio files and will have generic  
audio files.

[Click Here to Invite EmmanBot.](https://discord.com/oauth2/authorize?client_id=845180622418870283&scope=bot&permissions=1609956823)

## How to use:

Clone the Repo: ``git clone https://github.com/MujyKun/EmmanBot.git``  

Rename `.env.example` to `.env`.  

Open `.env`, put your bot token under `LIVE_BOT_TOKEN`, and audio directory under `AUDIO_PATH` and save.  

Next, to install the dependencies, type `pip install -r requirements.txt`.  

If you do not already have ffmpeg installed, you may need to do so (and probably add it to PATH as well).

After that, you may launch `run.py` and everything should work fine.  

Default Server Prefix is `*` and may be changed in `run.py`.

To add your own audio file, place an audio file or a subdirectory in your audio folder, and it will be available 
for usage instantly. 

If you are using subdirectories, you would use dot notation to access the files for example:

If `audio` is your main audio directory, and I have a sub-folder called `mujy`, and an audio file inside of `mujy` called 
`good.mp3`, then in my command usage, I would use `mujy.good` without the file type. 

When adding your own file, make sure the audio file is .mp3 as it is the default (and no others are currently allowed).

In this repo, I have included some audio files for test usage.  

## Commands:

**Default Bot Prefix is `*`**

**The term `loop` should be associated with how many times you want the files to play in TOTAL.**

`audio [sub directory]` List a sub directory or all audio files.

`dic [volume] [loop] [file_name1 file_name2 file_name3 ...]`  Plays files right after each other.

`join`  Join the voice channel of the user.

`leave` Leave the voice channel in this guild.

`ping`  Test if the bot is online.

`play [file_name] [volume] [loop]`  Play/Bruh an audio file.

`help [command name]`  View specific/all commands. 
Command Usage Examples

`*audio` would list all audio sub-directories and main audio files.
`*audio mujy` would list all sub-directories and audio files under `mujy.`

`*dic 40 4 mujy.test mujy.phrase` would loop `test phrase` `4` times at volume level `40`.

Please note that the default volume level of `dic` is 100, and the default loop is 1. In order to call words with
the default settings, you will need to type them like so:  
`*dic 100 1 mujy.test mujy.phrase` would say `test phrase` `1` time at volume level `100`.

`*join` will join my voice channel if I am in one.

`*leave` will leave the voice channel on the server regardless if I am in one.

`*ping` would respond with "Pong" if it is online and running.

`*play` would play the default bruh (voiced by Emman himself) at volume `100` `once`.

`*play mujy.test 60 3` would play mujy's test audio at `60`% volume `3` times.

`*help` would bring up a list of all the commands their descriptions.

`*help play` would bring up a more detailed description of the `play` command.   

## Why is the bot named EmmanBot?
As simple as it is, the name of the person that requested the bot to be developed is Emman.

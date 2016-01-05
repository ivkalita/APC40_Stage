# APC40_Stage
This repository contains Ableton Live remote script for Akai APC40.
## The goal
APC40_Stage (this is the name of the script) allows you to use your APC40 as some kind of track manager when you are on a stage with live band. I organised my project such a way:
 + Setup contains multiple songs and 1 metronome track
 + Each song is a group (Ableton tracks group) of midi and audio tracks with clips
 + Each midi-track contains only one instrument for only one song
 + Each audio-track contains similar sounds for only one song
 + All clips for songs are launching automatically by using "follow actions"

So, when I'm playing with live band, I can just click first scene launch button and wait for the end of performance - all effects, transitions, etc are recorded and automated. Of course, it is not really cool. That's why I decided to play the most powerfull synths by myself (using another controller - SL Mk2), in "manual mode". APC40_Stage helps me to switch between "auto" and "manual" modes faster.

## Requirements

I have tested this script on Ableton Live Suite 9.2.1 only.

## Installation

### Fast installation
Check paths to Ableton Live application in Makefile if something goes wrong.
```
git clone https://github.com/kaduev13/APC40_Stage
cd APC40_Stage
make
```
### Easy installation
 + Create folder APC40_Stage in MIDI Remote scripts folder (`/Applications/Ableton Live 9 Suite.app/Contents/App-Resources/MIDI Remote Scripts` for Ableton Live 9 Suite for MacOS)
 + Copy all files from `APC40_Stage/src` to this folder


## Debugging

Internal Ableton Live log file is located at ~/Library/Preferences/Ableton/Live\ 9.2.1/Log.txt (it depends on Live version, just google it). Also, I'm using my custom logger, it allows me to call log function from instance of each class I want, not only from instances of children of _Framework.ControlSurface. To use this custom logger, you should open src/Logger.py, set CUSTOM_DEBUG_LOGGING to True, and rewrite CUSTOM_LOG_FILE_PATH.
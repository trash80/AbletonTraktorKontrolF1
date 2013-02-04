AbletonTraktorKontrolF1
=======================

Ableton Remote MIDI Python Scripts for NI Traktor Kontrol F1

This was a weekend project originally based on the Launchpad's decompiled source.
F1's RGB buttons (full REGB clip support) are mapped to Ableton's session view matrix 
and the Click Encoder is setup for navigation. The bottom row of buttons are mapped 
to stop clips in the track range using the Kontrol F1 Up template in the NI controller 
editor or they are mapped as scene launch buttons using the Kontrol F1 Side template.

Installation
=======================
1. Add the controller map templates provided into the NI Controller Editor. In the "Templates" tab, click the "Edit" dropdown. Select "Append > Open" and add the provided files.

2. Add the Remote Script folder "KontrolF1" to Ableton's Remote MIDI Scripts folder.
    --- For Windows --- Drop the folder intoC:\Program Files\Ableton\Live x.x.x:\Resources\MIDI Remote Scripts
    --- For Mac --- Go to Applications, Right click or Ctrl-click "Ableton Live" and select "Show Package Contents", Navigate to "Contents/App-Resources/MIDI Remote Scripts" -Drag the folder into this directory.

3. Open Ableton, go to preferences and in the MIDI sync tab select "KontrolF1" in the control surface dropdown and select the MIDI in & out ports.

Mappings
=======================
This package comes with 2 templates. The first is a standard "up" view and works as expected. The second "Side" view is meant for hte F1 to be viewed sideways- Sliders & knobs to the left, grid to the right. It makes sense for taking advantage of the scene launch buttons.

All other controls not listed can be remapped  / assigned to whatever.

Midi map:
- The grid is on Channel 3, and consumes CC values 0 to 15 on channels 1 to 3
- Scene Launch buttons are on Channels 1 using CC: 56,57,58,59
- Stop Launch buttons are on Channels 1 using CC: 60,61,62,63
- Navigation encoder expects to be on Channel 1 using CC: 105
- Toggling left or down on navigation (the push button on the encoder) is on Channel 1
using CC: 106

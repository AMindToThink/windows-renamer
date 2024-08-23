# windows-renamer
This script can run on any computer, not just Windows (in fact, running it on Windows would be pointless because the point is to format files *for* Windows).


WARNING! 

Please read this entire README before using. It isn't very long.

I hope you have a backup of whatever you are acting on, because this renames and edits all of the files in a folder. 

Use at your own risk! Running in a root folder is an especially bad idea.



NOTE:

In addition to the special characters, Windows also has problems with long file paths. You can fix that by:

Follow this: https://www.microfocus.com/documentation/filr/filr-4/filr-desktop/t47bx2ogpfz7.html

Run this: git config --global core.longpaths true


DESCRIPTION:

Windows filenames disallow certain characters. That means that a project that works on Mac and Linux might not work if taken to windows (eg when you Git clone it). 

This is a simple script that renames all the files in a directory to remove characters that are illegal in windows. 

By default, These are the replacements made. Feel free to change them by changing the illegal_char_to_legal_char_dict:

'<' -> '[lt]'

'>' -> '[gt]'

':' -> '[col]'

'"' -> '[quo]'

'/' -> '[fsl]'

'\\' -> '[bsl]'

'|' -> '[pip]'

'?' -> '[que]'

'*' -> '[sta]'


By changing the symbols to a string that will not appear in a document's name naturally (eg "[lt]"), the script can be run in reverse to change all the "[lt]" in filenames to "<". This is the "unfix" option.


The script will also look in any files with the extensions '.r','.R','.py', or '.ipynb' for references to documents that have been renamed so that the reference can be changed to the updated version.

(if your document names are common substrings, this may result in issues!)

Again, feel free to change the list of extensions to add more scripts.


Usage:

User must have python installed.

Create the script on your computer.

Run the following line:

python <folder containing the script>/rename_everything_for_windows.py <folder to act on> fix 

To (attempt to) undo the changes (it will work unless you have one of the strings like "[pip]" as a substring in a filename to begin with), run:
python <folder containing the script>/rename_everything_for_windows.py <folder to act on> unfix 


If you want to know what was changed, the '\[...\]' and '\[..\]' regular expressions can be handy.


To do a "dry run", which shows you what it would do without doing it, use the --dry-run flag:
python <folder containing the script>/rename_everything_for_windows.py <folder to act on> fix --dry-run

Recommended: cd into the target folder, then <folder to act on> will be '.'


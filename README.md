# Battery_checker
This is a simple script which notifies the user whenever the battery status is critical. Notifications are in the form of speech and also through the graphical mode by creating a notification in the taskbar.
It uses the script here https://gist.github.com/wontoncc/1808234 to create a notification and also the apis winsound for sounds, wmi for battery checks and pyttsx for text to speech.
The program checks for the battery status and if it below a threshold (25 here), it notifies the user, and if the user still doesn't plug in the charger, the program notifies the user by speech mode speaking out a message along with a beep.

To install the necessary modules, run the following command from the command line:

pip install pyttsx

All other modules are preincluded.

Note: The program is made and tested on Windows.

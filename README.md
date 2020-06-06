# Ambassador

### How To
- Todo

### Technical Details

- Checks to see if all apps are installed specified by ambassador/docs/apps-information.csv field 4.
- If the check fails then it runs install_apps with a list of the non-updated apps. (Currently only checks the android apps).
- Once all apps are are installed it'll check to see if you're installing and android app or ios app and will pass a list of the respected app paths to an install function.
- Tool exits. 

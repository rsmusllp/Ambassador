# Ambassador

![Issues Open](https://img.shields.io/github/issues/rsmusllp/ambassador)

Ambassador is a tool for rapidly provisioning mobile devices for use in mobile security services.

------
### First time usage
#### Dependencies
For Ambassador to run properly the device needs to be rooted/jailbroken. For IOS provisioning Ambassador requires the device to have openssh installed and will prompt for the IP Addr when establishing the debugging bridge.
#### Retrieving and running Ambassador.
```
# Clone down the repository.
git clone https://github.com/rsmusllp/Ambassador
# Install paramiko dependency
pip install paramiko
# Run Ambassador
python Ambassador.py -h 
```
------
### Technical Details 
Starting Ambassador requires a csv file entitled `apps-information.csv` to be located within `{ambassador-root-dir}\data\docs\`. Ambassador parses this file to retreivie neccessary information to properly install provision the mobile devices with the appropriate application(s). 

#### apps-information.csv format
| Title           | Example (1)                         | Example (2)                         | Description                                                                                                                                                        |
|-----------------|-------------------------------------|-------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| app_name        | The RSM App                         | The RSM App                         | The application identifier.                                                                                                                                        |
| app_platform    | Android                             | IOS                                 | The platform the application runs on.                                                                                                                              |
| app_type        | File                                | Package                             | This value can have two values (file or package). Files are APK(s) or IPA(s) to be installed through IDB or ADB. Packages are hosted through aptitude.             |
| app_installer   | The_RSM_App.apk                     | com.rsm.rsmapp                      | This value either needs to be the file name for the IPA or APK to be installed through a debugging bridge or the package identifier as specified through aptitude. |
| app_url         | https://rsm.com/TheRSMApp.apk       | N/A                                 | The URL to retrieve the application from (N/A if a package).                                                                                                       |
| app_description | Example Application for Ambassador. | Example Application for Ambassador. | The description to be displayed beside the app_name when a user uses the `--help-apps` flag. 

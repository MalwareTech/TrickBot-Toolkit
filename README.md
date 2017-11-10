# TrickBot
A collection of tools for working with TrickBot

## ConfigDecrypter.py
**Used to decrypt TrickBot configs (found in install directory under then name config.conf)**

Example usage: ConfigDecrypter.py -input config.conf -output config.txt

## FileDownloader.py
**Used to download files from command and control server**

For it to work you'll need to fill servers.txt with a list of recent servers (TrickBot servers die very quickly)

the -f (--file) specifes the file to download, here is a list of files available. 
* Modules
  * systeminfo32 - gather information about the infected system (32-bit module)
  * injectdll32 - injects into the browser and performs webinjects (32-bit module)
  * mailsearcher32 - searches through files to gather a list of email addresses (32-bit module)
  * sharedll32 - allows the malware to move laterally via network shares (32-bit module)
  
* Config Files
  * main - main TrickBot config which includes the latest server list
  * dinj - dynamic webinject configuration
  * sinj - static webinject configuration
  * dpost - server which the dynamic webinjects will send intercepted requests to
  * mailconf - server to send harvested email list to

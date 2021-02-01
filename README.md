# Dell-Zerotouch-Blade-Provisioning
Dell Zero-Touch provisioning for Blade servers

Python script that mimics the Dell Zero-Touch/DHCP Provisioning behavior for Blades since this appears to be no longer enabled for blade servers out of the box.

Environment:
Dell M1000e Blade Chassis
Dell M640 Blades

Requirements:
Linux Server with Python >= 3.5

OpenManageEnterprise with an alert policy for Blades being inserted
*Category > Built-in > iDrac > System Health > Other   
*Severity > Normal
*Target > Static or Dynamic groups containing the Chassis

Configure SSH keys for remote login from OME server (Section 3.3 from this:)
https://downloads.dell.com/manuals/all-products/esuprt_software_int/esuprt_software_ent_systems_mgmt/dell-openmanage-enterprise_white-papers150_en-us.pdf   




Workflow:
Blades get slotting in chassis
OME alert triggers on blade inserts and fires python script from remote server passing the IP of the CMC
Python script:
   * Waits 30 min (in case more blades are getting slotted into that chassis shortly after)
   * Looks for a lock file to determine if the script is being run on this chassis already
   * Checks each blade slot in the chassis for a blade with no IP (meaning iDrac LAN is off)
   * Enable iDrac LAN
   * Wait for iDracs to get DHCP IP, then recheck those blades for their new IPs
   * Connect to newly IP'd blades and toggle DHCP provisioning/Zero-Touch



![badge](https://forthebadge.com/images/badges/fuck-it-ship-it.svg)

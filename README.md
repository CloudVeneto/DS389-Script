# DS389-Script
Simple script for OpenLdap --> 389 Directory Server (DS389) migration 

In DS389 the list of users and/or groups to be authorized must be specified in the /etc/sssd.conf file
Since the syntax is a bit complex, we provide a simple Python script, which allows to build the sssd.conf file accoding to your needs

The script needs:
- a file (users_ldap) where to specify the list of authorized users an/or
- a file (groups_ldap) where to specify the list of authorized groups

Examples of how to fill these 2 files are provided



When you use the script, you simply need to specify the directory where these are located, e.g.:

python python_ds389.py /root

The script will customize the sssd.conf file accordingly

Then you need to restart the sssd service to implement the change:

systemctl restart sssd



import sys
import os

# Check if there is path of files users_ldap and group_ldap
# the path must be the same for the two files
if(len(sys.argv) <= 1):
	print(" ***************************************************************************")
	print(" ********************* PARAMETER NEEDED !!!!!!!!!! ************************ ")
	print(" ************** Please enter the path where the two files  *****************")
	print(" ************ \"users_ldap\" and \"groups_ldap\" are located   *************")
	print(" ** Please pay attention: the filename must be users_ldap and groups_ldap **")
	print(" ************ THE PATH MUST BE THE SAME FOR THE TWO FILES ******************")
	print(" ***************************************************************************")
	exit()

file_user_ldap = str(sys.argv[1]) + "/users_ldap"
file_group_ldap = str(sys.argv[1]) + "/groups_ldap"
file_migrate = "/etc/sssd/sssd.conf"

# backup copy original sssd.conf  file
os.system(' cp /etc/sssd/sssd.conf /etc/sssd/sssd.conf.orig')

# create temporary new file
new_sssd =  open("sssd.conf.new", "w")

ldap_string_check = 0

# read sssd.conf file and create new tempary file adding users and group required
with open(file_migrate, "r") as file_ldap:
	#print(file_ldap.readline())
	fldap=file_ldap.read().split('\n')
	#print("fldap:",fldap)
	for fl in fldap:
		#print("fl1:",fl)
		# if there is record ldap_access_filter commented, ignore it
		if (("ldap_access_filter" in fl) and (not fl.startswith('#'))):
			ldap_string_check +=1
			#string_ldap = "ldap_access_filter = (|(memberOf=cn=calcolo,ou=groups,dc=pd,dc=infn,dc=it)(memberOf=cn=CICCIO,ou=groups,dc=pd,dc=infn,dc=it))"
			#ldapsearch -x -b 'dc=pd,dc=infn,dc=it' '(|(memberOf=cn=h_lxcrescente,ou=groups,dc=pd,dc=infn,dc=it)(memberOf=cn=calcolo,ou=groups,dc=pd,dc=infn,dc=it)(&(uid=pippo)(objectclass=posixAccount)))'
			string_ldap = "ldap_access_filter = (|(memberOf=cn=calcolo,ou=groups,dc=pd,dc=infn,dc=it)"
			#print("string_ldap1: ",string_ldap)

			# Add group
			if(os.path.isfile(file_group_ldap)==True):
				print("Find file for GROUP: ",file_group_ldap)
				with open(file_group_ldap,"r") as group:
					grp=group.read().split('\n')
					for g in grp:
						if(not g):
							continue
						string_ldap = string_ldap + "(memberOf=cn={},ou=groups,dc=pd,dc=infn,dc=it)".format(g)
						print("Add GROUP: {} ok".format(g))
			else:
				print("The file \"group_ldap\" doesn't exist. No group will be added in LDAP")

			# Add Users
			if(os.path.isfile(file_user_ldap)==True):
				print("Find file for USERS: ",file_user_ldap)
				with open(file_user_ldap,"r") as user:
					usr=user.read().split('\n')
					for u in usr:
						if (not u):
							continue
						string_ldap = string_ldap + "(&(uid={})(objectclass=posixAccount))".format(u)
						print("Add USER: {} ok".format(u))
			else:
				 print("The file \"users_ldap\" doesn't exist. No users will be added in LDAP ")
			string_ldap = string_ldap + ")"
			fl=string_ldap
		#print("fl2:",fl)
		new_sssd.write(fl)
		new_sssd.write('\n')



new_sssd.close()

if (ldap_string_check > 1):
	print("please you check your sssd.conf file! you have more string ldap_access_filter declared!!!" )
	print("ERROR: procedure aborted no changes will be made ")
	exit()

# overwritting  new temporary file into sssd.conf 
os.system(' \cp -r sssd.conf.new /etc/sssd/sssd.conf')
os.system(' chmod 600 /etc/sssd/sssd.conf')


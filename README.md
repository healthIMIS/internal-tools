# Internal Tool Setup
This repository will host our internal open source tool setup which will contain productivity tools for text- and video chat, file storage with editing and collaboration features and more tools for internal use-cases.  
It is also used for planning and evaluating possible tools.  

**This is work in progress. Do not use it in live systems!**  
As soon as this repository contains a complete setup which is ready to be used, there will be a *release*.


# Install

## Clone the repository 
Clone via https:  
```git clone --recurse-submodules https://github.com/healthIMIS/internal-tools.git```  
or via ssh:  
```git clone --recurse-submodules git@github.com:healthIMIS/internal-tools.git```  

Change directory:  
```cd internal-tools/ansible/inventory```  

Initialize submodule:  
```git submodule init```


## Set up config  
Set your domain:    
```export DOMAIN=mydomain.com```

Copy example config:  
```cp host_vars/matrix.$DOMAIN/vars.example.yml host_vars/matrix.$DOMAIN/vars.yml```

Change desired settings and save the file afterwards:  
```vim host_vars/matrix.$DOMAIN/vars.yml```   

## Set up secrets:  
Copy example secrets file:  
```cp host_vars/matrix.$DOMAIN/vault.example.yml host_vars/matrix.$DOMAIN/vault.yml```

Write desired secrets and save the file afterwards:  
```vim host_vars/matrix.$DOMAIN/vault.yml``` 

Write desired password to a file, remember it (!) and save the file afterwards:  
```vim /tmp/password_file```   

Encrypt your secrets with the password file:  
```python3 ../utils/encrypt_vault_variables.py -v host_vars/matrix.$DOMAIN/vault.yml -p /tmp/password_file```  

Remember the password (!) and delete the password file:  
```rm /tmp/password_file```  

You will be prompted for the password when running the playbooks.

## Install and start services
Install matrix (synapse + element) and jitsi:  
```ansible-playbook --ask-vault-pass -i hosts ../../matrix-docker-ansible-deploy/setup.yml --tags=setup-all```

Install and start nginx and keycloak:  
```ansible-playbook --ask-vault-pass -i hosts ../playbook.yml --tags=start``` 

Start matrix (synapse + element) and jitsi:  
```ansible-playbook --ask-vault-pass -i hosts ../../matrix-docker-ansible-deploy/setup.yml --tags=start```

## Check if everything works

Run the matrix-docker-ansible-deploy self-check:  
```ansible-playbook --ask-vault-pass -i hosts ../../matrix-docker-ansible-deploy/setup.yml --tags=self-check```

Check accessibility of domains in browser:
- auth.$DOMAIN
- element.$DOMAIN
- jitsi.$DOMAIN

Go to auth.$DOMAIN and login as the admin user.  
Click "Users" and then "Add user".  
Enter a username, create the user, navigate to "Credentials" and set a (non-temporary) password for the user.  
Go to element.$DOMAIN and click "Sign In" and then "Continue with Keycloak".  
Login as the new user and confirm to log into Element with your credentials.  
You should now be logged into Element as the new user.  
Click "Explore Public Rooms" and change the server to look for rooms to "Matrix rooms (matrix.org)".  
Check that a list of public rooms is fetched and join one to confirm that federation is working properly.  
You can also test your server's federation at https://federationtester.matrix.org/.

If you made it until here, everything seems to be working!  
Congratulations!

# Stop services

Stop nginx and keycloak:  
```ansible-playbook --ask-vault-pass -i hosts ../playbook.yml --tags=stop``` 

Stop matrix (synapse + element) and jitsi:  
```ansible-playbook --ask-vault-pass -i hosts ../../matrix-docker-ansible-deploy/setup.yml --tags=stop```

# Restart services

Start nginx and keycloak:  
```ansible-playbook --ask-vault-pass -i hosts ../playbook.yml --tags=start``` 

Start matrix (synapse + element) and jitsi:  
```ansible-playbook --ask-vault-pass -i hosts ../../matrix-docker-ansible-deploy/setup.yml --tags=start```

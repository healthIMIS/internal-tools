# Open Source Tool Setup

This repository hosts our open source tool setup which contains productivity tools for text- and video chat and will
contain file storage with editing and collaboration features and more tools for internal use-cases.

In the near future we aim to provide a useful easy-to-install ansible setup that can also be used by other small
businesses or private persons.

The setup offers the following tools:

- Matrix chat (private Messages, Channels, group conversations, in-chat video and audio calls)
- Jitsi video conferencing (from chat or standalone; possibility to allow guests)
- Keycloak user management (manage user accounts; single sign-on for all services)
- *in the future: Nextcloud file storage (store and manage files; collaborative file editing)*

It is composed of the following components:

- Synapse: Matrix Homeserver
- Element: Matrix Client
- Jitsi: Videoconference Server
- Keycloak: Identity Management Server
- Nginx: Webserver

and uses these tools for server management:

- Proxmox: Virtualisation Platform with lxc containers
- ansible: automation tool

**This is work in progress. Do not use it in live systems!**  
As soon as this repository contains a complete setup which is ready to be used by others, there will be a *release*.

# Contributing

We are open for contributions!  
If you consider participating, please read our [CONTRIBUTING.md](https://github.com/healthIMIS/internal-tools/blob/main/CONTRIBUTING.md) for more information.

# Installation

## Requirements

- Debian 11
- TODO

## Clone repository

Clone via https:  
```git clone --recurse-submodules https://github.com/healthIMIS/internal-tools.git```  
or via ssh:  
```git clone --recurse-submodules git@github.com:healthIMIS/internal-tools.git```

Initialize matrix-docker-ansible-deploy submodule:  
```git submodule init```

## Set up config

Change directory:  
```cd internal-tools/ansible/inventory```

Set your domain:    
```export DOMAIN=mydomain.com```

Copy example config:  
```cp host_vars/example.org.yml host_vars/$DOMAIN.yml```

Change desired settings and save the file afterwards:
- Interface name of the server
- (static) IPv4 of the server

```vim host_vars/$DOMAIN.yml```

## Set up secrets:

We use ansible vault to protect secrets on the ansible clients:

Copy example secrets file:  
```cp vars/vault.example.yml vars/vault.yml```

Edit the file and assign strong secrets. Save the file afterwards:  
```vim vars/vault.yml```

Write strong password to a file, remember it (!) and save the file afterwards:  
```vim /tmp/password_file```

Encrypt your secrets with the password file:  
```python3 ../utils/encrypt_vault_variables.py -v ../vars/vault.yml -p /tmp/password_file```

Remember the password (!) and delete the password file:  
```rm /tmp/password_file```

You will be prompted for the password when running the ansible playbook with `--ask-vault-pass`.

## Set up server

### Initial

TODO: manual configuration (IP, network device, ...)

Start the playbook with the *initial* tag to setup sshd, proxmox, iptables and more:  
```ansible-playbook --ask-vault-pass -i inventory.yml ../initial-playbook.yml --tags=initial```

TODO: additional manual steps necessary?

### LXC containers

(This is not yet done via ansible so you have to create the containers manually.)

Use ssh to tunnel the proxmox web interface to your machine:  
`ssh -L 8080:localhost:8006 $DOMAIN`

The web interface should now be accessible at https://localhost:8080 in your browser.

Log in to your account and create three containers:

- nginx
    - IP: 10.10.10.2
    - TODO
- keycloak
    - IP: 10.10.10.3
    - TODO
- matrix
    - IP: 10.10.10.4
    - TODO: Specs!

Make sure the containers are started and running.

### SSH config

Add host and proxy command to your ssh config to connect to the containers:

```
echo "
HOST $DOMAIN
    Hostname $DOMAIN
    User ansible
    ControlMaster auto
    ControlPath ~/.ssh/cm-%r@%h:%p
    ControlPersist 5m
    IdentityFile ~/.ssh/example.com
Host 10.10.10.*
    ProxyCommand ssh -W %h:%p $DOMAIN
    User root
    IdentityFile ~/.ssh/example.com" >> ~/.ssh/config
```

You should now be able to connect to the containers like this:  
`ssh 10.10.10.2`

## Install and start services

Then you can start to install the services to their specific hosts.

### nginx

Install and start nginx:  
```ansible-playbook --ask-vault-pass -i inventory.yml ../initial-playbook.yml --limit=nginx```

Connect to the nginx container and make sure nginx is running:  
`ssh 10.10.10.2`  
`systemctl status nginx`

### keycloak

Install and start keycloak:  
```ansible-playbook --ask-vault-pass -i inventory.yml ../initial-playbook.yml --limit=keycloak```

Connect to the keycloak container and make sure the docker containers for keycloak and it's database are running and
work as expected ("healthy"):  
`ssh 10.10.10.3`  
`docker ps`

### matrix

Then, you can install matrix (synapse + element) and jitsi:  
```ansible-playbook --ask-vault-pass -i inventory.yml ../initial-playbook.yml --limit=matrix --tags=setup-all```

If the installation succeeded, start matrix (synapse + element) and jitsi:  
```ansible-playbook --ask-vault-pass -i inventory.yml ../initial-playbook.yml --limit=matrix --tags=start```

Now make sure everything works as expected with the matrix-docker-ansible-deploy self-check:  
```ansible-playbook --ask-vault-pass -i inventory.yml ../initial-playbook.yml --limit=matrix --tags=self-check```

## Check if everything works together

Check accessibility of the subdomains in your browser:

- auth.$DOMAIN
- element.$DOMAIN
- jitsi.$DOMAIN

Go to auth.$DOMAIN and login as the admin user.  
Click "Users" and then "Add user".  
Enter a username, create the user, navigate to "Credentials" and set a (non-temporary) password for the user.  
Now go to element.$DOMAIN and click "Sign In" and then "Continue with Keycloak".  
Login as the new user and confirm to log into Element with your credentials.  
You should now be logged into Element as the new user.  
Click "Explore Public Rooms" and change the server to look for rooms to "Matrix rooms (matrix.org)".  
Check that a list of public rooms is fetched and join one to confirm that federation is working properly.  
You can also test your server's federation at https://federationtester.matrix.org/.

If you made it until here, everything seems to be working!  
Congratulations!

# Hosts & Roles

In case you want to understand how the services are distributed over the **hosts** and what the used *roles* are for, you can
find a brief overview here:

### dedicated

- *user-initial*: make sure that ansible_service_user is present
- *ssh-initial*: edit sshd config and add ssh keys
- *iptables*: install iptables and implement NAT rules
- *proxmox-initial*: install proxmox
- *host-users*: authorize ssh users
- lxc containers (not yet "ansibleized"): create lxc containers for our services
    - 10.10.10.2: nginx 
    - 10.10.10.3: keycloak 
    - 10.10.10.4: matrix 

### nginx

- *nginx*: install the webserver and set up the reverse proxy to our service's containers

### keycloak

- *keycloak*: install keycloak, create realm and set up synapse client for OpenID Connect

### matrix

For installing synapse, postgres, element and jitsi we use the roles from the
awesome [matrix-docker-ansible-deploy repository](https://github.com/spantaleev/matrix-docker-ansible-deploy) that we
include as a submodule in our repository.

- *matrix-postgres*: install postgres and set up database for matrix
- *matrix-synapse*: install synapse and set up OpenID Connect with keycloak
- *matrix-client-element*: install element client
- *matrix-jitsi*: install jitsi and configure element to use it for in-chat video and audio calls
- *matrix-ma1sd*: install ma1sd matrix identity server
- *matrix-nginx-proxy*: do not install nginx-proxy, but create nginx configuration files for synapse, jitsi and more
- *matrix-coturn*: install coturn turn server and configure jitsi to use it

# Stop services
If you want to stop the services on one of the hosts, use the *stop* tag.

Stop nginx:  
```ansible-playbook --ask-vault-pass -i inventory.yml ../initial-playbook.yml --limit=nginx --tags=stop```

Stop keycloak:  
```ansible-playbook --ask-vault-pass -i inventory.yml ../initial-playbook.yml --limit=keycloak --tags=stop```

Stop matrix (synapse + element) and jitsi:  
```ansible-playbook --ask-vault-pass inventory.yml ../initial-playbook.yml --limit=matrix --tags=stop```

# Start services
For (re-)starting the services on one of the hosts, use the *start* tag.

Start nginx:  
```ansible-playbook --ask-vault-pass -i inventory.yml ../initial-playbook.yml --limit=nginx --tags=start```

Start keycloak:  
```ansible-playbook --ask-vault-pass -i inventory.yml ../initial-playbook.yml --limit=keycloak --tags=start```

Start matrix (synapse + element) and jitsi:  
```ansible-playbook --ask-vault-pass -i inventory.yml ../initial-playbook.yml --limit=matrix --tags=start```

# Credits
This project makes use of many awesome open source projects!  
We want to thank all contributors for their great work and give credit to those who provided the base for this setup.  

You can find all used third-party projects and their source and *licenses* here:
- matrix-docker-ansible-deploy ([GitHub](https://github.com/spantaleev/matrix-docker-ansible-deploy), [*AGPL-3.0 License*](https://github.com/spantaleev/matrix-docker-ansible-deploy/blob/master/LICENSE)) which uses:
  - Synapse ([GitHub](https://github.com/matrix-org/synapse))
  - Element ([GitHub](https://github.com/vector-im/element-web))
  - Jitsi ([Website](https://jitsi.org/), [GitHub](https://github.com/jitsi/jitsi))
  - Postgres ([Website](https://www.postgresql.org/), [GitHub](https://github.com/postgres/postgres))
  - Coturn ([GitHub](https://github.com/coturn/coturn))
  - ma1sd ([GitHub](https://github.com/ma1uta/ma1sd))
- Keycloak ([GitHub](https://github.com/keycloak/keycloak), [*Apache-2.0 License*](https://github.com/keycloak/keycloak/blob/main/LICENSE.txt))
- Postgres ([Website](https://www.postgresql.org/), [GitHub](https://github.com/postgres/postgres), [*License*](https://github.com/postgres/postgres/blob/master/COPYRIGHT))
- Nginx ([Website](https://nginx.org/), [GitHub](https://github.com/nginx/nginx), [*License*](https://nginx.org/LICENSE))
- Docker ([Website](https://www.docker.com/), [GitHub](https://github.com/docker), [*Apache-2.0 License*](https://github.com/docker/cli/blob/master/LICENSE))
- Docker Compose ([GitHub](https://github.com/docker/compose), [*Apache-2.0 License*](https://github.com/docker/compose/blob/v2/LICENSE))
- Ansible ([GitHub](https://github.com/ansible/ansible), [*GPL-3.0 License*](https://github.com/ansible/ansible/blob/devel/COPYING))
- Proxmox VE ([Website](https://www.proxmox.com/en/proxmox-ve), [Git](https://git.proxmox.com/), [*AGPL-3.0 License*](https://www.gnu.org/licenses/agpl-3.0.en.html))
- Certbot ([GitHub](https://github.com/certbot/certbot), [*Apache-2.0 License*](https://github.com/certbot/certbot/blob/master/LICENSE.txt))
- OpenSSL ([GitHub](https://github.com/openssl/openssl), [*Apache-2.0 License*](https://github.com/openssl/openssl/blob/master/LICENSE.txt))

In case we missed acknowledging a third-party project used in our setup, please tell us at [community@imis-innovation.de](mailto:community@imis-innovation.de) or create a pull request!







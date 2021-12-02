# brew install ansible
# or pip install ansible
# ansible --version
# vim ~/hosts
    # [local]
    # localhost
    # [fudojail]
    # 10.0.2.4
# ssh-copy-id -i ~/.ssh/id_rsa.pub localhost 
# ansible all --inventory-file=~/hosts -m ping
# 
# ------- 2 podejście do env -----------------------------------------
# ansible local -m ping
# sudo apt-get install sshpass
# sudo ansible local --connection=local -m shell -a 'echo PANDA'
# ansible fudojail -m ping
# ansible fudojail -m raw -a "fudojail list"
# --------------------------------------------------------------------
# https://github.com/geerlingguy/ansible-for-devops
# https://www.youtube.com/channel/UCR-DXc1voovS8nhAvccRZhg
# Ansible 101: Episode 1
# https://www.youtube.com/watch?v=goclfp6a2IQ&list=PL2_OBreMn7FqZkvMYt6ATmgC0KAGGJNAN
# ansible -i inventory fudojail -m ping 
# -i  - run file like a host with specific sets of clients
# create ansible.cfg in .chapter1 
# -add 'INVENTORY = inventory'
# ansible fudojail -m ping
# ansible fudojail -m ping -u pmajdanski
# ad hoc commands:
# ansible fudojail -m raw -a 'df -h'
# ansible fudojail -m raw -a 'date'
#  normaly you will user: ansible fudojail -a 'date'   but freebsd have below problems:
    # pm1990@dwt-ubuntu1:~/chapter1$ ansible fudojail -a 'date'
    # [WARNING]: Module invocation had junk after the JSON data: Exit 1
    # [WARNING]: Platform freebsd on host 10.0.2.4 is using the discovered Python interpreter at /usr/local/bin/python, but future installation of another Python interpreter could change this. See https://docs.ansible.com/ansible/2.9/reference_appendices/interpreter_discovery.html for more information.
    # 10.0.2.4 | FAILED | rc=1 >>
    # ld-elf.so.1: /usr/local/lib/libpython3.8.so.1.0: Undefined symbol "close_range@FBSD_1.6"non-zero return code
    # pm1990@dwt-ubuntu1:~/chapter1$ 
# -m what module to use
# -a argument for a module
# ansible <group in invenrory> -m <module> -a <argument for module> -u <user>
# 
# Ansible 101: Chapter1.2
# - Use vegrant to build machine locally, good for test automation
# - VirtualBox + Vegrant
# sudo apt install virtualbox
# curl -O https://releases.hashicorp.com/vagrant/2.2.9/vagrant_2.2.9_x86_64.deb
# sudo apt install ./vagrant_2.2.9_x86_64.deb
# vagrant --version
# vagrant init geerlingguy/centos7
# vagrant up 
# vagrant ssh 
# vagrant ssh-config  - jak się połączyć/ip address
# vagrant stop
# vagrant global-status - lista vagrantów i status
# vagrant provision   - przygotowuje vagranta w oparciu na vagranfile
# vagrant up          - uruchamia (jako ze mamy tam ansible uruchamia od razu )
# vagrant destroy
# --------------------------------------------------------------------
# Ansible 101: Episode 2: Ad-hoc tasks and Inventory
#   - the best is to use playbook, but if you need you can use ad hoc commands
# vagrant init geerlingguy/centos7
# - more vagrant you can see here: https://app.vagrantup.com/boxes/search
# - prepare vagrant file for chapter3
# vagrant up
# vagrant global-status
# ansible multi -i inventory -a "hostname"
#  -if we dont specify module ansible will use by default command module
#  - ansible run in parrarel matter - so order will be different each time
# ansible multi -i inventory -a "hostname" -f 1
#  - with -f 1 you force ansible to got one at a time and wait for response
# ansible db -i inventory -m setup
#  - setup show all info what ansible collect
# ansible multi -i inventory -b -m yum -a "name=ntp state=present"
#  -b become different users, so use sudo
# ansible multi -i inventory -K -b -m yum -a "name=ntp state=present" 
#  - -K  or use --ask-become-pass - if sudo require password 
# ansible multi -i inventory -b -m service -a "name=ntpd state=started enabled=yes"
# ansible-doc service - give you documentation for any module
# ansible multi -i inventory -b -a "service ntpd stop"
# ansible db -i inventory -b -m mysql_user -a "name=django host=% password=12345 priv=*.*:ALL state=present" (it will faill)
# --------------------------------------------------------------------
# Ansible 101: Episode 3: Introduction to Playbooks
# (copied vagrantfile and inventory from chapter3)
# ansible -i inventory multi -a "date"
# Background task:
# ansible -i inventory multi -b -B 3600 -P 0 -a "yum -y update"
#   - B how log it take
#   - P 0 it will exite after 0 sec (so right now)
# ansible -i inventory multi -b -m async_status -a "jid=839784546947.2860"
#   -m async_status -a "jid=839784546947.2860" <- return status of specific job
# ansible -i inventory db -b -m async_status -a "tail /var/log/messsages"
# ansible -i inventory db -b -a "tail /var/log/messsages"  < to check logs
# ansible -i inventory db -b -m shell -a "tail /var/log/messsages"
#   - good practise is to not use shell
# ansible -i inventory db -b -m cron -a "name=something hour=4 job=/path/to/script.sh"
# ansible -i inventory db -b -m git -a "repo=github_repo dest=opt/app update=yes version=2.1.2"
# - Use pipelining = True in ansible.cfg - so ssh connection will be use over and over insted of reastablishing connection
# vagrant destroy -f   <- destroy 3 servers currently running
# AWS - połączenie do ec2:
#   sudo ssh ubuntu@34.228.212.78 -i /Users/przemyslawmajdanski/Documents/DevOps/panda2.pem
# create playbook.yml 
#   --- <-  this is seperator for multiple yml document in one file
# - we create playbook that fit shell script. 
# ansible-doc yum
# sudo ansible -i inventory ec2 -m ping
# ansible -i inventory ec2 -m ping
# ansible-playbook -i inventory playbook2.yml
# ansible-playbook -i inventory multi --limit=10.0.0.1 playbook2.yml  <- to run command only on one ip address
# ansible-inventory --list
# --------------------------------------------------------------------
# Ansible 101: Episode 4: Your first real-world playbook
# - setup machine in AWS & playbook file
# ansible-playbook main.yml --syntax-check
# ansible-playbook -i inventory main.yml --syntax-check <- to check playbook 
# ansible-playbook -i inventory main.yml <- run playbook
# --------------------------------------------------------------------
# Ansible 101: Episode 5: Your first real-world playbook
# ansible-playbook -i inventory playbook.yml
# ansible -i inventory all -m ping
# ansible-playbook -i inventory playbook.yml --force-handlers   <- tp force run handlers
#   - not all handlers must run, keep this in mind. 
#   playbook2.yml - present what to do when thee is more than one OS family in inventory
# ansible -i inventory ec22 -m setup <- to gather facts about specific machine from inventory - and then use those facts in ansible playbook
# - debug: var=foo['status']['After'] to get specific facts
# --------------------------------------------------------------------
# Ansible 101: Episode 6: Ansible Vault and Roles
#   - ansible vault is added as a feature (you can use hashicorp insted)
# ansible-vault encrypt vars/api_key.yml <- to encrypt file with passwords. 
# ansible-playbook playbook.yml --ask-vault-pass <- to ptomtp for password
# ansible-playbook playbook.yml --vault-password-file ~/.ansible/api-key-pass.txt <- to use file as a password
# ansible-vault decrypt vars/api_key.yml  <- to decrypto file
# ansible-vault rekey vars/api_key.yml <- to change a password
#   - you can have blocks of tasks and if they fail you can have resque tasks
#   - if it look like programing work so you stoped automating!
# Playbook organization:
#   - keep handlers in seperate file
#   - use import_tasks
#   - with import_tasks you can overwrite variable used in those tasks
#   - include_tasks: tasks/log.yml - allow to dynamically changing tasks using include.
#   - import_playbook: playbook3.yml <- to umport playbook
#   - import work as you will copy those task from other file to current playbook. 
# Nodejs playbook + vagrant examples:
# vagrant global-status
# vagrant up
# ---------
# Upgrade Vagrant:
#   brew install vagrant
#   vagrant plugin expunge --reinstall
#   vagrant up
# ---------
#   - its good to use roles (sets of task that can be used in many playbook)
# role require two folders: meta & tasks
#   - you an use include_roles 
# ansible-galaxy role init test <- to create role, with all subfolders
# --------------------------------------------------------------------
# Ansible 101: Episode 7: Molecule Testing and Linting and Ansible Galaxy
#   - if you working with docker ou can also use ansible
# 00-Ansible Galaxy:
#   - https://galaxy.ansible.com/
#   - how to get roles:
# ansible-galaxy role install geerlingguy.homebrew --ignore-certs 
#    --ignore-certs <- allow to solve problem with [SSL: CERTIFICATE_VERIFY_FAILED] 
#   - its good to install roles from galaxy locally, to use for specific playbook
#   - ansible cfg file with 'role_path = ./roles' tell where we can find file with roles
# ansible-galaxy install -r requirements.yml --force --ignore-certs <- to install role from galaxy based on requirements
# ansible-playbook main.yml -K
# to find installed roles: cd ~/.ansible/roles/
# 01-Debug:
#   - there should be many level of tests;
#   Ansible testing spectrum(move from yamliinit to parallel inf):
#       - yamllint
#       - ansible-playbook --syntax-check
#       - ansible-line
#       - molecule test (integration)
#       - ansible-playbook --check (against prod)
#       - parallel infrastructure
# pip3 install yamllint 
# yamllint .  <- check current dir and return results
#  we can create .yamllint file to adjust rules for checks.
# ansible-playbook main.yml --syntax-check <- to perform syntac check. it not check if playbook can be run only syntax
# pip3 install ansible-lint
# ansible-lint main.yml <- more detail check than syntax
#   - lint is good to keepi good practice.
# Molecule testing!:
# pip3 install molecule
# molecule init role myrlole (the same as 'ansible-galaxy role init myrole' but withour role structure for molecule)
# molecule.yml - describe how molecule will run tests
# molecule test <- rune inside role folder
#  ! Some problem with run molecule+docker
# molecule login <- to logi into created test machine.
# --------------------------------------------------------------------
# Ansible 101: Episode 8: Playbook testing with Molecule and GitHub Actions CI
# - for dev& testing ansible role,playbook 
# molecule init scenario     <- to initilize scenario
#   -edit converge.yml inside maolcule/default to: run specific playbook not entire folder & update cahce to avoide problem with packages. 
# molecule converge
# ---------------------
# Virtual Env:
# pip3 install virtualenv 
# virtualenv venv 
# source venv/bin/activate
# deactivate
# virtualenv venvMolecule
# source venvMolecule/bin/activate
# pip freeze > requirements.txt
# pip install -r requirements.txt
# ---------------------
# Fudojail:
# ansible -i inventory fudojail -m ping
# ansible-playbook -i inventory main.yml
# 
# ---------------------
# 
# docker run hello-world <- test docker
# - Problem appear to be cause by docker lackness on mac
# molecule init scenario <- create default scenario in this dir
# molecule converge <- to build env for test
# command: bash -c "while true; do sleep 10000; done"
# docker ps
# molecule login
# molecule list
# molecule destroy 
# molecule init role myrlole -d docker
# molecule test
# 2 working instances on chapter8.3(base) & 8.4(experiments) ready for molecule test:
# image: "geerlingguy/docker-${MOLECULE_DISTRO:-centos8}-ansible:latest" <- lets use this and then we can:
#   MOLECULE_DISTRO=debian10 molecule converge <- it will replace centos8 with debian10
# molecule verify <- when you already prepared env using converge, you can run: molecule verify, and this will return only effect of verify.yml playbook. 
#   - you can add verification into playbook (it will always be checked) or you can have seperate verify.yml
# lint: | <- in moelcule.yml aow you run scripts for lint, it will use .yumlint 
# molecule lint <- to only check syntax/construction of your playbooks
# 
# 
# ---------------------
# GIT:
# echo "# test" >> README.md
# git init
# git add README.md
# git commit -m "first commit"
# git branch -M main
# git remote add origin https://github.com/przemaj1990/test.git
# git push -u origin main
# git status
# ---------------------
# Add Workflow to repository:
# - add .github/workflow/ci.yml
# git add -A
# git commit -m "add CI workflow for GitHub actions"
# git push    <- on push the ci will run action and test code. 
# git checkout -b test 
# git add -A 
# git push -u origin test
# gh auth login  
# gh pr create 
# git push -u origin test 
# gh pr create 
# git commit -m 'error creation'
# gh pr create 
# --------------------------------------------------------------------
# Ansible 101: Episode 9 - First 5 min server security with Ansible
# '5 minutes security':
#   - Use secure&encrypt communication (ssh, disable password base auth, use key-auth as it better for automation, run ssh on different port, )
#   - diable root login and use sudo (at minimul use user with sudo right, only users that should have access) 
#   - remove unused software & open only required ports
#   - use the principle of least privilage
#   - Update the OS and instlled software
#   - use a properly-configured firewall
#   - make sure log files are populated and rotated
#   - Monitor logins and block suspect ip
#   - Use SELinux
# 
# if you change ssh config, its good to have backup session open to log into server if problem appear, and fix it manually
# all example included in chapter9/main.yml
#  nmap 54.152.11.204 <- to scan ports on end device
#  https://galaxy.ansible.com/geerlingguy/security <- security role for linux
# 
# --------------------------------------------------------------------
# Ansible 101: Episode 10: Ansible Tower and AWX
#   - AWX - community, to support official
#   - tower - official
# https://github.com/geerlingguy/tower-operator <- tower-operator
# brew install minikube 
# minikube start --memory 8g --cpus 4
# minikube addons enable ingress
# as problem appeared I changed settings of docker & restarted
# kubectl get pods --all-namespaces <- show kubernetest cluster
# minikube delete
# brew install hyperkit
# brew link hyperkit
# minikube start --memory 8g --cpus 4
# minikube addons enable ingress <- allow to access example-tower.test
# cd tower-operator-master insert into download git repo: https://github.com/geerlingguy/tower-operator.git
# molecule test -s test-minikube
# brew install tree 
# --------------------------------------------------------------------
# next try base on: https://github.com/ansible/awx-operator 
# minikube start --cpus=4 --memory=6g --addons=ingress
# minikube kubectl -- get nodes
# minikube kubectl -- get pods -A
# alias kubectl="minikube kubectl --"
# export NAMESPACE=my-namespace
# git clone https://github.com/ansible/awx-operator.git
# cd awx-operator 
# make deploy
# kubectl get pods -n $NAMESPACE <- check if running
# kubectl config set-context --current --namespace=$NAMESPACE  <- set current namespace for kubectl
# check awx-demo.yml there metadata.name will be name of awx deployment
# kubectl apply -f awx-demo.yml
# kubectl logs -f deployments/awx-operator-controller-manager -c awx-manager <- check logs where installtion process is at all
# --------------------------------------------------------------------
# next try base on: https://app.pluralsight.com/player?course=red-hat-ansible-tower-managing&author=red-hat&name=312fbe09-5220-4419-b71d-5857800a7241&clip=0
# Ansible Tower:
#   - contorl node (with ansible installed)
#   - managed hosts
# https://releases.ansible.com/ansible-tower/setup-bundle/ <- link to release of ansible
# https://www.ansible.com/products/controller <- limk to ansible tower
# download nad extract last version
# - set up 3 password inside inventory
# sudo ./setup.sh
# as its not worked on MAC i moved to redhat on cloud:
# wget https://releases.ansible.com/ansible-tower/setup-bundle/ansible-tower-setup-bundle-3.8.4-1.tar.gz
# tar xzvf ansible-tower-setup-bundle-3.8.4-1.tar.gz
# cd ansible-tower-setup-bundle-3.8.4-1
# - set up 3 password inside inventory
# sudo ./setup.sh
# https://3.230.150.252/
#   - Generate subscription base on: https://docs.ansible.com/ansible-tower/3.8.4/html/userguide/import_license.html#obtain-sub-manifest
#   - upload whole manifest.zip file
# - admin/password
#   - set up users & privilage/access
#   - admin - full access
# type of access: admin(admin right to object), read, execute(on job template)
#   - ogranization - logicall collection of team&projects&inv
#  https://app.pluralsight.com/course-player?clipId=c247b596-7f69-469c-9d8b-66bfd8ad3f8b <- course how to manage tower
#   - static inventory
# --------------------------------------------------------------------
# Ansible tower && with https://www.youtube.com/watch?v=iKmY4jEiy_A&list=PL2_OBreMn7FqZkvMYt6ATmgC0KAGGJNAN&index=12
# min 22
# ansible-galaxy install -r requirements.yml 
# if you are using ansible-galaxy lower than 2.9 or older - you need two separate installation:
#   ansible-galaxy role install -r requirements.yml 
#   ansible-galaxy collection -r requirements.yml 
# for errors: [SSL: CERTIFICATE_VERIFY_FAILED]:
# ansible-galaxy install -r requirements.yml --ignore-certs
# --------------------------------------------------------------------
# Ansible 101: Episode 11 - Dynamic Inventory and Smart Inventories
# https://www.youtube.com/watch?v=_rDzMYp-fBs&list=PL2_OBreMn7FqZkvMYt6ATmgC0KAGGJNAN&index=11
#   - its good to have all hosts in: /inventory/hosts.ini
#   - and all vars in /inventory/group_vars/all.yml
# ansible-inventory -i inventory/hosts.ini --list   <- to check inventory and how ansible see it.
# chmod +x inventory/inventory-php 
# inventory/inventory-php --list
# inventory/inventory-php --host
# ansible-inventory inventory/inventory-php --list
# ansible-inventory inventory/inventory-php --host 3.210.205.104
# ansible-playbook -i inventory/inventory-php main.yml
# /inentory/inventory-python <- example of dynamic inv in pyhon
# ansible-inventory inventory/inventory-python --list
# ansible-inventory -i inventory/inventory-python --list    <- how ansible see inventory, for tshoot
# ansible-inventory -i inventory/inventory-python --graph   <- hosts by group
# ansible-inventory -i inventory/inventory-python --list -y <- yml formal
# pip3 install boto3 <- solve problem
# /inventory/demo.aws_ec2.yml <- how to use plugin with aws
#   hostnames:
#       - test        <- give you all valid options
# - Inventory should be version control with projects;
# AWS IAM: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp.html <- we can ghenerate access for script to et list of nodes;
# https://docs.ansible.com/ansible-tower/latest/html/userguide/credentials.html#amazon-web-services <- plugins for inventory
# - you can have multiple inventory, just put 2 scripts in the same directory: inventory/
# ansible-inventory -i inventory/ --list
# --------------------------------------------------------------------
# Ansible 101: Episode 12 - Real-world Ansible Playbooks
# https://www.youtube.com/watch?v=_QZr4xKhir4&list=PL2_OBreMn7FqZkvMYt6ATmgC0KAGGJNAN&index=13
#   blocks - few task togheter, if one fail whole block fail
#   rescure - can react on problem with one of blocks
#   ansible-playbook playbook.yml --tags deploy <- use only task with deplot tag
# https://github.com/geerlingguy/ansible-for-devops/tree/master/deployments-balancer <- deploy-balancer
# ansible-galaxy install -r requirements.yml --ignore-certs
# vagrant up
# curl -Is http://192.168.4.2 | grep Cookies;
# curl -Is http://192.168.4.2/ <- if you use few time you see changed ip as there is loadbalancer
# - use post taks from /Users/przemyslawmajdanski/Documents/DevOps/Ansible/chapter12/deployments-balancer/playbooks/deploy.yml
#   post task will check if node is up. So you will know if everything is working correctly. 
#  vagrant destroy -f
# serial: 1 <- tell to operate on one server at a time(so finish playbook on one server and move to second one)
# Node.js example (https://github.com/geerlingguy/ansible-for-devops/tree/master/deployments-rolling)
# ansible-galaxy install geerlingguy.firewall --ignore-certs --force <- before start vagrant install roles.
# ansible-playbook -i inventory playbooks/deploy.yml
# --------------------------------------------------------------------
# Ansible 101 - Episode 13 - Ansible Collections and a Test Plugin
# ansible-playbook main.yml -c local -i "localhost," <- to run only localy
# How to create plugins:
#   - create directory /test_plugins
#   - then when you create ex. red.py, you can use red as variable for method inside :)
# Collections:
#   - create folder /collections
#   - ansible-galaxy collection init local.colors --init-path ./collections/ansible_collections
#   - you need to use namespece
#   - you need to give collection --init-path to tell where create collection
#   - only galaxy file is required, rest is optional
#   - in plugin/redme you have instruction what type of folders are supported
# mkdir collections/ansible_collections/local/colors/plugins/test < new folder test
# now when you have collection and you added red.py into /plugins/test/ , you need to refere to plugin - so whole FQCN: local.colors.blue 
# - you can use in main.yml:
#   [defaults]
#   collection_paths = ./collections <- and this will overwritte base collections
# - is good to use requirements file…
# ansible-galaxy install -r requirements.yml
# ansible-galaxy role install -r requirements.yml
# ansible-galaxy collections install -r requirements.yml
# - in main.yml you can add:
#   collections:
#       - local.colors <- then you can just use red insted of local.colors.red 
#   roles:
#       - local.colors.red <- to install that role 
# ansible-test <- for test collections;
# --------------------------------------------------------------------
# Ansible 101 - Episode 14 - Ansible and Windows (not for me)
# https://github.com/geerlingguy/ansible-for-devops/issues/289
# -install powershell
# using powershell install subsystem linux
# then install pip3
# use pip3 to install ansible :) 
# --------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# DevOps with GitHub and Azure: The Big Picture - https://app.pluralsight.com/course-player?clipId=44dd0a31-0bde-476d-bbfa-41313addb4dc
# Part I: Understanding Continuous Delivery and DevOps with GitHub and Azure
# --------------------------------------------------------------------
# - Source Control: Github
# New repo for this work: https://github.com/przemaj1990/Github_Azure_Ansible
# Greate introduction from Github:
# Quick setup — if you’ve done this kind of thing before
# or	
# https://github.com/przemaj1990/Github_Azure_Ansible.git
# Get started by creating a new file or uploading an existing file. We recommend every repository include a README, LICENSE, and .gitignore.
# …or create a new repository on the command line
# echo "# Github_Azure_Ansible" >> README.md
# git init
# git add README.md
# git commit -m "first commit"
# git branch -M main
# git remote add origin https://github.com/przemaj1990/Github_Azure_Ansible.git
# git push -u origin main
# …or push an existing repository from the command line
# git remote add origin https://github.com/przemaj1990/Github_Azure_Ansible.git
# git branch -M main
# git push -u origin main
# --------------------------------------------------------------------
# git branch -M main <- rename branch
# CODEOWNERS.txt <- define who have right to access your code
# https://github.com/przemaj1990/Github_Azure_Ansible/settings/branches <- go there to setup branch protection rules.
#   Github Issue - to deliver software (metadata about specific part of work like bug, use markdown to trace work) ex: https://github.com/przemaj1990/Github_Azure_Ansible/issues/2
#       - milestones - to prioritize issues
#       - label
#   Github Project - to describe feature
#       - you can use comment during makieng change like: 'Fixes #4' and this way you will collerate change with bug #4 
#   Github kaban board - to show how work is done now,
#   Github Backlog - list of work
#   Github Pages - publi documentation
#       - Settings>Pages>choose branch and create
#       - https://przemaj1990.github.io/Github_Azure_Ansible/ <- example of ready website
#       - Page for client, wiki internal
#   GitHub Actions - Automation Engine
#       - CI / continous integration
#       - CD / continous deployment
#       - automation of pull request
# Using Action + Azure:
# got to: App Services -> Create new one and connect with git:
#   movie with steps:    https://app.pluralsight.com/course-player?clipId=fb93df3e-cedd-48a2-a899-0e94bda55078
#   new app: https://githubazureansible.azurewebsites.net/
#   - after connecting this on Azure in Github/Action appear connection to Azure
# --------------------------------------------------------------------
# Create Qucik Django App: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/development_environment
# pip3 install django
# python3 -m django --version
# mkdir django_app
# cd django_app
# django-admin startproject mytestsite
# cd mytestsite
# python3 manage.py runserver
# pip3 freeze > requirements.txt
# --------------------------------------------------------------------

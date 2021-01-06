AnsibleDB - OpenSource
============================
Ansibledb_collection gives you the ability to quickly collect facts about your server estate and via our API, pull out the information important to you. If you've used puppetDB, the functionality is almost identical. With ansibleDB OpenSource, you can also create dynamic ansible inventories to target specific servers with a specific action.

You need to first install and setup our ansibledb_api_opensource repo:
https://github.com/apidb-io/ansibledb_api_opensource

The collection roles are maintained by APIDB LTD

Includes:

 * apidb_localfacts
 * apidb_collect
 * apidb_post

Usage
-----

Install the collection locally:
````
$ ansible-galaxy collection install apidb.ansibledb_opensource -p ./collections
````

Requirements
------------

Only if your control node is Ubuntu or RHEL/Centos/OEL 8, you may need to install ````python-requests```` to use this collection.
````
$ sudo apt-get install -y python-requests
````
or
````
$ yum install -y python-requests
````

Dependencies
------------

 * Ansible >= 2.7
 * Python >= 2.7

STEP 1
------
You need to first install and setup our ansibledb_api_opensource repo:

https://github.com/apidb-io/ansibledb_api_opensource


STEP 2
------

<details>
 <summary>Setup fact collection</summary>
  <p>

# Setup fact collection:
Once Ansibledb_api_opensource is setup, go ahead and setup this repo to start collection and posting facts into ansibledb_api_opensource.


Example deployment file
-----------------------
Create your own ````deploy.yml```` file and add the contents below.

    ---
    - name: collect facts
      hosts: all
      collections:
        - apidb.ansibledb_opensource
      tasks:
        - import_role:
            name: apidb_localfacts
          tags: facts
    
        - import_role:
            name: apidb_collect
          tags: collect
    
    - name: Post to APIDB
      hosts: localhost
      connection: local
      gather_facts: false
      collections:
        - apidb.apidb_collection
      roles:
        - role: apidb_post
          tags: post


Set-up the group_vars
---------------------
Run the following command to add a group_vars/all file and add the TOKEN:

 * ````mkdir group_vars````
 * Now add the endpoint ````vi group_vars/all````
 * Add the following to the file.

````
---
ansibledb_server: "http://ansibledb_api_IP_Address:5000"

````
 * Now save the file.
 
ansible.cfg
-----------
Consider adding these settings to your ansible.cfg file under ````[defaults]````

 * Forks allows to run more concurrent runs than the default of 5.
 * Inventory should point to your inventory file
 * display_skipped_hosts won't show all the "skipped" ansible code.

````
[defaults]
forks = 20
inventory = inventory
display_skipped_hosts = false
````

Intital run
-----------
Now you've setup ansibledb_opensource, run it to check everything is working and you have connectivity.

````
ansible-playbook  deploy.yml
````


Adding your own Custom Facts
----------------------------
We've setup a simple way for your to run you're own custom playbooks to collect facts important to you. Follow this process:

**Option 1**:
Use our prepared facts from our [custom_extensions](https://github.com/apidb-io/custom_extensions) repo in github.

 * Clone the repo into the same base DIR as our collection: ````git clone https://github.com/apidb-io/custom_extensions.git````
 * Edit the main.yml ````vi custom_extensions/main.yml```` 
 * Un-hash the playbooks you would like to run. Some fact collections will only work on specific operating system versions.

````
    - custom_extensions/extensions/tidyup.yml # Cleans out old files
#    - custom_extensions/extensions/sample_facts.yml # My own loacl fact collection populates the dashboard.
#    - custom_extensions/extensions/cis.yml # Checks CIS controls against RHEL7
#    - custom_extensions/extensions/packages.yml # adds packages intot he dashboard.
#    - custom_extensions/extensions/sysctl.yml # Add sysctl settings into the dashboard.
````
 * Run the playbook as below:

````
ansible-playbook deploy.yml
````

**Option 2**:
You're free to add your own playbooks into the same directory once you create it and they will be picked up when the apidb collection runs.

 * In the same base DIR of the collection, create the directory: ````mkdir custom_extensions````
 * Add your own playbooks templates, files etc into this DIR.
   * To create your own facts, you need to create a file **ON THE REMOTE SERVERS** in ````/tmp/local/<name>.fact```
   * Add a title to line one like this: ````[fact_name]````
   * The facts need to be in this format ````key: value````:

**I.E**

````
[local_facts]
cloud: AWS
INSTANCE_TYPE: t2.micro
AVAIL_ZONE: eu-west-1b
REGION: eu-west-1
````

 * Run the playbook as below and  nsibledb_openshift will collect the facts and insert them into the DB. 

````
ansible-playbook deploy.yml
````


Performance tuning
------------------
If you're running against lots of servers, you can utilise the ````ansible.cfg```` "forks" setting. The default is 5 forks but you can increase this (depending on the size of your control node). You will need to do some testing, but you should be able to double or triple the number of forks you run.

**I.E.**
````
[defaults]
forks = 20
````

How to use the  API
-------------------
To pull out server and fact information directly from the database. Here are some examples:

 * Pull out all data:

    ````curl -s http://ansibledb_api_IP_address:5000/api/servers | jq````

 * List all servernames, distribution and version:

    ````curl -s http://ansibledb_api_IP_address:5000/api/servers | jq '[.[] | {name:.ansible_facts.ansible_fqdn, distribution:.ansible_facts.ansible_distribution,  version: .ansible_facts.ansible_distribution_version}]'````

 * Generate a list of servernames that match a specific fact (in this case ubuntu 18.04):
 
    ````curl -s http://35.177.212.236:5000/api/servers | jq --arg INPUT "$INPUT" -r '.[] | select(.ansible_facts.ansible_distribution_version | tostring | contains("18.04")) | (.ansible_facts.ansible_fqdn+"\"")'````


</p></details>

License
-------
BSD

Author Information
------------------
This role has been create by the APIDB team. Further information and contact is available from [here](https://www.apidb.io/)

Disclaimer
----------
The ansible facts you send to APIDB will be stored in our DB. This will be remote from your company datacentre. Only send facts you are happy to send and make use of the "Resticted Keys" functionality. We also offer an onsite solution where we can setup APIDB within your own Datacentre, removing many security concerns.

Contact us for pricing and setup information.

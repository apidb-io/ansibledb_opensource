AnsibleDB - OpenSource
============================
AnsibleDB gives you the ability to quickly collect facts about your server estate and via our API, pull out the information important to you. If you've used puppetDB, the functionality is almost identical. With ansibleDB OpenSource, you can also create dynamic ansible inventories to target specific servers with a specific action.

The collection roles are maintained by APIDB LTD

Includes:

 * apidb_localfacts
 * apidb_collect
 * apidb_post
 * ansibleDB-opensource

Usage
-----

Install the collection locally:
````
$ ansible-galaxy collection install apidb.apidb_collection -p ./collections
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
The collection comes in two parts. The first thing you will do it setup ansibleDB-opensource. Follow these instructions:

<details>
 <summary>AnsibleDB-OpenSource Setup</summary>
  <p>

# ansibledb-opensource

ansibledb-opensource is way to send data from ansible to an api and then read that data. You will need to install the ansibledb-opensource collection from Ansible galaxy and configure it to point to your API server

This is the API Server that recieves requests from Ansible and also offers an end point to get your data

## Installation

Clone the Repository
```bash
$ git clone https://github.com/apidb-io/ansibledb-opensource.git
$ cd ansibledb-opensource/
```

Install python3 and requirements (YUM based)
```bash
$ yum install python3
$ pip3 install -r requirements.txt
```

Install python3 and requirements (APT based)
```bash
$ apt install python3 python3-pip
$ pip3 install -r requirements.txt
```

#### Install MongoDB Server (Community) from:
```url
https://www.mongodb.com/try/download/community
```

#### Example: Centos 8 (Mongo version 4.4)
```bash
wget https://repo.mongodb.org/yum/redhat/8/mongodb-org/4.4/x86_64/RPMS/mongodb-org-server-4.4.3-1.el8.x86_64.rpm
yum localinstall mongodb-org-server-4.4.3-1.el8.x86_64.rpm
systemctl start mongod 
systemctl enable mongod
systemctl status mongodb
```

#### Example: Ubuntu 18.04 (Mongo version 3.6)
```bash
apt install mongodb
systemctl enable --now mongodb
systemctl status mongodb
```

## Running the Server

```bash
python3 server.py
```

## Usage

#### Get Server Versions (using JQ to filter)

Install JQ:
````
apt/yum install jq
````

Now use JQ to pull out the data you want to see.
```bash
curl -s http://<URL>/api/servers | jq '[.[] | {name:.ansible_facts.ansible_fqdn, distribution:.ansible_facts.ansible_distribution,  version: .ansible_facts.ansible_distribution_version}]'
```

## Production
In order to use this in production, we suggest using uwsgi and something like nginx in front of it.

CentOS 7
```url
https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-centos-7
``` 
Ubuntu 20
```url
https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-20-04
```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)

</p></details>


STEP 2
------

<details>
 <summary>Setup fact collection</summary>
  <p>

# Setup fact collection:
Once AnsibleDB-opensource is setup, go ahead and setup the collection and posting scripts.


Example deployment file
-----------------------
Create your own ````deploy.yml```` file and add the contents below.

    ---
    - name: collect facts
      hosts: all
      collections:
        - apidb.apidb_collection
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
 * Now add the TOKEN ````vi group_vars/all````
 * Add the following to the file. Your TOKEN can be found on your "profile" page on [the APIDB dashboard](https://app.apidb.io/profile)
 
````
---
apidb_token: "your-token"
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

Security
--------
We do not collect your secure data. We use "restricted keys" to stop certain fields being sent to APIDB. You have the control to add additional keys or remove the defaults.

<img src="https://raw.githubusercontent.com/apidb-io/apidb-collection/master/apidb_screenshot4.JPG"> 

Intital run
---------
Now you have the collection downloaded, you can complete the first run to check everything is working and you have connectivity. Once run, your dashboard will display distrubution, kernel, operatingsystem and uptime values.

````
ansible-playbook  deploy.yml
````

First Fact run complete
-----------------------
You should now have successfully collected the 4 Ansible facts available and can view them on the dashboard. If you click on the servers tab or on one of the servers on the dashboard, you can view specific server information.

The power of APIDB really comes into it's own when you add your own facts. These can be anything from the datacentre a server is in, to the version of a particualr piece of software. If you want to add your own facts, you have two options below.

Adding your own Custom Facts
----------------------------
We've setup a simple way for your to run you're own custom playbooks to collect facts important to you. Follow this process:

**Option 1**:
Use our prepared facts from our [custom_extensions](https://github.com/apidb-io/custom_extensions) repo in github.

 * Clone the repo into the same base DIR as our collection: ````git clone https://github.com/apidb-io/custom_extensions.git````
 * Edit the main.yml ````vi custom_extensions/main.yml```` 
 * Un-hash the playbooks you would like to run
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

 * Run the playbook as below and the APIDB collection will collect the facts and display them in the dashboard:

````
ansible-playbook deploy.yml
````

Dashboard
---------
Check the APIDB dashboard for your new data.

Performance tuning
------------------
If you're running against lots of servers, you can utilise the ````ansible.cfg```` "forks" setting. The default is 5 forks but you can increase this (depending on the size of your control node). You will need to do some testing, but you should be able to double or triple the number of forks you run.

**I.E.**
````
[defaults]
forks = 20
````

Experimental Kubernetes role
---------------------------
This role is currently under development but is available for you to test.
Expectations/limitations:

<img src="https://raw.githubusercontent.com/apidb-io/apidb-collection/master/kubernetes_cluster.JPG">


 * This role will only run against Bastion host(s) - (A host that can connect to your kubernetes master).
 * Authentication: Currently only support the kubeconfig file (This will need to be updated manually).
 * Username/Password & TOKEN authentication is being developed.

Manage your kubeconfig files in the ````group_vars/all```` file. Add the location of your kubeconfig file as below. If you have multiple clusters, you can add multiple kubeconfig files.

````
kubeconfig:
  - "$HOME/.kube/test-cluster.yml"
  - "$HOME/.kube/dev-cluster.yml"
````

To use the Kubernetes role, add the following to the deploy.yml file:

    - name: Sample kubernetes data collection
      hosts: localhost
      connection: local
      gather_facts: false
      collections:
        - apidb.apidb_collection
      tasks:
        - import_role:
            name: apidb_kubernetes
          tags: k8s
          when: '"k8s" in ansible_run_tags'
      tags: gather


You will need to update the ````hosts:```` to point to your bastion server.

Usage:
````
ansible-playbook  deploy.yml --tags=gather,k8s,post
````

APIDB API
---------
You also have the option to use the APIDB API to pull out server and fact information directly from the database. Here are some examples:

 * Export your APIKEY first (Found on the profile page):

    ````export apikey=1234567891011121314151617````

 * Server list:

    ````curl --silent -X GET https://app.apidb.io/api/servers   -H "Authorization: Token $apikey"  -H "Accept:application/json" | jq````

 * List all production servers:

    ````curl --silent -X GET https://app.apidb.io/api/facts/environment/production   -H "Authorization: Token $apikey" -H "Accept:application/json" | jq````

 * List all production server but only show Servername & Environment:

    ````curl --silent -X GET https://app.apidb.io/api/facts/environment/production   -H "Authorization: Token $apikey" -H "Accept:application/json" | jq '[.servers[] | {name: .fqdn, Env: .factvalue}] | group_by(.fqdn, .factvalue)'````

 * Show all CentOS 6.9 servers:
 
    ````curl --silent -X GET https://app.apidb.io/api/facts/operatingsystem/"centos 6.9"   -H "Authorization: Token $apikey" -H "Accept:application/json" | jq '[.servers[] | {name: .fqdn, Env: .factvalue}] | group_by(.fqdn, .factvalue)'````

 * List all T2.small instance types:

    ````curl --silent -X GET https://app.apidb.io/api/facts/instance_type/t2.small   -H "Authorization: Token $apikey" -H "Accept:application/json" | jq '[.servers[] | {name: .fqdn, Env: .factvalue}] | group_by(.fqdn, .factvalue)'````

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

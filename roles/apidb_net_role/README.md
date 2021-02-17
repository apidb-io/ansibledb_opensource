Apidb_collect_net
============================
Apidb_collect_net role gives you the ability to quickly collect facts from your Network Devices and via our API, pull out the information important to you. If you've used puppetDB, the functionality is almost identical. With ansibleDB OpenSource, you can also create dynamic ansible inventories to target specific servers with a specific action.

Like our sister collection (ansibledb_opensource - for linux and windows), we have seperated our network devices because the data and facts they collect are not the same. Although it's possible to combine ansibledb_opensource and ansibledb_net into one larger collection, it's not advised simple because the datasets are so different.


Network Devices
---------------
We are adding more supported network devices all the time. Here is a list of the currently supported devices:

  * Palo Alto
  * Cisco

Setup
--------------

You need to first install and setup:

- [ansibledb_api_opensource repo](https://github.com/apidb-io/ansibledb_api_opensource)  
- [ansibledb_opensource](https://github.com/apidb-io/ansibledb_opensource)

This role is maintained by APIDB LTD

Includes:

 * apidb_collect_net

Usage

Saves this role in the apidb_opensource collection under roles


Dependencies
------------
 * Ansible >= 2.9
 * Python >= 2.7
 * Tested with ````jq```` version 1.5.1
 * Collection from the network vendor for example Cisco or Palo

Each specific Network Device will need to utilise it's own vendors collection. The below deployment file gives an example of using Palo Alto and Cisco devices, but you will need to install the vendor collections, before you can collect the facts. For more information see:

- [Palo Alto](https://paloaltonetworks.github.io/pan-os-ansible/)
- [Cisco](https://github.com/ansible-collections/cisco.ios)



Example deployment file
-----------------------
Create your own ````deploy.yml```` file and add the contents below.

    ---
    - name: collect facts
      hosts: all
      collections:
        - apidb.ansibledb_net
      tasks:
        - import_role:
            name: 
          tags: facts
    
        - import_role:
            name: apidb_collect
          tags: collect

        - import_role:
            name: apidb_collect_net
          tags: collect_net          
    
    - name: Post to APIDB
      hosts: localhost
      connection: local
      gather_facts: false
      collections:
        - apidb.ansibledb_net
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

Set-up the devices

For networking device you need for example:
```
      ansible_connection: local
      ansible_network_os: panos  
```      
 
Intital run
-----------
Now you've setup ansibledb_net, run it to check everything is working and you have connectivity. In my exampe, I've added the inventory file to the ansible.cfg file. If you haven't, you'll need to include the inventory file in additon to the command below.

````
ansible-playbook  deploy.yml
````


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

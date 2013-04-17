Summary Report (All)
====================

- Period: %(tmpl_period)s
- Cloud(india.futuregrid.org): eucalyptus, openstack
- Cloud(sierra.futuregrid.org): eucalyptus, nimbus
- Cloud(hotel.futuregrid.org): nimbus
- Cloud(alamo.futuregrid.org): nimbus
- Cloud(foxtrot.futuregrid.org): nimbus
- Metrics: VMs count, Users count, Wall hours, Distribution by Wall Hours, Project, Project Leader, and Institution, and Systems

Wall Hours by Clusters (Total, monthly)
---------------------------------------

.. Summary chart for all services on all systesm

.. ================================================================================================================
.. 1) WALL HOURS image
.. ================================================================================================================
.. image:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-runtime-%(service)s--hostname.png
   :alt:  Wall Hours by Clusters
..   :align: left
| Figure 1. Wall Hours by Clusters
| This pie chart represents overall usage of Wall Hours.

- Period: %(tmpl_period)s                   
- Cloud:
   - india: Eucalyptus, Openstack
   - sierra: Eucalyptus, Nimbus
   - hotel: Nimbus
   - alamo: Nimbus
   - foxtrot: Nimbus
.. - Cloud(IaaS): %(all_services)s                               
.. - Hostname: %(all_hostnames)s                               

.. ================================================================================================================
.. 2) same chart but MONTHLY bar charts 
.. ================================================================================================================
.. image:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-runtime-%(service)s--monthlyhostname.png
   :alt: Wall Hours by Clusters (Monthly)
..   :align: left
| Figure 2. Wall Hours by Clusters (Monthly)
| This stacked column chart represents average monthly usage of Wall Hours.

- Period: %(tmpl_period)s                   
- Cloud:
   - india: Eucalyptus, Openstack
   - sierra: Eucalyptus, Nimbus
   - hotel: Nimbus
   - alamo: Nimbus
   - foxtrot: Nimbus
.. - Cloud(IaaS): %(all_services)s                               
.. - Hostname: %(all_hostnames)s                               

VM Count by Clusters (Total, monthly)
---------------------------------------

.. ================================================================================================================
.. 3) VM COUNT
.. ================================================================================================================
.. image:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-count-%(service)s--hostname.png
   :alt: Figure 3: VMs count by Clusters
..   :align: left
| Figure 3. VMs count by Clusters
| This pie chart represents overall count of launched VM instances during the period.

- Period: %(tmpl_period)s                   
- Cloud:
   - india: Eucalyptus, Openstack
   - sierra: Eucalyptus, Nimbus
   - hotel: Nimbus
   - alamo: Nimbus
   - foxtrot: Nimbus
.. - Cloud(IaaS): %(all_services)s                               
.. - Hostname: %(all_hostnames)s                               

.. ================================================================================================================
.. 4) VM COUNT (MONTHLY)
.. ================================================================================================================
.. image:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-count-%(service)s--monthlyhostname.png
   :alt: Figure 4: VMs count by Clusters (Monthly)
..   :align: left
| Figure 4. VMs count by Clusters (Monthly)
| This stacked column chart represents average counts of launched VM instances per month.

- Period: %(tmpl_period)s                   
- Cloud:
   - india: Eucalyptus, Openstack
   - sierra: Eucalyptus, Nimbus
   - hotel: Nimbus
   - alamo: Nimbus
   - foxtrot: Nimbus
.. - Cloud(IaaS): %(all_services)s                               
.. - Hostname: %(all_hostnames)s                               

Users Count by Clusters (Total, monthly)
----------------------------------------

.. ================================================================================================================
.. 5) USERS COUNT
.. ================================================================================================================
.. image:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-countusers-%(service)s--hostname.png
   :alt: Figure 5: Users count by Clusters
..   :align: left
| Figure 5. Users count by Clusters
| This pie chart represents total number of active users.

- Period: %(tmpl_period)s                   
- Cloud:
   - india: Eucalyptus, Openstack
   - sierra: Eucalyptus, Nimbus
   - hotel: Nimbus
   - alamo: Nimbus
   - foxtrot: Nimbus
.. - Cloud(IaaS): %(all_services)s                               
.. - Hostname: %(all_hostnames)s                               

.. ================================================================================================================
.. 6) USERS COUNT (MONTHLY)
.. ================================================================================================================
.. image:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-countusers-%(service)s--monthlyhostname.png
   :alt: Figure 6: Users count by Clusters (Monthly)
..   :align: left
| Figure 6. Users count by Clusters (Monthly)
| This stacked column chart represents average count of active users per month.

- Period: %(tmpl_period)s                   
- Cloud:
   - india: Eucalyptus, Openstack
   - sierra: Eucalyptus, Nimbus
   - hotel: Nimbus
   - alamo: Nimbus
   - foxtrot: Nimbus
.. - Cloud(IaaS): %(all_services)s                               
.. - Hostname: %(all_hostnames)s                               

.. Cloud vs HPC
.. -------------
.. .. image:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-runtime-hpccloud--hostname.png
.. .. image:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-count-hpccloud--hostname.png
.. .. image:: ../../images/%(output_directory)s/%(from_dateT)s-%(to_dateT)s-countusers-hpccloud--hostname.png

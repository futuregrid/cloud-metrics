Real-time monitoring for HPC in FutureGrid
------------------------------------------

Sample
------------
http://129.79.49.179:18080/list

Description
-----------

Notes for implementation
------------------------

First discussion
^^^^^^^^^^^^^^^^

We expect to have :

- Q1. how many users use queues now
- Q2. how many nodes are assigned overall to hpc
- Q3. how many nodes are used (in %) of those nodes that are assigned to HPC

How to implement?
^^^^^^^^^^^^^^^^^

Using Torque command tools, we can obtain resource utilization such as status of pbs batch jobs, state information and diagnostic output for a specified job.

Getting an active user list
"""""""""""""""""""""""""""
This is an approach to answer Q1.

1. ``qstat`` displays user name and queuing jobs.

  E.g.

        .. line-block::

        Job id                    Name             User            Time Use S Queue
        ------------------------- ---------------- --------------- -------- - -----
        397056.i136                STDIN            lihui                  0 Q batch          
        487315.i136                30_chol_pops_npt pela3247               0 H batch          
        553849.i136                twisterJob       yangruan        00:00:00 R delta-long``

2. We collect user name by selecting specific fields in ``qstat``. 
   ``R`` indicates Running jobs so we search ``S`` in ``qstat`` and get unique user names.
   
        ``qstat|grep " R "|awk '{ print $3}'|sort -u``
        
        E.g.

        ``feiteng
        jasonkwan
        pela3247
        xcguser
        yangruan``

Getting an active node list (or number of active nodes)
"""""""""""""""""""""""""""""""""""""""""""""""""""""""
This is an approach to answer Q2.

1. ``qstat -n`` displays a node list.

   E.g.

   .. line-block::

   553849.i136          yangruan delta-lo twisterJob        21110     8  96    --  168:0 R 20:41
   d002i/11+d002i/10+d002i/9+d002i/8+d002i/7+d002i/6+d002i/5+d002i/4+d002i/3
   +d002i/2+d002i/1+d002i/0+d005i/11+d005i/10+d005i/9+d005i/8+d005i/7+d005i/6
   +d005i/5+d005i/4+d005i/3+d005i/2+d005i/1+d005i/0+d006i/11+d006i/10+d006i/9
   +d006i/8+d006i/7+d006i/6+d006i/5+d006i/4+d006i/3+d006i/2+d006i/1+d006i/0
   +d007i/11+d007i/10+d007i/9+d007i/8+d007i/7+d007i/6+d007i/5+d007i/4+d007i/3
   +d007i/2+d007i/1+d007i/0+d008i/11+d008i/10+d008i/9+d008i/8+d008i/7+d008i/6
   +d008i/5+d008i/4+d008i/3+d008i/2+d008i/1+d008i/0+d010i/11+d010i/10+d010i/9
   +d010i/8+d010i/7+d010i/6+d010i/5+d010i/4+d010i/3+d010i/2+d010i/1+d010i/0
   +d011i/11+d011i/10+d011i/9+d011i/8+d011i/7+d011i/6+d011i/5+d011i/4+d011i/3
   +d011i/2+d011i/1+d011i/0+d012i/11+d012i/10+d012i/9+d012i/8+d012i/7+d012i/6
   +d012i/5+d012i/4+d012i/3+d012i/2+d012i/1+d012i/0``

2. The template looks like {node name with node number/number of cores+...}, so we parse them in such a way that following. 
   
   ``qstat -n|grep "/"|sed -e "s/+/\\n/g" -e "s/\s\+//g"|awk -F"/" '{ print $1}'|sort -u|wc``

   If we remove ``wc``, then we can get the list of active nodes.

Getting a utilization of nodes allocated to HPC
"""""""""""""""""""""""""""""""""""""""""""""""
This is an approach to answer Q3.

1. Based on the number of question 2 above, we will get the utilization.

   Total utilization = the number of active nodes / total nodes

2. We have fixed number of total nodes. For example, india has 496 cores including bravo, delta, xray.

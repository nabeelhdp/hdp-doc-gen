# hdp-doc-gen

Cluster documentation is generally an area that's not always given much attention in many corporate environments. Both generation of the cluster documentation and maintaining it as and when changes go in into the cluster configurations is takes a significant amount of time for the cluster administration teams. In most cases, logging in to Ambari is the most followed route for finding out certain FAQ.
<dl>
  <dt>Eg</dt>
  <dd><i>What's our HDFS blocksize?</i></dd>
<dd><i>What's our HDFS blocksize?</i></dd>
<dd><i>Is LLAP enabled in this cluster ?</i></dd>
<dd><i>What's the default replication for Kafka ?</i></dd>
</dl>
There could also be questions for developers to connect to the cluster -
<dl>
  <dt> </dt>
<dd><i>What's the NN URL ?</i></dd>
  <dd><i>What's the Hive JDBC URL ?</i></dd>
    </dl>
 And then there are questions like    
<dl>
  <dt> </dt>
<dd><i>Which nodes do we have these components installed ?</i></dd>
  <dd><i>What components are installed on this particular node ?</i></dd>
    </dl>
    
This project is an attempt to crack this problem using automation of generating the pages with the information available via Ambari REST API and other REST APIs in the cluster components. 

The nested JSON structures emitted by Ambari REST responses are parsed and condensed into HTML output with only the most needed configurations displayed in the output.

The result is an HTML document that can be inserted into Confluence pages. At a later stage, I plan to add direct publishing of contents to Confluence via it's REST APIs. There's some fancy graph representations doable for host component representation as a graph somewhere along the lines of https://martin.atlassian.net/wiki/spaces/lestermartin/pages/1019871233/Hadoop+Component+Dependency+Graph

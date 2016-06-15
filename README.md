# LetterSiteV1

This is an attempt to make a network-graph interface for the [Letters of 1916](http://letters1916.ie) project.

The idea is to combine eXist-DB for storage, querying and transformation of TEI-XML documents, the neo4j graph database (of which I currently know very little) as a graph representation for querying relations (which would be painful in XQuery), some client-side graph library (probably Sigma.js), and stitch it all together with the Python Flask library and some client-side javascript.

This is probably a bad idea.
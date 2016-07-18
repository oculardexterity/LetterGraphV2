# LetterSiteV2

This is an attempt to make a network-graph interface for the [Letters of 1916](http://letters1916.ie) project.

The application uses eXist-DB for storing TEI-XML files, the Python graph-tool library for server-side graph manipulation and layout, <del>Flask</del> Tornado as a web framework*, a slightly modified Sigma.js graph interface and tons of oddball JavaScript to tie it all together. This is version two!

This is probably a bad idea.



*needed to run the graph layout algorithm in some multi-process, asynchronous fashion reliably. Flask was rubbish at this.
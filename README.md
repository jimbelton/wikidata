# wikidata
Tools for working with wikidata (structured data from wikipedia)

## wd-extract.py

Extract data from a JSON dump of wikidata.org

Usage: `wd-extract.py [-cfnr] [-l lc] [-p lc] [-s pat] [-t type] [-w]` *wd-dump-json*

| Option | Long Option | Description |
| --- | --- | --- |
| -c | --claims        | Don't simplify claims. By default, the complex structure will be simplified. |
| -f | --failonerror  | If present, exit if an error occurs. |
| -l | --language *lc*   | Use language *lc* for all string members, falling back to **en** if needed, falling back to a random language if needed. The member name will also be depluralized (e.g. "labels" to "label"). If not specified, the multilingual string tables will be left unmodified. |
| -n | --names         | Print labels only instead of dumping objects in JSON |
| -p | --properties *lc* | Replace property ids with labels in language *lc*, falling back to **en** or a random language if needed. If not already present, a file named ########-properties.json will be generated, containing a map of property ids to labels. |
| -s | --sitelinks *pat* | Pattern for sitelinks to include or "" to exclude all sitelinks. Sitelinks are links to other websites. |
| -t | --type *type*     | Type of object to extract (property|item). Default=all |
| -r | --references    | Don't remove references. References are links to sources of information. |
| -w | --warning       | Print warnings. |

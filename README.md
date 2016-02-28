# wikidata
Tools for working with wikidata (structured data from wikipedia)

## data/YYYYMMDD-properties.json
These files are maps from property identifiers to (usually) english language labels. You can generate indeces and extracted data with whichever language you choose. For an example index, see [data/20160215-properties.json](https://github.com/jimbelton/wikidata/blob/master/data/20160215-properties.json)

## wd-extract.py

Extract data from a JSON dump of wikidata.org. Currently, extracting only English strings (-l en) and stripping all sitelinks reduces the size of the JSON by roughly 10 times.

Usage: `wd-extract.py [-cCfnr] [-l lc] [-p lc] [-s pat] [-t type] [-w]` *wd-dump-json*

| Option | Long Option | Description |
| --- | --- | --- |
| -C | --claims        | Don't simplify claims. By default, the complex structure will be simplified. |
| -c | --classes       | TBD: Create a class map and dump it in JSON format. |
| -f | --failonerror  | If present, exit if an error occurs. |
| -l | --language *lc*   | Use language *lc* for all string members, falling back to **en** if needed, falling back to a random language if needed. The member name will also be depluralized (e.g. "labels" to "label"). If not specified, the multilingual string tables will be left unmodified. |
| -n | --names         | Print labels only instead of dumping objects in JSON. Uses language, or **en** if none specified. |
| -p | --properties *lc* | Replace property ids with labels in language *lc*, falling back to **en** or a random language if needed. If not already present, a file named ########-properties.json will be generated, containing a map of property ids to labels. |
| -s | --sitelinks *pat* | Pattern for sitelinks to include or "" to exclude all sitelinks. Sitelinks are links to other websites. |
| -t | --type *type*     | Type of object to extract (property\|item). Default=all |
| -R | --references    | TBD: Don't remove references. References are links to sources of information. |
| -w | --warning       | Print warnings. |

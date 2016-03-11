# wikidata
Tools for working with wikidata (structured data from wikipedia)

## data/YYYYMMDD-properties.json
These files are maps from property identifiers to (usually) english language labels. You can generate property maps and extracted data with whichever language you choose. For an example index, see [data/20160215-properties.json](https://github.com/jimbelton/wikidata/blob/master/data/20160215-properties.json)

## wd-extract.py

Extract data from a JSON dump of wikidata.org. Currently, extracting only English strings (-l en) and stripping all sitelinks reduces the size of the JSON by roughly 10 times.

Usage: `wd-extract.py [-c|-C] [-DfnR] [-i file] [-l lc] [-o file] [-p lc] [-s pat] [-t type] [-w]` *wd-dump-json*

| Option | Long Option | Description |
| --- | --- | --- |
| -C | --claims        | Don't simplify claims. By default, the complex structure will be simplified. |
| -c | --classes       | Create a class hierarchy and dump it in JSON format. |
| -D | --datatypes    | Don't simplify datatypes. e.g. string values will remain wrapped in JSON objects |
| -f | --failonerror  | If present, exit if an error occurs. |
| -i | --index file    | Output an index to a file. This can be used to quickly read an item out of the extracted data.  |
| -l | --language *lc*   | Use language *lc* for all string members, falling back to **en** if needed, falling back to a random language if needed. The member name will also be depluralized (e.g. "labels" to "label"). If not specified, the multilingual string tables will be left unmodified. |
| -n | --names         | Print labels only instead of dumping objects in JSON. Uses language, or **en** if none specified. |
| -o | --output file    | Output the extracted data or list to a file. Default=stdout |
| -p | --properties *lc* | Replace property ids with labels in language *lc*, falling back to **en** or a random language if needed. If not already present, a file named ########-properties.json will be generated, containing a map of property ids to labels. |
| -s | --sitelinks *pat* | Pattern for sitelinks to include or "" to exclude all sitelinks. Sitelinks are links to other websites. |
| -t | --type *type*     | Type of object to extract (property\|item). Default=all |
| -R | --references    | TBD: Don't remove references. References are links to sources of information. |
| -w | --warning       | Print warnings. |

### Examples
To generate a sorted list of all of the books (id=Q571) in wikidata (72432 as of 2016-02-15), run the following command:
```
./wd-extract.py -n -l en -p en -s "" -t Q571 data/20160215.json | sort -d
```

## wd-diagram.py

Generates a class diagram from extracted classes

Usage: `wd-diagram.py [-dfw] [-l n] *wd-classes-json*

| Option | Long Option | Description |
| --- | --- | --- |
| -d | --dot         | Output the diagram in dot format (default=ascii) |
| -f | --failonerror | If present, exit if an error occurs |
| -l | --levels n    | Show only the first n levels of classes below the root in the hierarchy (default=unlimited)
| -w | --warning     | Print warnings |

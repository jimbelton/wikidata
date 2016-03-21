# wikidata
Tools for working with wikidata (structured data from wikipedia)

## data/YYYYMMDD-properties.json
These files are maps from property identifiers to (usually) english language labels. You can generate property maps and extracted data with whichever language you choose. For an example index, see [data/20160215-properties.json](https://github.com/jimbelton/wikidata/blob/master/data/20160215-properties.json)

## wd-extract.py

Extract items from a JSON dump of wikidata.org. Currently, extracting only English strings (-l en) and stripping all sitelinks reduces the size of the JSON by roughly 10 times.

Usage: `wd-extract.py [-c|-C] [-DfFnR] [-i file] [-I labels] [-l lc] [-o file] [-p lc] [-s pat] [-t type] [-w]` *wd-dump-json*

| Option | Long Option | Description |
| --- | --- | --- |
| -C | --claims        | Don't simplify claims. By default, the complex structure will be simplified. |
| -c | --classes       | Create a class hierarchy and dump it in JSON format. |
| -D | --datatypes    | Don't simplify datatypes. e.g. string values will remain wrapped in JSON objects |
| -f | --failonerror  | If present, exit if an error occurs. |
| -F | --format  | Format the extracted data readably; this is mainly useful for testing |
| -i | --index file    | Output an index to a file. This can be used to quickly read an item out of the extracted data; you must specify a type with -t  |
| -I | --include labels | Don't remove the properties in the quoted comma separated list of labels (see the list below for properties that would normally be removed) |
| -l | --language *lc*   | Use language *lc* for all string members, falling back to **en** if needed, falling back to a random language if needed. The member name will also be depluralized (e.g. "labels" to "label"). If not specified, the multilingual string tables will be left unmodified. |
| -n | --names         | Print labels only instead of dumping objects in JSON. Uses language, or **en** if none specified. |
| -o | --output file    | Output the extracted data or list to a file. Default=stdout |
| -p | --properties *lc* | Replace property ids with labels in language *lc*, falling back to **en** or a random language if needed. If not already present, a file named ########-properties.json will be generated, containing a map of property ids to labels. |
| -s | --sitelinks *pat* | Pattern for sitelinks to include or "" to exclude all sitelinks. Sitelinks are links to other websites. |
| -t | --type *type*     | Type of object to extract (property\|item\|Q#). Default=all. If specified, the type member will be removed from all extracted objects. |
| -R | --references    | TBD: Don't remove references. References are links to sources of information. |
| -w | --warning       | Print warnings. |

### Examples
To generate a sorted list of all of the books (id=Q571) in wikidata (72432 as of 2016-02-15), run the following command:
```
./wd-extract.py -n -l en -p en -s "" -t Q571 data/20160215.json | sort -d
```

### Ignored Properties
The following properties will be removed unless explicitly included with the **-I** option:

| Property Label | Description |
| --- | --- |
| BNCF Thesaurus                        | Florentine national central library                              |
| BnF identifier                        | French national library                                         |
| Commons category                      | Wikimedia Commons                                               |
| Commons gallery                       | Wikimedia Commons |
| Freebase identifier                   | Defunct structured data source, purchased and closed by Google |
| GND identifier                        | German universal authority file |
| IMDb identifier                       | Internet movie database |
| ISFDB title ID                        | Internet speculative fiction database |
| KINENOTE film ID                      | Japanese KINENOTE movie database |
| LCAuth identifier                     | US libary of congress |
| Library of Congress Classification    | US libary of congress |
| LibraryThing work identifier          | LibraryThing |
| MusicBrainz artist ID                 | MusicBrainz |
| MusicBrainz release group ID          | MusicBrainz |
| MusicBrainz work ID                   | MusicBrainz |
| NDL identifier                        | Japan national diet library |
| NLA (Australia) identifier            | Australian national library |
| OCLC control number                   | WorldCat |
| Open Library identifier               | openlibrary.org |
| PSH ID                                | Czech technical library |
| Regensburg Classification             | German university of Regensburg library |
| SUDOC authorities                     | French university libraries |
| VIAF identifier                       | Virtual international authority file |

## wd-diagram.py

Generates a class diagram from extracted classes

Usage: `wd-diagram.py [-dfw] [-l n]` *wd-classes-json*

| Option | Long Option | Description |
| --- | --- | --- |
| -d | --dot         | Output the diagram in dot format (default=ascii) |
| -f | --failonerror | If present, exit if an error occurs |
| -l | --levels n    | Show only the first n levels of classes below the root in the hierarchy (default=unlimited)
| -w | --warning     | Print warnings |

## wd-package

Generate a package of data from data extracted from a wikidata dump

Usage: `wd-package.py` *class* *data-file* *index*

Currently, *class* can be the item identifier of a class to package, or it can be `books`, which will extract all objects related to books. This script is a work in progress.

## wd-lookup.py

Looks up a key (an item identifier number without the leading **Q**) in the data extracted from a wikidata dump. This script can be used to test the **Index** class.

Usage: `wd-lookup` *key* *data-file* *index-file*

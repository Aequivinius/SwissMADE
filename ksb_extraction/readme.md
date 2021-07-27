# KSB data conversion

* Installed Postgres and pgAdmin 4, in pgAdmin created a database called `database` and ran `psql -d test_db.db -U postgres -f data/tester.sql` to load the dump into the database (`tester.sql` is a version of `dump...sql` with some lines commented out).
* in pgAdmin, then exported table `bericht` in `database` (set delimiter to tab, quote to \', including header)

![Capture d’écran 2021-06-01 à 14.08.02](img/export.png)

* The resulting file has 113771 rows (= number of articles).
* Using `extract.ipynb` the rows are converted as follows: The JSON is *flattened*, that means the nested example (1) is transformed to (2):

```json
# unflattened JSON (1)
{ "Bericht": 
   { "Befunde": 
      { "HatInhalt" : "1" ,
        "Inhalt" : "Labor: Siehe ..."
      }
   }
}
```

```json
# flattened JSON (2)
{ "Bericht_Befunde_HatInhalt" : "Diagnosen" ,
  "Berichte_Befunde_Inhalt" : "Labor: Siehe ..." 
}
```

* Then *all* item titles (such as `Bericht_Verlauf_Titel`) are aggregated, yielding 7285 possible fields. From this, a CSV is generated, encoded in UTF-8, delimited by `,` and values quoted with `"`, with all 7285 item titles as header, and filling in in every row the corresponding values from the report. Naturally, some rows don't have values for all the headers, so there are lots of empty fields.
* Additionally, every report is exported as a plain text file, with the `reportnr_ano` field from the database serving as file name, in which the item title is followed by its value. 

## A note on encoding

As GATE opens documents in the operating system's default encoding, which under windows is `ISO-8859-9` ([Link](https://gate.ac.uk/sale/tao/splitch3.html#sec:developer:unicode)), it is important to *explicitly* open the files with `UFT-8` encoding as shown in the picture below:

![encoding](img/encoding.png)


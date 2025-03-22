# SMT IV Table Editor

This is a table editor for SMT IV and SMT IV Apocalypse. It works by
splitting each the table file (*.tbb) into a spreadsheet (.xlsx) with
each sheet corresponding to a table from the file. Data can be edited
in the spreadsheets and packaged back into table files for modding
purposes.

Note that this was developed and tested only on Linux. If it doesn't
work on other OS please report the issue.

### Unpacking the tables

To unpack the tables, run the following command:

```
python unpack.py /path/to/romfs/<TITLE_ID>/...
```

This will unpack all table files into a directory titled
`spreadsheets`. The above command will also work for any combination
of subdirectories and .tbb files. I recommend unpacking all tables
initially.

NB: The path MUST have the game's title ID in it. That is how the
library distinguishes the games from each other.

While all tables should get unpacked properly, any file that fails
should get listed in a `failed.txt` file.

### Packing the tables

To pack the tables, run the following command:

```
python pack.py /path/to/romfs/<TITLE_ID>/...
```

The path argument(s) should be the same paths/files used for unpacking
(i.e. tbb files and/or directories containing those files). This will
load the tbb files, along with their corresponding spreadsheets, and
dump any modified tables in a `mods` directory.

Mods should be ready to go, but it is the user's responsibility to
confirm this for themselves.

### Testing

A good test run is to unpack and then pack all tables back to back.
If all goes well, all the spreadsheets should get built, and no modded
files should get written.

## Spreadsheet Editing

### Editing data

Data can be edited as you would with any other spreadsheet. Some
guidelines to follow:

- Do not edit sheet names in the spreadsheet.

- Do not add or delete any columns.

- You can add or delete data rows in some cases (e.g. shop
  inventory). There is no need to update the addresses and row numbers
  in columns A and B if you do this.

- Be careful editing strings. I recommend sticking with Roman
  lettering to avoid any encoding issues. The table files never
  specify string length, so I can only guess how many bytes the game
  actually reads. A good rule of thumb here is not to exceed the
  length of the longest string in the column. If you must exceed it,
  make sure to test it in game.

#### Notes

- battle/NKMBaseTable:

  - Affinities: Setting affinities requires setting both a weakness
    percentage multiplier and some flags. Their pairings are labelled
    "Phys/Gun/Elem, Aff" in the spreadsheet.  Values to use when
    editing are shown in the table below. Ailments follow a similar
    pattern, but there are slight differences I have yet to test.

    | Weakness | Resistance | Null | Repel | Drain |
    :---------:|:----------:|:----:|:-----:|:------:
    | 125, 8   | 50, 20 | 100, 4 | 100,12 | 100,16 |

- skill names: To my knowledge these aren't in any files in the romfs,
  so I added some lists of them in the `skills` directory.

### Column formatting

To edit columns of spreadsheets built, you can edit the corresponding
json file in the `format` directory. This allows for naming the sheet
in the spreadsheet and specifying titles and types for data
columns. Allowed types are signed and unsigned integers of sizes 8,
16, 32, and 64 (e.g. `uint8`, `int32`), and also `float`. Strings can
vary in length and are expected to be of the form `string_N` where `N`
is the number of bytes (e.g. `string_16` or `string_0x10`). See the
`item/ItemTable` files for simple examples.

I have no plans on extensively figuring out all the correct column
types and adding headers. Anyone else interested in doing this is
welcome to contribute with pull requests. My only guideline to follow
is that I want column titles to be short rather than descriptive
(e.g. see `battle/NKMBaseTable` with headers "Aff" for "Affinity"
rather than "Resistance/Weakeness/Drain/Reflect/Null").

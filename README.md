# CombosStat: A utility tool designed to compute shared data statistics for given combinations of data samples

## Installation
```bash
python3 -m pip install combos_stat
```

## Usage
```bash
combos_stat -h
```

### *`1. stat`*
```
Usage: python -m combos_stat.bin.main stat [OPTIONS]

  Calculate statistics for shared data counts based on combinations of samples.

Options:
  -i, --input-file PATH           Path to the input data file  [required]
  -o, --output-file PATH          Path where the results will be saved  [default: output_stat.txt]
  -n, --num-samples INTEGER       Number of samples to compute  [required]
  -t, --share_type [intersection|union]
                                  Type of share to compute
  --header INTEGER                Row number to use as the column names  [default: 0]
  --sep TEXT                      Delimiter to use for reading the input file (e.g., "\t" for tab)
  --start-col INTEGER             Column index to start reading sample data from  [default: 1]
  --show-progress BOOLEAN         Show progress
  --chunksize INTEGER             The chunksize lines to read
  --chunk INTEGER                 The index of chunk
  -h, -?, --help                  Show this message and exit.


examples:
    combos_stat stat -h
    combos_stat stat -i input.txt -o output.txt -n 13 -t intersection
    combos_stat stat -i input.txt -o output.txt -n 13 -t intersection --chunksize 100 --chunk 2 [read 101-200 lines]
```

### *`2. plot`*
```bash
Usage: python -m combos_stat.bin.main plot [OPTIONS] RESULT_DIR

  Generate Boxplot with statistics results

Options:
  -R, --Rscript TEXT  Path to the executable Rscript  [default: Rscript]
  -w, --write TEXT    Write the R code to a file
  --option TEXT       Options in the format key=value for boxplot, eg. title="Demo Stats", x_lab="Shared_Numbers",
                      y_lab="Data"
  -h, -?, --help      Show this message and exit.

  

examples:
    combos_stat plot -h
    combos_stat plot out/result
    combos_stat plot out/result --write boxplot.R
    combos_stat plot out/result --write boxplot.R --option x_lab=XXX --option width=30 --option dpi=500
                          
default options:
    infile = 'processed_stats.tsv'
    output = 'boxplot'
    x_lab = 'Genomes'
    y_lab = 'Families'
    title = 'BoxPlot'
    legend_title = 'Type'
    dpi = 300
    width = 14
    height = 7
```


### *`3. batch`*
```bash
Usage: python -m combos_stat.bin.main batch [OPTIONS]

  Generate batch shells and SJM job

Options:
  -i, --input-file PATH    Path to the input data file
  -sep, --sep TEXT         Delimiter to use for reading the input file (e.g., "\t" for tab)
  -s, --start-col INTEGER  Column index to start reading sample data from  [default: 1]
  -t, --threshold INTEGER  The threshold to divide the combinations  [default: 200000]
  -O, --output-dir PATH    Path to the output directory  [default: .]
  --job TEXT               Generate SJM Job
  --no-check               Do not check queues for SJM
  -h, -?, --help           Show this message and exit.


examples:
    combos_stat batch -h
    combos_stat batch -i input.txt -t 200000 -O out
    combos_stat batch -i input.txt -t 200000 --job run.job
```

## Result
***prefix***
- x: intersection
- y: union

`shell directory`
```
shell/
├── plot.sh
├── x2
│   └──stat.x2_1.sh
├── y2
│   └──stat.y2_1.sh
...
├── x14
│   ├── stat.x14_1.sh
│   ├── stat.x14_2.sh
│   ├── ...
│   └── stat.x14_100.sh
...
└── y29
    └──stat.y29_1.sh
```

`result directory`
```
result/
├── x2
│   └──x2_1.txt
├── y2
│   └──y2_1.txt
...
├── x14
│   ├── x14_1.txt
│   ├── x14_2.txt
│   ├── ...
│   └── x14_100.txt
...
└── y29
    └──y29_1.txt
```
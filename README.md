# `show-me`

This is a simple tool to show you history of your Github contributions.

```
$ show-me
 Repo                                  |   ★ |   Total |   Pulls |   Issues |   Commits |   Reviews
---------------------------------------+-----+---------+---------+----------+-----------+-----------
 packit-service/packit                 |  20 |     421 |      47 |       58 |       258 |        58
 ansible-community/ansible-bender      | 105 |     177 |      20 |       33 |       123 |         1
 user-cont/release-bot                 |  36 |      76 |       6 |       21 |        28 |        21
 packit-service/ogr                    |   5 |      68 |      10 |        9 |        32 |        17
 user-cont/colin                       |  30 |      41 |       2 |        1 |        29 |         9
 user-cont/conu                        | 141 |      39 |       3 |        3 |        21 |        12
 TomasTomecek/speaks                   |   2 |      26 |       0 |        1 |        25 |         0
 TomasTomecek/dotfiles                 |   3 |      24 |       0 |        0 |        24 |         0
 packit-service/upsint                 |   1 |      17 |       2 |        6 |         8 |         1
 TomasTomecek/sen                      | 760 |      12 |       1 |        1 |         9 |         1
 TomasTomecek/ansible-role-release-bot |   0 |      11 |       0 |        0 |        11 |         0
 TomasTomecek/pretty-git-prompt        |  33 |       9 |       1 |        1 |         7 |         0
 rebase-helper/rebase-helper           |  30 |       8 |       1 |        5 |         0 |         2
 TomasTomecek/mysterious-keybinds      |   0 |       8 |       0 |        0 |         8 |         0
 prgcont/workshop-ansible-containers   |   4 |       7 |       1 |        0 |         6 |         0
```

Legend (columns in order):
* Name of the Github repository.
* Current star count.
* Total number of contributions (sum of pull requests, issues, commits and reviews).
* A Count of pull requests created by you.
* How many issues you've created.
* Total count of commits you submitted to the repository.
* A number of reviews you performed.


## Requirements

* Python 3.6+
* Github API token: you can get it in your [settings
  page](https://github.com/settings/tokens).
  * Pass it to show-me via environment variable `GITHUB_TOKEN`.


## Installation

```
$ pip3 install --user show-me
```

Feel free to install directly from Github:
```
$ pip3 install --user git+https://github.com/TomasTomecek/show-me
```


## Usage

```
$ GITHUB_TOKEN=my-token show-me
```

You can configure show-me via CLI options:
```
Usage: show-me [OPTIONS]

  Show me my Github contributions!

Options:
  -n, --lines INTEGER     Print first N lines.  [default: 15]
  --cache-file-path PATH  Path to the cache file.  [default:
                          /home/tt/.cache/show-me.json]
  --load-from-cache       Don't query Github and load from cache.
  --save-to-cache         Query Github and save response to a file (to save
                          time and bandwidth).
  --debug                 Show debug logs.
  --start-year INTEGER    Start counting the contributions in the selected
                          year.  [default: 2019]
  -h, --help              Show this message and exit.
```


Have fun!

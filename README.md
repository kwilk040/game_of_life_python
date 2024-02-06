# Game of life python

## Requirements

+ python3.12
+ make

To set up the environment run:

```shell
make install &&
source .venv/bin/activate
```

## Running the application

To start the application run:

```shell
make run
```

To start the application with custom ruleset:

```shell
python src/game.py -r [RULESET]
```

For example:

```shell
python src/game.py -r B2/S23
```

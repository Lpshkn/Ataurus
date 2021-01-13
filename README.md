# ATAURUS (Attribution of Authorship Russian)

The program for recognizing the author of russian texts or articles.

## Features extraction

The list of features that will be used in this program: [FEATURES.md](doc/FEATURES.md)

## Quick start

Clone the repository:
```shell script
git clone https://github.com/Lpshkn/Ataurus.git ataurus
cd ataurus
```

At first, you have to create the Docker image:
```shell script
sudo docker build -t ataurus .
```

There are 3 main commands for working with the program: `train`, `predict` and `info`:
* `train` - training a model on the input data. While training extracted features from texts serialize to 
`.config` directory. The trained model will be serialized into the same directory (if `-o` option didn't specify).

* `predict` - predicting target classes for the input data. If the input file was processed earlier (and saved in 
`.config` directory), it will be retrieved from the cache.

* `info` - getting information about the model, containing in the `.config` directory.

### Training

```shell script
sudo docker run \
-v <path to a directory>/data:/ataurus/data \
-v <path to a directory>/.config:/ataurus/.config \
ataurus train ./data/train2.csv
```
or
```shell script
sudo docker run \
-v $PWD/data:/ataurus/data \
-v $PWD/.config:/ataurus/.config \
ataurus train ./data/train2.csv
```

### Getting information

```shell script
sudo docker run -v <path to a directory>/.config:/ataurus/.config ataurus info
```
or
```shell script
sudo docker run -v $PWD/.config:/ataurus/.config ataurus info
```

### Predicting

```shell script
sudo docker run \
-v <path to a directory>/data:/ataurus/data \
-v <path to a directory>/.config:/ataurus/.config \
ataurus predict ./data/test2.csv
```
or
```shell script
sudo docker run \
-v $PWD/data:/ataurus/data \
-v $PWD/.config:/ataurus/.config \
ataurus predict ./data/test2.csv
```

## Testing

To run tests:

```shell script
nosetests --with-coverage --cover-package=ataurus
```
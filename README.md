# Landlab grain type component executor

## Install dependencies

``` 
pip install -r requirements.txt
``` 

## Params
List of parameters for experiment.

```
  -h, --help            show this help message and exit
    
  -i INPUT, --input INPUT
                        Path to model grid in ASC format.
  -n NAME, --name NAME  Experiment title
  -c CHECKPOINT, --checkpoint CHECKPOINT
                        Number of step for checkpoints
  -e EXECUTIONS, --executions EXECUTIONS
                        Number of steps for experiment
```

## Experiment images
There are some asc images used by this project in /image folder

## Run
```
python main.py -i [INPUT] -n [NAME] -c [CHECKPOINT] -e [EXECUTIONS]
```

## Results
The run command will save a folder in /output with a subfolder contains 
the terrain, drainage area, shear stress and  grain type image result
and the models grid ASCs. 
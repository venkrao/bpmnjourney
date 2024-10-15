This git repository contains the artifacts used in substack - https://bpmjourney.substack.com/

I used a locally running Camunda installation - so all examples in this repo are tested only against that.

# Installation

## Camunda
For Camunda 8.x installation instructions - See https://github.com/camunda/camunda-platform

## Camunda Modeler
See https://camunda.com/download/modeler/

## This repo
To run the code in this repo, install dependencies from requirements.txt

```
python -m venv venv
source ./venv/bin/activate

pip install -r requirements.txt
```

# Example BPMN Models and Related Automation

BPMN Models in this repo are compatible with Camunda 8 Platform. When using Camunda Modeler, make sure you choose Camunda 8!

To deploy a BPMN model, simply locate the .bpmn file, load it in Camunda Modeler. To run the model, use the "play" button at the bottom left corner of Camunda Modeler. **Be sure to pass appropriate variables in json format**.

For this to work, you must have Camunda running locally.

## Example: Washsuperwell Limited

It's fully functioning model for handling a washing machine repair request used by a hypothetical company Washsuperwell Limited.

See `src/washsupewell_limited`.

```
.
├── customer_response_paid_service.py       -> 3. Run this to mimic the behavior of a customer replying, accepting or denying paid service.
├── Washsuperwell-Limited.bpmn              -> 1. Load this in Camunda Modeler
└── worker.py                               -> 2. Run this so that the worker can listen and act on service tasks.

```
- Starting the model in Camunda Modeler should accompany some variables in json format: 

    - Use `{"warranty_number": "WARR-111"}` to traverse the "warranty->Yes" path.
    - Use `{"warranty_number": "WARR-000"}` to traverse the "warranty->No" path.

- In warranty -> No path, the execution stops at "Read Response"!
    - To continue, you've to mimic a customer reply.
    - To do that, run: `python ./customer_response_paid_service.py WARR-000 True`



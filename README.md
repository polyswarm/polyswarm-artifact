# PolySwarm Artifact

[![pipeline status](https://gitlab.polyswarm.io/externalci/polyswarm-artifact/badges/master/pipeline.svg)](https://gitlab.polyswarm.io/externalci/polyswarm-artifact/commits/master)
[![coverage report](https://gitlab.polyswarm.io/externalci/polyswarm-artifact/badges/master/coverage.svg)](https://gitlab.polyswarm.io/externalci/polyswarm-artifact/commits/master)

Python package for mapping artifact types to the ArtifactType enum in the BountyRegistry contract.

Supports python3 >=3.5.2 and >=3.6.5.

# Versions in this schema

Everything in here is meant to be a part of an evolving schema. 
No versions, but all changes are additions only. 

## Use non-null and required carefully

Since we cannot remove fields, when a field is no longer useful, it needs to be nullable.
Unfortunately we cannot add nullable at a later date, as that would invalidate new schemas when being read by an old  

We can easily remove required fields, but we cannot add more. 
Doing so would invalidated old schemas.  

## Schema object

Schema objects possess the following methods and attributes:

``dict()``
    returns a dictionary of the model's fields and values
``json()``
    returns a JSON string representation dict()
``copy()``
    returns a deep copy of the model
``parse_obj()``
    a utility for loading any object into a model with error handling if the object is not a dictionary
``parse_raw()``
    a utility for loading strings of numerous formats
``parse_file()``
    like parse_raw() but for files
``from_orm()``
    loads data into a model from an arbitrary class
``schema()``
    returns a dictionary representing the model as JSON Schema
``schema_json()``
    returns a JSON string representation of schema()
``construct()``
    a class method for creating models without running validation
``__fields_set__``
    Set of names of fields which were set when the model instance was initialised
``__fields__``
    a dictionary of the model's fields
``__config__``
    the configuration class for the model


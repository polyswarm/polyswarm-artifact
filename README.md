# PolySwarm Artifact

[![pipeline status](https://gitlab.polyswarm.io/externalci/polyswarm-artifact/badges/master/pipeline.svg)](https://gitlab.polyswarm.io/externalci/polyswarm-artifact/commits/master)
[![coverage report](https://gitlab.polyswarm.io/externalci/polyswarm-artifact/badges/master/coverage.svg)](https://gitlab.polyswarm.io/externalci/polyswarm-artifact/commits/master)

Python package for mapping artifact types to the ArtifactType enum in the BountyRegistry contract.

# Versions in this schema

Everything in here is meant to be a part of an evolving schema. 
No versions, but all changes are additions only. 

## Use non-null and required carefully

Since we cannot remove fields, when a field is no longer useful, it needs to be nullable.
Unfortunately we cannot add nullable at a later date, as that would invalidate new schemas when being read by an old  

We can easily remove required fields, but we cannot add more. 
Doing so would invalidated old schemas.  

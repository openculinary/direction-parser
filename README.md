# RecipeRadar Direction Parser

A `direction` is a description of a step performed during preparation of a recipe.  The RecipeRadar Direction Parser takes a set of these directions as input, and extracts metadata from them before returning the results to caller.

For example, given the direction: `Place the casserole dish in the oven`, the `direction-parser` service can indicate that the direction references an `oven` appliance.

This functionality is provided to the [crawler](../crawler) service so that it can extract additional data from each recipe crawled.

## Install dependencies

Make sure to follow the RecipeRadar [infrastructure](../infrastructure) setup to ensure all cluster dependencies are available in your environment.

## Development

To install development tools and run linting and tests locally, execute the following commands:

```
pipenv install --dev
pipenv run make
```

## Local Deployment

To deploy the service to the local infrastructure environment, execute the following commands:

```
sudo sh -x ./build.sh
sh -x ./deploy.sh
```

## Operations

### Equipment list updates

Lists of kitchen equipment (e.g. slow cooker, whisk, ...) are stored in static text files which are deployed as part of the service and are loaded during application start-up.

To edit these equipment lists, look under the [data](web/data) directory in this repository.

# Heritage Science Schema Repository

This repository has been created to host completed heritage science metadata gathering json schema. Work and discussion relating to the development of these schema is being carried out within: [https://github.com/E-RIHS/hs-interoperability](https://github.com/E-RIHS/hs-interoperability)

For each type of schema, such as **Project**, create a section in this README file, as shown for **Project** to provide direct links to the current and developmental versions of each scheme along with a table of recent updates and changes.

Schema documents should be named using lowercase letters, according to the following naming structure: **name-v0.0.schema.json**. Changes to the first version number are reserverd for major changes that might include breaking changes, the second version number should be used for more minor changes including.

Note: Versions below 1.0 should be used for the intial development of each schema and therefore all versions changes, below 1.0, can include breaking changes even though the first part of the version number stays at 0. These early versions predate the choice for Cordra as the [central metadata store](https://data.e-rihs.io) for E-RIHS and are not available within this system. Because of this, these schema have been moved to the ['draft'](https://github.com/E-RIHS/schema/draft) subfolder in GitHub.

GitHub pages have been set up based on the root directory of this repository, this provides a much cleaner URL, but there can be a temporary lag between when new files are added and when the links will work. However, once the files have been added in there is no additional delay.
* [https://e-rihs.io/schema/service-v1.0.schema.json](https://e-rihs.io/schema/service-v1.0.schema.json)

Issues and ideas related to the schema published here can be added directly into the [Issues System](https://github.com/E-RIHS/schema/issues).

The schema GitHub repository can be access directly [here](https://github.com/E-RIHS/schema/). Additional modeling work and discussions relating to interoprability can be found [here](https://github.com/E-RIHS/hs-interoperability/).

## Schema overview

### [`Equipment`](https://e-rihs.io/schema/equipment) metadata schema

This schema is intended to model the metadata and details required to document and describe **equipments (tools)** used within an offered service in E-RIHS and IPERION-HS.

Current version: v1.0 [[JSON]](https://e-rihs.io/schema/equipment-v1.0.schema.json) [[Cordra]](#) [[Github]](https://github.com/E-RIHS/schema/blob/main/equipment-v1.0.schema.json)

### `KPI` metadata schema

This schema is intended to model the metadata and details required to document particular key performance indicators (KPIs) as defined by E-RIHS, capturing actual data.

Current version:

* Schema: [https://e-rihs.io/schema/kpi-v1.0.schema.json(https://e-rihs.io/schema/kpi-v1.0.schema.json)]
* Version: v1.0 (currently as a **living draft**)
* Links: [Cordra](#), [Github](https://github.com/E-RIHS/schema/blob/main/kpi-v1.0.schema.json)
* Related model: KPI model (unavailable)

### `KPI definition` metadata schema

This schema describes KPI definitions, which are used as a basis to calculate individual KPI scores.

Current version:

* Schema: [https://e-rihs.io/schema/kpi_definition-v1.0.schema.json](https://e-rihs.io/schema/kpi_definition-v1.0.schema.json)
* Version: v1.0 (currently as a **living draft**)
* Links: [Cordra](#), [Github](https://github.com/E-RIHS/schema/blob/main/kpi_definition-v1.0.schema.json)
* Related model: KPI model (unavailable)

### `Method metadata` schema

This new model has been created as a template for a range of **method** or setup descriptions - it allows for methods based on a series of statements and or a selection of the defined method parameters.

Current version:

* Schema: [https://e-rihs.io/schema/method-v1.0.schema.json](https://e-rihs.io/schema/method-v1.0.schema.json)
* Version: v1.0 (currently as a **living draft**)
* Links: [Cordra](#), [Github](https://github.com/E-RIHS/schema/blob/main/method-v1.0.schema.json)
* Related model: Method model (unavailable)

### `Organisation` metadata schema

This schema is intended to model the metadata and details required to document and describe **organisations (actors)** events within E-RIHS and IPERION-HS. 

Current version:

* Schema: [https://e-rihs.io/schema/organisation-v1.0.schema.json](https://e-rihs.io/schema/organisation-v1.0.schema.json)
* Version: v1.0 (currently as a **living draft**)
* Links: [Cordra](#), [Github](https://github.com/E-RIHS/schema/blob/main/organisation-v1.0.schema.json)
* Related model: Actor model (unavailable)

### `Person` metadata schema

This schema is intended to model the metadata and details required to document and describe **persons (actors)** events within E-RIHS and IPERION-HS. 

Current version:

* Schema: [https://e-rihs.io/schema/person-v1.0.schema.json](https://e-rihs.io/schema/person-v1.0.schema.json)
* Version: v1.0 (currently as a **living draft**)
* Links: [Cordra](#), [Github](https://github.com/E-RIHS/schema/blob/main/person-v1.0.schema.json)
* Related model: Actor model (unavailable)

### `Service` metadata schema

This schema is intended to model the metadata and details required to document and describe **service** or **access** providers within E-RIHS and IPERION-HS. These services will be offered by one or more **funding programmes** and exploited > in one or more research **projects**. It is anticipated that services will be defined as part of the registoring a service in the categlogue of service.

Current version:

* Schema: [https://e-rihs.io/schema/service-v1.0.schema.json](https://e-rihs.io/schema/service-v1.0.schema.json)
* Version: v1.0 (currently as a **living draft**)
* Links: [Cordra](#), [Github](https://github.com/E-RIHS/schema/blob/main/service-v1.0.schema.json)
* Related model: Service model (unavailable)


### `Software` metadata schema

This schema is intended to model the metadata and details required to document and describe **software (tools)** used within an offered service in E-RIHS and IPERION-HS.

Current version:

* Schema: [https://e-rihs.io/schema/software-v1.0.schema.json](https://e-rihs.io/schema/software-v1.0.schema.json)
* Version: v1.0 (currently as a **living draft**)
* Links: [Cordra](#), [Github](https://github.com/E-RIHS/schema/blob/main/software-v1.0.schema.json)
* Related model: Tool model (unavailable)


### `Technique` metadata schema

This schema is intended to model the metadata and details required to document and describe **techniques** that are used within access offerings in E-RIHS and IPERION-HS. 

Current version:

* Schema: [https://e-rihs.io/schema/technique-v1.0.schema.json](https://e-rihs.io/schema/technique-v1.0.schema.json)
* Version: v1.0 (currently as a **living draft**)
* Links: [Cordra](#), [Github](https://github.com/E-RIHS/schema/blob/main/technique-v1.0.schema.json)
* Related model: Technique model (unavailable)


## Special schemas

### `Controlled lists` helper schema

This schema collects all controlled list definitions with the link to the corresponding endpoint. These definitions are referenced throughout all other schemas as reusable components, and as such, this schema is not meant to be used as a standalone schema to model instances. There is no related model.

*Note: The schema in Github only contains a link to the controlled list endpoint. The version in Cordra is automatically populated with `enum` and `enum_titles` values*

Current version:

* Schema: [https://e-rihs.io/schema/controlled_lists-v1.0.schema.json](https://e-rihs.io/schema/controlled_lists-v1.0.schema.json)
* Version: v1.0 (currently as a **living draft**)
* Links: [Cordra](https://data.e-rihs.io/#objects/e-rihs.io/2a7a2b5031320ba6223b), [Github](https://github.com/E-RIHS/schema/blob/main/controlled_lists-v1.0.schema.json)
* Related model: none

### `CordraGroup` administrative schema

### `CordraUser` administrative schema

## Tools

The directory ['tools'](https://github.com/E-RIHS/schema/tree/main/tools) contains a set of useful scripts manipulate (validation, synchronisation...) the schema.

## Acknowledgement
This work project was supported by:

### The H2020 [IPERION-HS](https://www.iperionhs.eu/) project
[<img height="64px" src="https://github.com/jpadfield/simple-modelling/raw/master/docs/graphics/IPERION-HS%20Logo.png" alt="IPERION-HS">](https://www.iperionhs.eu/)<br/>
[<img height="32px" src="https://github.com/jpadfield/simple-modelling/raw/master/docs/graphics/iperionhs-eu-tag2.png" alt="IPERION-HS">](https://www.iperionhs.eu/)
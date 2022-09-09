# Heritage Science Schema Repository

This repository has been created to host completed heritage science metadata gathering json schema. Work and discussion relating to the development of these schema is being carried out within: [https://github.com/E-RIHS/hs-interoperability](https://github.com/E-RIHS/hs-interoperability)

For each type of schema, such as **Project**, create a section in this README file, as shown for **Project** to provide direct links to the current and developmental versions of each scheme along with a table of recent updates and changes. 

Schema documents should be named using lowercase letters, according to the following naming structure: **name-v0.0.schema.json**. Changes to the first version number are reserverd for major changes that might include breaking changes, the second version number should be used for more minor changes including. Versions below 1.0 should be used for the intial development of each schema and therefore all versions changes, below 1.0, can include breaking changes even though the first part of the version number stays at 0.

GitHub pages have been set up based on the root directory of this repository, this provides a much cleaner URL, but there can be a temporary lag between when new files are added and when the links will work. However, once the files have been added in there is no additional delay. 
* [https://e-rihs.github.io/schema/project-v0.2.schema.json](https://e-rihs.github.io/schema/project-v0.2.schema.json)

Issues and ideas related to the schema published here can be added directly into the [Issues System](https://github.com/E-RIHS/schema/issues).

The schema GitHub repository can be access directly [here](https://github.com/E-RIHS/schema/). Additional modeling work and discussions relating to interoprability can be found [here](https://github.com/E-RIHS/hs-interoperability/).

## Project metadata schema

This schema is intended to model the metadata and details required to document and describe smaller scale research activities and **access** events within E-RIHS and IPERION-HS. The identity of larger scale projects and initiatives are currently modelled as **funding programme**. It is anticipated that the process of documenting a **project** could be initiated as part of the application process rather than an additional extra step to be carried out at a latter date.

* Current Version: [https://e-rihs.github.io/schema/project-v0.2.schema.json](https://e-rihs.github.io/schema/project-v0.2.schema.json)
* Draft Version: TBC
* Related simple models can be see [here](https://github.com/E-RIHS/hs-interoperability/tree/main/Shared%20Models).

| Date  | Author | Version | Comment |
| :-----------: | :-----------: | :-----------: | ----------- |
| 17-08-2022 | W Fremount | 0.1 | Based on task discussions this is an initial work up of the Project model into a schema file. |
| 24-08-2022 | W Fremount | 0.2 | The project text descriptions have been moved to the top level, rather than being nested under the idea of a "Research Question", which has been removed. The notion of research categories has also been added. The idea "scope notes" describing each section or piece of metadata still need to be added.|
| <img width=325 /> |<img width=175 /> | <img width=60 /> | <img width=500 /> |

## Acknowledgement
This work project was supported by:

### The H2020 [IPERION-HS](https://www.iperionhs.eu/) project
[<img height="64px" src="https://github.com/jpadfield/simple-modelling/raw/master/docs/graphics/IPERION-HS%20Logo.png" alt="IPERION-HS">](https://www.iperionhs.eu/)<br/>
[<img height="32px" src="https://github.com/jpadfield/simple-modelling/raw/master/docs/graphics/iperionhs-eu-tag2.png" alt="IPERION-HS">](https://www.iperionhs.eu/)

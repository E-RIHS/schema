# Heritage Science Schema Repository

This repository has been created to host completed heritage science metadata gathering json schema. Work and discussion relating to the development of these schema is being carried out within: [https://github.com/E-RIHS/hs-interoperability](https://github.com/E-RIHS/hs-interoperability)

For each type of schema, such as **Project**, create a section in this README file, as shown for **Project** to provide direct links to the current and developmental versions of each scheme along with a table of recent updates and changes. 

Schema documents should be named using lowercase letters, according to the following naming structure: **name-v0.0.schema.json**. Changes to the first version number are reserverd for major changes that might include breaking changes, the second version number should be used for more minor changes including. Versions below 1.0 should be used for the intial development of each schema and therefore all versions changes, below 1.0, can include breaking changes even though the first part of the version number stays at 0.

GitHub pages have been set up based on the root directory of this repository, this provides a much cleaner URL, but there can be a temporary lag between when new files are added and when the links will work. However, once the files have been added in there is no additional delay. 
* [https://e-rihs.io/schema/project-v0.3.schema.json](https://e-rihs.io/schema/project-v0.3.schema.json)

Issues and ideas related to the schema published here can be added directly into the [Issues System](https://github.com/E-RIHS/schema/issues).

The schema GitHub repository can be access directly [here](https://github.com/E-RIHS/schema/). Additional modeling work and discussions relating to interoprability can be found [here](https://github.com/E-RIHS/hs-interoperability/).

## Service metadata schema

This schema is intended to model the metadata and details required to document and describe **service** or **access** providers within E-RIHS and IPERION-HS. These services will be offered by one or more **funding programmes** and exploited in one or more research **projects**. It is anticipated that services will be defined as part of the registoring a service in the categlogue of service.

* Current Version: [https://e-rihs.io/schema/service-v0.4.schema.json](https://e-rihs.io/schema/service-v0.5.schema.json)
* Draft Version: TBC
* Related simple models can be see [here](https://github.com/E-RIHS/hs-interoperability/tree/main/Shared%20Models).

| Date  | Author | Version | Comment |
| :-----------: | :-----------: | :-----------: | ----------- |
| 28-11-2022 | J Padfield | 0.1 | The service record is intended to define the top level descriptions and catergoisations of the a given service. It is anticipated that the more detailed descriptions of the equipment and workflows etc. will be described separeatly and linked to the service record.|
| 01-02-2023 | J Padfield | 0.2 | THis model has been updated to match the discussed needs of E-RIHS along with additional fields to support the development of DIgital services.|
| 23-02-2023 | W Fremout, J Padfield | 0.3 | This model has been updated based on the concept of a Record, which was used to define Tools and services to be listed under E-RIHS.io - a few fields have had some additional examples added - but new metadata fields were also added - the concept of Administration fields was also introduced.|
| 01-03-2023 | W Fremout | 0.4 | This model has been updated based on the discussions during the weekly IPERION HS T6.3 meeting.|
| 21-06-2023 | W Fremout | 0.5 | This model has been updated based on the discussions during the weekly IPERION HS T6.3 meeting to match with model v0.5.|
| <img width=325 /> |<img width=175 /> | <img width=60 /> | <img width=500 /> |


## Project metadata schema

This schema is intended to model the metadata and details required to document and describe smaller scale research activities and **access** events within E-RIHS and IPERION-HS. The identity of larger scale projects and initiatives are currently modelled as **funding programme**. It is anticipated that the process of documenting a **project** could be initiated as part of the application process rather than an additional extra step to be carried out at a latter date.

* Current Version: [https://e-rihs.io/schema/project-v0.5.schema.json](https://e-rihs.io/schema/project-v0.5.schema.json)
* Draft Version: TBC
* Related simple models can be see [here](https://github.com/E-RIHS/hs-interoperability/tree/main/Shared%20Models).

| Date  | Author | Version | Comment |
| :-----------: | :-----------: | :-----------: | ----------- |
| 17-08-2022 | W Fremout | 0.1 | Based on task discussions this is an initial work up of the Project model into a schema file. |
| 24-08-2022 | W Fremout | 0.3 | The project text descriptions have been moved to the top level, rather than being nested under the idea of a "Research Question", which has been removed. The notion of research categories has also been added. The idea "scope notes" describing each section or piece of metadata still need to be added.|
| 28-06-2023 | J Padfield | 0.5 | The schema has been further developed to match changes made to other models and to conform with naming conventiones.|
| <img width=325 /> |<img width=175 /> | <img width=60 /> | <img width=500 /> |


## Actor metadata schemas

For practical reasons the Actor model is implemented in two separate schemas: **Person** and **Organisation**.

### Person metadata schema

This schema is intended to model the metadata and details required to document and describe **persons (actors)** events within E-RIHS and IPERION-HS. 

* Current Version: [https://e-rihs.io/schema/person-v0.2.schema.json](https://e-rihs.io/schema/person-v0.2.schema.json)
* Draft Version: TBC
* Related simple models can be see [here](https://github.com/E-RIHS/hs-interoperability/tree/main/Shared%20Models).

| Date  | Author | Version | Comment |
| :-----------: | :-----------: | :-----------: | ----------- |
| 11-05-2023 | W Fremout | 0.2 | Based on task discussions this is an initial work up of the Actor model (v0.2) into a schema file. For compatibility reasons, we have chosen to make a separate schema for persons. |
| <img width=325 /> |<img width=175 /> | <img width=60 /> | <img width=500 /> |

### Organisation metadata schema

This schema is intended to model the metadata and details required to document and describe **organisations (actors)** events within E-RIHS and IPERION-HS. 

* Current Version: [https://e-rihs.io/schema/organisation-v0.2.schema.json](https://e-rihs.io/schema/organisation-v0.2.schema.json)
* Draft Version: TBC
* Related simple models can be see [here](https://github.com/E-RIHS/hs-interoperability/tree/main/Shared%20Models).

| Date  | Author | Version | Comment |
| :-----------: | :-----------: | :-----------: | ----------- |
| 11-05-2023 | W Fremout | 0.2 | Based on task discussions this is an initial work up of the Actor model (v0.2) into a schema file. For compatibility reasons, we have chosen to make a separate schema for organisations. |
| <img width=325 /> |<img width=175 /> | <img width=60 /> | <img width=500 /> |


## Technique metadata schema

This schema is intended to model the metadata and details required to document and describe **techniques** that are used within access offerings in E-RIHS and IPERION-HS. 

* Current Version: [https://e-rihs.io/schema/technique-v0.4.schema.json](https://e-rihs.io/schema/technique-v0.4.schema.json)
* Draft Version: TBC
* Related simple models can be see [here](https://github.com/E-RIHS/hs-interoperability/tree/main/Shared%20Models).

| Date  | Author | Version | Comment |
| :-----------: | :-----------: | :-----------: | ----------- |
| 31-05-2023 | W Fremout | 0.4 | Schema developed during an online meeting to match with the corresponding model 0.4.|
| <img width=325 /> |<img width=175 /> | <img width=60 /> | <img width=500 /> |


## Tools metadata schemas

For practical reasons the Tools model is implemented in two separate schemas: **Equipment** and **Software**.

### Equipment metadata schema

This schema is intended to model the metadata and details required to document and describe **equipments (tools)** used within an offered service in E-RIHS and IPERION-HS. 

* Current Version: [https://e-rihs.io/schema/equipment-v0.3.schema.json](https://e-rihs.io/schema/equipment-v0.3.schema.json)
* Draft Version: TBC
* Related simple models can be see [here](https://github.com/E-RIHS/hs-interoperability/tree/main/Shared%20Models).

| Date  | Author | Version | Comment |
| :-----------: | :-----------: | :-----------: | ----------- |
| 14-06-2023 | W Fremout | 0.3 | Based on task discussions this is an initial work up of the Equipment/Tools model (v0.3) into a schema file. For compatibility reasons, we have chosen to make a separate schema for equipment and software. |
| <img width=325 /> |<img width=175 /> | <img width=60 /> | <img width=500 /> |

### Software metadata schema

This schema is intended to model the metadata and details required to document and describe **software (tools)** used within an offered service in E-RIHS and IPERION-HS.

* Current Version: [https://e-rihs.io/schema/software-v0.3.schema.json](https://e-rihs.io/schema/software-v0.3.schema.json)
* Draft Version: TBC
* Related simple models can be see [here](https://github.com/E-RIHS/hs-interoperability/tree/main/Shared%20Models).

| Date  | Author | Version | Comment |
| :-----------: | :-----------: | :-----------: | ----------- |
| 19-07-2023 | W Fremout, J Padfield | 0.3 | Based on task discussions this is an initial work up of the Software/Tools model (v0.3) into a schema file. For compatibility reasons, we have chosen to make a separate schema for equipment and software. |
| <img width=325 /> |<img width=175 /> | <img width=60 /> | <img width=500 /> |

## Acknowledgement
This work project was supported by:

### The H2020 [IPERION-HS](https://www.iperionhs.eu/) project
[<img height="64px" src="https://github.com/jpadfield/simple-modelling/raw/master/docs/graphics/IPERION-HS%20Logo.png" alt="IPERION-HS">](https://www.iperionhs.eu/)<br/>
[<img height="32px" src="https://github.com/jpadfield/simple-modelling/raw/master/docs/graphics/iperionhs-eu-tag2.png" alt="IPERION-HS">](https://www.iperionhs.eu/)

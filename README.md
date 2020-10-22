# Med Cabinet for Cannabis Consumers
A cross team project to help patients find the right strain, dosing, intake method and schedule.

## Data Science
For the Data Science portion of this project we created a connection from the raw dataset and the predictive learning model to an API. This API will be used by the WEB team to create an app for new users of cannabis and existing users to find the best strain to treat their ailments.

- The predictive model trained for this API to utilize is a K Nearest Neighbor model. The model will return the 5 most likely strains based on the information provided by the user. This model was created and trained by [Toby Chen](https://github.com/TobyChen320).

- The connection was created using FastAPI. Then was deployed to Heroku. This connection was a team effort created by [Joanne Middour](https://github.com/jmmiddour) and [Zachary Snyder](https://github.com/zsnyder20).

- **Deployed to Heroku: https://strains-cannabis.herokuapp.com/**

## Schema
The API contains two databases strains and inputs. strains contains all the possible outputs that the model can return. The inputs database will contain the search history of the users as they utilize the API for future research purposes(currently not functional as of 10/21/2020). 
The database is structured as follows:  
    - Strains  
      - ID: Primary Key integer identifier for each strain in the table   
      - Strain_name: String identifier for the strains     
      - Strain_type: identifies the variant of the marijuana (Sativa, Indica or Hybrid)  
      - Description: string describing the strain  
      - Effect: Expected impacts of consuming the strain  
      - Aliment: Medical conditions that the strain is intended to alleviate  
      - Flavor: What the strain is intended to taste like   
    - Inputs  
      - ID: Primary Key integer identifier for each user input   
      - Aliment_In: User inputted Aliment   
      - Flavor_In: User inputted Flavor  
      - Effects_In: User inputted effects  
      - Strain_In: Model output based on user outputs   

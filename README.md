This is the capstone project for the Full Stack Developer Nanodegree. This simple application has two data tables - Projects and Actors. Projects have attributes Title and Release Date, while Actors have names, genders, and ages.

This application uses Auth0 to manage different user types and permissions. Casting Assistants have the most limited permissions - with the ability to only view actors and movies. Casting Directors can do everything Casting Assistants can do and also edit (patch) actors and projects and create new actors. Executive Producers have Casting Director permissions and can also create new projects. 

The login/register page for this application can be found at: https://cwinterb.auth0.com/authorize?audience=agency&response_type=token&client_id=niAAnrxzVlTXC5J3K76pLItw8JiSj9LV&redirect_uri=https://talent-agency-capstone-2.herokuapp.com/

This project has been deployed to production using Heroku and can be found at this URL: https://talent-agency-capstone-2.herokuapp.com/

This application includes the following endpoints: 


GET /actors 
Fetches all actors in the database in a JSON body

POST /actors 
Creates a new Actor with arguments name, age, gender

PATCH /actors/id
When provided an actor’s id and a JSON request, this endpoint will update the actor with the arguments supplied in the request

DELETE /actors/id
When provided an actor’s id this endpoint will delete that actor from the database

GET /projects
Fetches all actors in the database in a JSON body

POST /projects
Creates a new Project with arguments title and release date

PATCH /projects/id
When provided a project’s id and a JSON request, this endpoint will update the project with the arguments supplied in the request

DELETE /project/id
Wh	en provided a project’s id this endpoint will delete that project from the database

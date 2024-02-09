<!-- PROJECT SHIELDS -->

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![Activity][activity-shield]][activity-url]
<!-- [![Stargazers][stars-shield]][stars-url] -->


<!-- TABLE OF CONTENTS -->
<details>
    <summary> Table of Contents </summary>
    <ol>
        <li>
            <a href="#about"> About the project</a>
            <ul>
                <li><a href="#built-with">Built With</a>
            </ul>
        </li>
        <li>
            <a href="#prerequisites"> Prerequisites</a>
        </li>
        <li>
            <a href="#installation"> Installation</a>
        </li>
        <li>
            <a href="#license"> License</a>
        </li>
    </ol>
</details>


<!-- ABOUT THE PROJECT -->
## About
<div align="center">
<h3 align="center">Accessible Routes</h3>
    <a href="https://github.com/json-mp3/Accessible-Routes">
<img src="https://github.com/zxhjlk/Accessible-Routes/blob/main/Logo.png" alt="ARoutes Logo" width="360" height="216">
</a>
<p>The Accessible Routes project was established to provide students with a guide to navigating a less-than-accessible campus.</p>
</div>

### Built With

* [![React][React.js]][React-url]
* [![Node][Node.js]][Node-url]
* [![JavaScript][JavaScript.com]][JavaScript-url]
* [![PostgreSQL][PostgreSQL.com]][PostgreSQL-url]
* [![Open Street Map][OpenStreetMap.com]][OpenStreetMap-url]

<!-- Getting Started -->
## Prerequisites
 * Clone or fork the repo
    * GitHub Desktop: download [here](https://desktop.github.com/)
    * Clone repo through Git Bash
    ```sh
    $ git clone https://github.com/Accessible-Routes/Database
    ```
    * To fork, press the fork button on the top right of the repo, or [here](https://github.com/json-mp3/Accessible-Routes/fork)
 * [Django](https://www.djangoproject.com/start/overview/)
    * Install through pip
   ```sh
   pip install Django
   ```


## Installation
>The backend for Accessible Routes is written using the Django Framework.
[https://docs.djangoproject.com/en/4.2/intro/overview/](https://docs.djangoproject.com/en/4.2/intro/overview/)

To start the backend, you have to create the database then migrate the database.

### Part 1: Create the database
1. Install PostgreSQL and PgAdmin. The version that the production server uses is version 16 but any version should work.
2. Follow step 6 on here: https://stackpython.medium.com/how-to-start-django-project-with-a-database-postgresql-aaa1d74659d8
    Take note of the NAME, USER, PASSWORD, HOST, and PORT. The username and password you set will be needed to connect to the database
    using Django.

### Part 2: Migrate the database
1. (Optional) Create a python virtual environment and start it.
2. Run "pip install -r Django/requirements.txt"
3. Run "python Django/backend/manage.py makemigrations"
4. Run "python Django/backend/manage.py migrate"
5. Run "python Django/backend/manage.py runserver"

If start successfully, you should see something like "Starting development server at http://127.0.0.1:8000/"
If you are having issues, they may be related to setting up the Postgres database locally.

The main API that is needed is below:
Create an API key for requests that need API Keys.

GET <url>/api/all-buildings returns a list of json with buildings. 

GET <url>/api/all-rooms returns a json of each building and a list in each building for every room that exists.

GET <url>/api/rooms/<room_id> returns data about that room specifically.

POST <url>/api/create-room/ creates a room and connections to that room. Room data should be in the request body.
                                                                    NOTE: The room must exists meaning if you want connect two newly made rooms. 
                                                                    You must create the two rooms then modify them to connect them.
                                                                    This request is API key authenicated.

POST <url>/api/edit-room/ modify a room. Room must exist to modify its data. Room data that can be edited are the room number,
                                                                    room_type, building_id, stairs, elevator, ramps, accessible, connected_rooms, 
                                                                    and tags. 

POST <url>/api/recreate/ recreates the outdoor nodes database. The post requires a json and assumes the data in the json is valid then
                                                                    deletes the outdoor database and recreates it based on the json.

GET <url>/api/get-route/ gets the route from two building. The request data should be a query param with the start and 
                                                                    end building UUID.


## License

Distributed under the MIT License. See [LICENSE](https://github.com/json-mp3/Accessible-Routes/blob/main/LICENSE) for more information.

<!-- https://home.aveek.io/GitHub-Profile-Badges/ -->

<!-- LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/json-mp3/Accessible-Routes.svg?style=for-the-badge
[contributors-url]: https://github.com/json-mp3/Accessible-Routes/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/json-mp3/Accessible-Routes.svg?style=for-the-badge
[forks-url]: https://github.com/json-mp3/Accessible-Routes/network/members
[stars-shield]: https://img.shields.io/github/stars/json-mp3/Accessible-Routes.svg?style=for-the-badge
[stars-url]: https://github.com/json-mp3/Accessible-Routes/stargazers
[issues-shield]: https://img.shields.io/github/issues/json-mp3/Accessible-Routes.svg?style=for-the-badge
[issues-url]:  https://github.com/json-mp3/Accessible-Routes/issues
[license-shield]: https://img.shields.io/github/license/json-mp3/Accessible-Routes.svg?style=for-the-badge
[license-url]: https://github.com/json-mp3/Accessible-Routes/blob/master/LICENSE.txt

[activity-shield]: https://img.shields.io/github/last-commit/json-mp3/accessible-routes?style=for-the-badge
[activity-url]: https://github.com/Zxhjlk/Accessible-Routes/activity



[JavaScript.com]: https://img.shields.io/badge/JavaScript-F7DF1E.svg?style=for-the-badge&logo=JavaScript&logoColor=black
[JavaScript-url]: https://www.javascript.com/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[PostgreSQL.com]: https://img.shields.io/badge/PostgreSQL-4169E1.svg?style=for-the-badge&logo=PostgreSQL&logoColor=white
[PostgreSQL-url]: https://www.postgresql.org/
[OpenStreetMap.com]: https://img.shields.io/badge/OpenStreetMap-7EBC6F.svg?style=for-the-badge&logo=OpenStreetMap&logoColor=white
[OpenStreetMap-url]: https://openstreetmap.org
[Node.js]: https://img.shields.io/badge/Node.js-339933.svg?style=for-the-badge&logo=nodedotjs&logoColor=white
[Node-url]: https://nodejs.org/en
# IME-Inventory-Database

## Technical Instructions

### Tech Stack:

Frontend: Javascript ES6, CSS, HTML (Jinja template language, mainly to work with Flask)
Backend: Flask, pymongo
Database: MongoDB

### Deploy on AWS

- Account: `pme.developer@gmail.com`
- Password: See email
- Recommended hosting environment: AWS Lightsail - Amazon Linux 2 ($3.5/month)
- Deployment: git pull, luanch through `docker-compose up --build` (be sure to update development configuration in `development.env` if used for production)

### Questions about Code/Repo Maintainance

Email me.

## Todos

As of Jun 10, 2021:
- **Responsive Mobile UI**: Currently the UI breaks down on smaller screens. Add some `@media` conditions in the css files to mix it.
- **User information editing page**: Allow users to edit their information on their user page.
- **Email confirmation system**: Setup an email for the site so that users can get email confirmation when registaring accounts. I would imagine this involves getting a domain name first, although if there might be a way to make do with Gmail API?
- **Password retrieval**: Allow user to change password. It will probably involve working with the site email system.
- **Institution sign in**: Integrate UChicago's shibboleth sign in system so users can sign in using their UChicago account. This likely involves a lot of dicussion with the IT staff and a lot of system design choices. I would start with understanding the current database scheme and see if we can use some kind of common identifier to link UChicago account with our current user scheme, but if you feel like scraping the whole thing thats fine too.
- **Hosting options/hostname**: Follow the hosting option above to set up a new server environment, then contact the school IT staff to discuss hostname options. (Regarding AWS: From my discussion with them, hosting on AWS seems to make integration into the school's system easier. But docker-compose is pretty versatile and we are already using a complete virtual environemnt, so integration should be possible whereever you host your development server.)
- **Bulk Upload**: This is a requested feature from the early feedbacks we gathered. This will probably lead to big changes from database to the frontend template. Again, a lot of work but certainly possible.





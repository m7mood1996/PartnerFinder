
# Partner Finder Search Engine

> A smart search engine that enables searching for research partners in a short time using NLP on tags and keywords and descriptions.

<div align="center"><img src="https://i.imgur.com/iyxryPA.jpg" width="400" height="300"/></div>

<br>

---

### Table of Contents

- [Description](#description)
- [How To Use](#how-to-use)
- [References](#references)
- [License](#license)
- [Author Info](#author-info)

---

## Description

Search engine that connected to two repositories, the European Union and B2match. 
It has more than 5M organizations, and 300K participants. 
The engine uses NLP and TF-IDF for comparing tags from user to tags and descriptions of the organizations and the participants in order to get accurate results.
The website updates the repositories each month using scheduled tasks which executes by celery library. it also has automatic alerts for finding potential calls from the EU that has at least three partners from three different countries, and alerts for potential events from b2match.

### Technologies

- Django Framework
- MongoDB
- React.JS
- Material-UI
- Python
- NLTK
- Gensim
- Celery
- VS Code
- Pycharm

[Back To The Top](#partner-finder-search-engine)

---

## How To Use

### Installation

- Copy this link ***https://github.com/bashbash96/PartnerFinder.git*** then on cmd or bash do:

		cd ~/Desktop
		git clone {{the link you just copied}} Project

- This creates a directory named "Project", clones the repository there and adds a remote named "origin" back to the source.

		cd Project
		git checkout develop

- If that last command fails

		git checkout -b develop

------------
### Updating/The Development Cycle

You now have a git repository, likely with two branches: master and develop. Now bake these laws into your mind and process:

You will never commit to ***master*** or ***develop*** directly  .

Instead, you will create ***feature branches*** on your machine that exist for the purpose of solving singular issues. You will always base your features off the develop branch.

		git checkout develop
		git checkout -b my-feature-branch

This last command creates a new branch named "my-feature-branch" based off of develop. You can name that branch whatever you like. You should not have to push it to Github unless you intend to work on multiple machines on that feature.

Make changes.

	git add .
	git commit -am "I have made some changes."

This adds any new files to be tracked and makes a commit. Now let's add them to develop.

	git checkout develop
	git merge --no-ff my-feature-branch
	git push origin develop
------------
### Releasing

Finished with your project?

- Create a feature branch as normal.
- Update the version history in the README.md file
- Update this to develop as normal.

		git checkout master
		git merge --no-ff develop
		git push origin master
		git tag v1.0.0
		git push origin v1.0.0
------------
### Front-end

In the Frontend\partner-finder directory, you can run:

### `npm start`

Runs the app in the development mode.<br>
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.<br>
You will also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.<br>
See the section about [running tests](#running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.<br>
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.<br>
Your app is ready to be deployed!

See the section about [deployment](#deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can’t go back!**

If you aren’t satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (Webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you’re on your own.

You don’t have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn’t feel obligated to use this feature. However we understand that this tool wouldn’t be useful if you couldn’t customize it when you are ready for it.

### Installing a Dependency

The generated project includes React and ReactDOM as dependencies. It also includes a set of scripts used by Create React App as a development dependency. You may install other dependencies (for example, React Router) with `npm`:

```
npm install --save <library-name>
```


### Adding Bootstrap

You don’t have to use [React Bootstrap](https://react-bootstrap.github.io) together with React but it is a popular library for integrating Bootstrap with React apps. If you need it, you can integrate it with Create React App by following these steps:

Install React Bootstrap and Bootstrap from NPM. React Bootstrap does not include Bootstrap CSS so this needs to be installed as well:

```
npm install react-bootstrap --save
npm install bootstrap@3 --save
```

Import Bootstrap CSS and optionally Bootstrap theme CSS in the ```src/index.js``` file:

```js
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/css/bootstrap-theme.css';
```

Import required React Bootstrap components within ```src/App.js``` file or your custom component files:

```js
import { Navbar, Jumbotron, Button } from 'react-bootstrap';
```

Now you are ready to use the imported React Bootstrap components within your component hierarchy defined in the render method. Here is an example [`App.js`](https://gist.githubusercontent.com/gaearon/85d8c067f6af1e56277c82d19fd4da7b/raw/6158dd991b67284e9fc8d70b9d973efe87659d72/App.js) redone using React Bootstrap.

------------
### Back-end

To run locally, do the following on Backend directory:

1. Create a Python 3.5 virtualenv

2. Install dependencies:
	
```
pip install -r requirements/dev.txt
npm install
```

   Alternatively, use the make task:

```
make install
```
    

in Backend/src directory you can run:

1. When making changes:

```
python manage.py makemigrations
python manage.py migrate
```

2. Run the server locally:
```
python manage.py runserver
```

[Back To The Top](#partner-finder-search-engine)

---

## References

[`Django`](https://docs.djangoproject.com/en/3.0/)
[`MongoDB`](https://www.mongodb.com/)
[`React.JS`](https://reactjs.org/)
[`Material-UI`](https://material-ui.com/)
[`Python`](https://www.python.org/)
[`NLTK`](https://www.nltk.org/)
[`Gensim`](https://radimrehurek.com/gensim/auto_examples/index.html)
[`Celery`](https://docs.celeryproject.org/en/stable/index.html)
[`VS Code`](https://code.visualstudio.com/)
[`Pycharm`](https://www.jetbrains.com/pycharm/)
[`European Union`](https://europa.eu/european-union/index_en)
[`B2match`](https://www.b2match.com/?campaignid=9573624898&adgroupid=102132546887&adid=423539737408&gclid=CjwKCAjw57b3BRBlEiwA1ImytnO4GfNg9sZ09Q1SvQPE_fEiUVPjYqoy3oeu3rFPw91iVwmjd7-N8RoCMIkQAvD_BwE)

[Back To The Top](#partner-finder-search-engine)

---
## License

GPL License

Copyright (c) [2020] [Amjad Bashiti]

  The licenses for most software and other practical works are designed
to take away your freedom to share and change the works.  By contrast,
the GNU General Public License is intended to guarantee your freedom to
share and change all versions of a program--to make sure it remains free
software for all its users.  We, the Free Software Foundation, use the
GNU General Public License for most of our software; it applies also to
any other work released this way by its authors.  You can apply it to
your programs, too.

  When we speak of free software, we are referring to freedom, not
price.  Our General Public Licenses are designed to make sure that you
have the freedom to distribute copies of free software (and charge for
them if you wish), that you receive source code or can get it if you
want it, that you can change the software or use pieces of it in new
free programs, and that you know you can do these things.

  To protect your rights, we need to prevent others from denying you
these rights or asking you to surrender the rights.  Therefore, you have
certain responsibilities if you distribute copies of the software, or if
you modify it: responsibilities to respect the freedom of others.

  For example, if you distribute copies of such a program, whether
gratis or for a fee, you must pass on to the recipients the same
freedoms that you received.  You must make sure that they, too, receive
or can get the source code.  And you must show them these terms so they
know their rights.

[Back To The Top](#partner-finder-search-engine)

---
## Author Info

- Github - [bashbash96](https://github.com/bashbash96)
- Linkedin - [amjad-bashiti](https://www.linkedin.com/in/amjad-bashiti-2652a9192/)

[Back To The Top](#partner-finder-search-engine)

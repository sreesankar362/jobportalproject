# jobportalproject
-----------------------------------------------------------------------------------

### Main branch Merging with Working branch and pushing Steps:
    (from working branch)
    1.git add -A
    2.git commit -m 'message'
    3.git checkout main
    4.git pull 
    5.git checkout workingbranchname
    6.git merge main
    6.git status (to see changes) 
    %% Now main and your working branch is merged solve conflicts manually by
    editing conflicted files(removing == symbols and keep only the neededcode)
    
    (to push merged work to remote repository(main))
    7.git add -A
    8.git commit -m 'commit message'
    9.git push -u origin main workingbranchname
    
    10.come to github repository(browser) 'createpull request'
    11.create.
    12.Done


Heroku Deployment
https://medium.com/@shashankmohabia/deploying-a-django-app-to-heroku-using-github-repository-319c04a11c1a

Stripe Integration
https://www.geekinsta.com/integrate-stripe-with-django/

Postgresql setting on django project
link : https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-20-04

Git using for Team
link : https://www.freecodecamp.org/news/how-to-use-git-and-github-in-a-team-like-a-pro/
------------------------------------------------------------------------------------



1.open a new folder in pycharm

2.to get repository
  >git clone https://github.com/sreesankar362/jobportalproject.git

3.change directory to repository
  >cd jobportalproject

3.create and apply a new virtual environment

4.install packages from requirements.txt inside new virtual environment
  >pip install -r requirements.txt
  
5.

6. git branch   #list all branches

7. git checkout -b <newbranchname>       #create a new branch and switch to it

**make changes

Git local operation:

01 git init
02 git add filename
03 git commit -m "commit"
04 git status
05 git diff filename
06 git log 
   git log --pretty=oneline
07 git reset --hard HEAD^
08 git reset --hard "commit-id"
09 git reflog
10 git diff HEAD -- filename
11 git rm filename
12 git checkout -- filename

Git remote operation:

   #gen rsa private and public key
01 ssh-keygen -t rsa -C "your email addr"

   #relationship a remote git
02 git remote add origin git@github.com:github_username/Project_name.git

   #first push master bench all content to remote github
03 git push -u origin master
   
   #every change file and commit, push changed file to remote github 
   git push origin master



Main Function python micro web frame:
mirco_frame.py is Request, Router, Response
cookie.py is cookie
blog.py is test micro web frame.



PROJECT ON BUILDING CI-CD PIPELINE TOOL

1.	Task 1: Set Up a Simple HTML Project
(a) 	In VS Code create an HTML file and save as index.html
(b)	Push the HTML project to GitHub repository. Procedure is as follows:-
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/RalphFelix26/my-website.git
git push -u origin main

2.	Task 2: Set Up an AWS EC2/Local Linux Instance with Nginx

(a)	In AWS start  EC2 instance
(b)	Go to connect , and then to SSH of the EC2 instance and copy your ssh -i "your-key.pem" ec2-user@<ec2-public-ip>

(c)	Open power shell as an Administrator. CD to the folder where the pem key has been downloaded and saved. Feed the following:

ssh -i "your-key.pem" ec2-user@<ec2-public-ip>  # to connect to AWS

(d)	Install Nginx:
  sudo yum install nginx -y 

(e)	Start and enable Nginx:

    sudo systemctl start nginx
    sudo systemctl enable nginx

(f)	  Make a directory:
sudo mkdir my-html-project

(g)	  Clone the Git Repo:

  cd my-html-project
  sudo git clone https://github.com/RalphFelix26/my-website.git
  Result:
  Cloning into 'my-website'...
  remote: Enumerating objects: 15, done.
  remote: Counting objects: 100% (15/15), done.
  remote: Compressing objects: 100% (11/11), done.
  remote: Total 15 (delta 4), reused 14 (delta 3), pack-reused 0 (from 0)
  Receiving objects: 100% (15/15), 104.60 KiB | 14.94 MiB/s, done.
  Resolving deltas: 100% (4/4), done.

  sudo chmod -R 755 /var/www/html/my-html-project
  sudo chown -R nginx:nginx /var/www/html/my-html-project

(h)	Update the Nginx configuration to serve your HTML project:
  Create a configuration file for your project:
  
  sudo nano /etc/nginx/conf.d/html-project.conf

Enter the following details inside:-
    server {
        listen 80;
        server_name your-domain.com;

        root /var/www/html/my-html-project/my-website;
        index index.html;

        location / {
            try_files $uri $uri/ =404;
        }
    }


  	Save and exit.
  	Restart Nginx: sudo systemctl restart nginx

Task 3: Write a Python Script to Check for New Commits

(a)	Create the Python script to check for new commits:
  
  sudo nano /home/ec2-user/check_commits.py
  
  Feed the following code:
		
import requests
import os
import sys

# GitHub repository details
repoowner = "ralphfelix26"
reponame = "my-website"
GITHUB_API_URL = f"https://api.github.com/repos/{repoowner}/{reponame}/commits"

# File to store the last commit SHA
LAST_COMMIT_FILE = '/var/www/html/my-html-project/my-website/last_commit.txt'

def get_latest_commit():
    try:
        response = requests.get(GITHUB_API_URL)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        commits = response.json()
        return commits[0]['sha']
    except requests.exceptions.RequestException as e:
        print(f"HTTP error occurred: {e}")
        return None

def get_stored_commit():
    if os.path.exists(LAST_COMMIT_FILE):
        with open(LAST_COMMIT_FILE, 'r') as f:
            return f.read().strip()
    return None

def update_stored_commit(sha):
    os.makedirs(os.path.dirname(LAST_COMMIT_FILE), exist_ok=True)  # Ensure the directory exists
    with open(LAST_COMMIT_FILE, 'w') as f:
        f.write(sha)

if __name__ == "__main__":
    latest_commit = get_latest_commit()
    if latest_commit:
        stored_commit = get_stored_commit()
        if latest_commit != stored_commit:
            print("New commit detected")
            update_stored_commit(latest_commit)
            # Add deployment script execution here if needed
        else:
            print("No new commit")

Task 4: Write a Bash Script to Deploy the Code

(a)	Create the deployment script:
  
  sudo nano /home/ec2-user/update_website.sh

  Feed the following:

#!/bin/bash
REPO_URL="https://github.com/ralphfelix26/my-website.git"
REPO_DIR="/var/www/html/my-html-project/my-website"
WEBSITE_DIR="/var/www/html/my-html-project/my-website"
# These lines set up some information about where your files are
# Pull latest changes
cd $REPO_DIR || exit
git pull origin main
# This part goes to your local copy of the website and gets the latest changes
# Copy files to website directory
rsync -av --delete $REPO_DIR/ $WEBSITE_DIR/
# This copies the new files to where Nginx can find them
# Restart Nginx
sudo systemctl restart nginx
# This restarts Nginx to make sure it sees the new files
echo "Website updated successfully"
# This prints a message saying the update is done

(b)	Make the script executable:
  
  sudo chmod +x /home/ec2-user/update_website.sh

Task 5: Set Up a Cron Job to Run the Python Script

(a)	Create a wrapper script that runs both the Python and Bash scripts:
 
  sudo nano /home/ec2-user/ci_cd_wrapper.sh
  
  Feed the following:
  
#!/bin/bash
/usr/bin/python3 /home/ec2-user/check_commits.py

if [ $? -eq 0 ]; then
    /home/ec2-user/update_website.sh
fi

(b)	Make the code executable:
		sudo chmod +x /home/ec2-user/ci_cd_wrapper.sh

(c)	Setting-up a Cron Job that will run the script every 5 minutes:
  crontab -e
  
  Feed the the following to the cron file:
  
  */5 * * * * /home/ec2-user/ci_cd_wrapper.sh >> /home/ec2-user/ci_cd.log 2>&1

(d)	    Save the file and exit the cron editor:
  click ESC and type :wq






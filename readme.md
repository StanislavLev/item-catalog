# "Item catalog" project

This is car sell/buy site, where any registered user can create post about car sale.
Users can edit and delete their own posts.
Implemented a third-party authentication & authorization service: login with there Google+ account. 

## Installation

1. Install Python https://www.python.org/downloads/
2. Install Vagrant (https://www.vagrantup.com/)
3. Install VirtualBox (https://www.virtualbox.org/)
4. Download project files or clone the repo
5. Use command line (I used "Git Bash" https://git-scm.com/downloads), change directory to (your_path)\vagrant
    and Launch the Vagrant VM ("vagrant up")
6. Launch vagrant prompt: (vagrant ssh) and change directory (cd /vagrant/catalog)
7. Run the project (python project.py)
8. In browser open http://localhost:5000/
9. /vagrant/catalog/dummy_db_items.py file can be used to create posts in database, it uses pictures from /vagrant/tempPic4Upload/

## More information

For project were used
- Flask framework: http://flask.pocoo.org/
- Bootstrap framework: https://getbootstrap.com/

## License

Feel free to do whatever you want with the code.



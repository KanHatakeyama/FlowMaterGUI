# FlowMaterGUI
- Flowchart of Materials with Graphical User Interface (GUI)

# What is it?
- This is a Web-based digital labolatory notebook, compatible with machine learning
    -   Designed for chemistry and material science

![about](pics/about.PNG)

# How to use?
- Visit [here!](https://kanhatakeyama.github.io/expmanager_document/)

# Related paper
- https://chemrxiv.org/engage/chemrxiv/article-details/61ee04a671868d22fdbc8856

# Installization
## For beginners
- The system works on [Django framework](https://docs.djangoproject.com) of Python
    - Basic knowledge of Python and Django would be needed to run the program

## Setup
1. Clone this repositry
2. Setup Python environment according to "requirements.yml"
3. Runserver
    - ```python manage.py runserver```
    - Or, other command, such as 
        - ```gunicorn -b :8765 config.wsgi```
4. Access website
5. You can login the site with
    - Username: user
    - Pass: user

## Major packages to be installed
- Main framwrok
    - ```conda create -n django python=3.9```
    - ```pip install django-nested-inline```
    - ```pip install django-bootstrap5```
    - ```pip install django-ckeditor```
    - ```pip install django-import-export```
    - ```pip install django-cleanup```
    - ```conda install -c anaconda django -y```
    - ```conda install -c conda-forge rdkit -y```
    - ```conda install -c anaconda pillow -y```
    - ```conda install -c anaconda networkx -y```
    - ```conda install dtale -c conda-forge -y```
- Additional package to treat [Polymer structures](https://github.com/KanHatakeyama/PolyMolParser)
    - ```pip install git+https://github.com/KanHatakeyama/PolyMolParser.git```


- Modify bug on a current package
    - django-nested-inline (0.4.4)
        - Modification is needed to avoid a bug during saving records with "save as" option
        - [Check here](https://github.com/s-block/django-nested-inline/issues/139) to cope with the bug

# Version
- 2022.2.17 First prototype


# Author
- Kan Hatakeyama-Sato
- Waseda University
- https://kanhatakeyama.github.io/
- satokan@toki.waseda.(japan)
Open Correspondence
===================

A project to define the social networks that can be defined from letters written in the nineteenth century. Currently the project focuses on Charles Dickens but this will be expanded as new datasets are created. 

Project home page (wiki): http://wiki.okfn.org/p/Open_Letters

Installation and Setup
----------------------

You will need to have python, git, setuptools, virtualenv and pip to install ``openletters`` (all other dependencies will be automatically installed using pip):

    # create a new virtualenv
    virtualenv pyenv-openletters
    source pyenv-openletters/bin/activate

    # check out the code to openletters directory
    git clone https://github.com/okfn/openletters.git

    # move into the directory
    cd openletters

    # now install it to virtualenv at ../pyenv-openletters using pip
    pip install -r requirements.txt

Then you are ready to go.

Using the API
-------------

Most URLs can be suffixed with ?json to output data in JSON format. e.g. http://opencorrespondence.org/letter/548?json

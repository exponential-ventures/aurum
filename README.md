# aurum

Aurum is a new and simplified approach for data scientists to keep track of data and code without having to get another PhD for it. Aurum keeps track of all code and data changes, and lets you easily reproduce any experiment as well as easily compare metrics across experiments.

## Give it a try!

    pip install aurum

To create a new repository:

    $ mkdir newproject
    $ cd newproject
    $ au init

Aurum will create three directories for you:

    newproject/data
    newproject/src
    newproject/metrics

If your data lives in a remote system, configure aurum to retrieve and store data using your credentials:

    $ au remote add s3://

Then, add your data:

    $ wget https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data
    $ au data add adult.data

If your data already exists in the remote file system, add it by doing this:

    $ au data add remote remote_path_to_dataset  

Now work on it!

    $ cd src
    $ wget EXAMPLE_CODE_THAT_WORKS_WITH_EXAMPLE_DATASET.py
    $ python EXAMPLE_CODE_THAT_WORKS_WITH_EXAMPLE_DATASET.py

Everytime you run your code, aurum will track the changes and keep track of every experiment as well as its recorded metrics.

Check the performance evolution of your experiments by running:

    $ au metrics

If you want to go back to a specific experiment, run:

    $ au load exp_tag

Did we mention that Aurum runs on top of git? Now you can keep track of your data, code, and experiments all from any git server:

    $ git remote add origin https://github.com/user/repo.git
    $ git push origin master


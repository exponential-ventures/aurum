# aurum

Aurum is a new and simplified approach for data scientists to keep track of
data and code without having to get another PhD for it.

Aurum keeps track of all code and data changes, and lets you easily reproduce
any experiment as well as easily compare metrics across experiments.

__Aurum is currently in alpha state. There are a few rough edges we're still
working to get fixed, so use at your own risk! Feel free to issue pull requests
and contribute to the project__

## Give it a try!

    pip install aurum

To create a new repository:

    $ mkdir newproject
    $ cd newproject
    $ au init

Aurum will create the following directories for you:

    newproject/.au
    newproject/src
    newproject/logs

During the initialization step, Aurum will also create (or append to) the .gitignore file:

    newproject/.gitignore

If your data lives in a remote system, configure aurum to retrieve and store data using your credentials:

    $ au data add s3://bucket-name/dataset.csv --api kdljhkhsdskh --key lksjhdlkshsklh
    
or

    $ au data add ftp://dir/dataset.csv --user username --passwd password

If the data lives locally (in a directory outside the project directory), you must add it to Aurum manually:

    $ au data add /absolute/path/to/dataset.csv

If you want your data to just live inside the project, add it like this:

    $ wget https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data
    $ au data add adult.data
    
or

    $ au data add https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data

When the data being added is remote, Aurum will keep track of the dataset attributes to monitor any changes.


Once your project is initialized, and the data is added, you're ready to start working on it!

    $ cd src
    $ emacs experiment.py
    
Make sure to import aurum inside your experiment:
    
    #!/usr/bin/env python
    
    import aurum as au

It is also useful to keep track of the parameters used for training:

    au.parameters(a=0.01, b=1000, c=46, epochs=100, batch_size=200)
    
These parameters are then saved with the version to help you better keep track of all aspects of your experiment. Once the parameters are set, you can use them inside the code as follows:

    print(f"Parameter a = {au.a}")
    >>> Parameter a = 0.01

One of the advantages of registering the parameters with aurum before using is that you can pass them via command line to the experiment execution, as follows:

    python experiment.py a=0.01 b=1000 c=46 epochs=100 batch_size=200
   
If the parameters are also specified inside the code, the command line arguments will take precedence.
This trick is specially interesting if you'd like to automate the execution of multiple experiments, varying the parameters
automatically.

Sometimes you want to keep track of your file. You can do this with `aurum` running this:

    myTrainedModel = ... # train your model
    au.save_model(pickle.dumps(myTrainedModel))

Note that we used the pickle example here, but all you need to do is to pass the `byte[]` representation of your model and it will handle it. You don't need to use `pickle` to serialise data, you can use anything you want. Now on the next iteration you won't need to loose time training your model again. All you need to do in that case is:

    myLastTrainedModel = pickle.loads(au.load_model())

Note that the `load_model` method will return the previously registered `byte[]` representation of your model. So, the use of pickle is not mandatory and you can serialise and desserialise it the way you want.

At the end of your script, make sure to add the relevant metrics for comparison, and tell aurum that the experiment ends there.    
    
    au.register_metric(error=0.01, accuracy=0.99, ...)
    au.end_experiment()

If you're using Stripping, aurum will by default prevent the local cache from being added to the repository.

If you're using Catalysis to retrieve data, aurum will automatically keep track of the all data used in the project.

Once you're ready to test your experiment, just run it: 

    $ python experiment.py

Everytime you run your code, aurum will track the changes and keep track of every experiment as well as its recorded metrics.

If you make changes to your code that you want to commit to the repository but you're not yet ready to run it, just use git! Because aurum is just an extension of git, all git commands will work as usual inside an aurum project:

    $ git commit -m "Staged x, y, and z. Changes related to a, b, and c."
    $ git push

After you're run your experiment a few times, you can check the performance and compare the results from the command line:

    $ au metrics # display metrics from all experiments
    $ au metrics acfdf6cd-1f1a-4929-b036-7b0a5399b0c6 # display metrics of the experiment with id acfdf6cd-1f1a-4929-b036-7b0a5399b0c6
    $ au metrics acfdf6cd-1f1a-4929-b036-7b0a5399b0c6,280459c5-b183-462d-b89e-e53019f81c88 # display metrics of the experiments with id acfdf6cd-1f1a-4929-b036-7b0 and 280459c5-b183-462d-b89e-e53019f81c88

If you want to go back to a specific experiment, run:

    $ au load exp_tag

If you want to export the experiment to be sent and run somewhere else, Aurum will create a zip
package containing the requirements.txt, the dataset, the metrics, the logs, and everything else
specific to the experiment. If you'd rather not add specific artifact to the package, you can
leave it out by passing configuration arguments.

    $ au export exp_tag

If you want to leave the dataset out of the package, do as follows:

    $ au export exp_tag --no-data


## How does Aurum keeps track of my experiments?

At the end of each experiment, Aurum will create a new version for the experiment making sure
to save the logs, metrics, data attributes, code, requirements, etc. into the repository.

Once the commit is made, a tag is created to mark the experiment.

In order to deal with concurrency (and avoid conflicts) the experiments won't make changes to
any files. Instead, they'll create a brand new file for the current experiment and drop the
ones that are not related to the current experiment.

The experiment itself should use the aurum parameters to allow for the experiment to change
without requiring any code changes.




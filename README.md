# TagFind
Find specific tag information within the repository's features files.
It is useful for the situations when it is required to provide Capybara test
statistics.

*Requirements*
 - Repository should have `features` directory in its Root. This directory should
 contain all the feature files with the corresponding test scenarios.
 - It is important to properly mark either each test case or the whole feature file
 with applicable tag (i.e. @ui)
 
*Usage*

1. Clone repository: https://github.com/fruser/tagfind and open the directory
1. Install Mini Conda environment for Python v3.5 from the following URL:
 http://conda.pydata.org/miniconda.html
2. Import Python environment from the `environment.yml` file:
`conda env create -f environment.yml`
3. Activate Python environment:
`source activate <environment_name>`
4. Run the script:
`python tagfind/tagfind.py [-h] [-o OUTPUT] [-d DOMAIN] -r REPO`
    _Required arguments:_
      -r REPO, --repo REPO  Enter GitHub repository URL
      
    _Optional arguments:_
      -h, --help            show this help message and exit
      -o OUTPUT, --output OUTPUT
                            Provide output directory for storing zip archives.
                            Default: Temp OS directory
      -d DOMAIN, --domain DOMAIN
                            Enter GitHub custom domain
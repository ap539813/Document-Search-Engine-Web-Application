import os
import logging

anaconda = input('Do you have anaconda installed ?')

if (anaconda.lower() == 'yes') or (anaconda.lower() == 'y'):
    os.system('conda create --name doc_search_env python=3.9')
    os.system('conda activate doc_search_env')
    os.system('pip install -r requirements.txt')

else:
    # logging.error('install anaconda first, It will be easy to install the environment in that case')
    print("\033[91m {}\033[00m".format("install anaconda first, It will be easy to install thnoe environment in that case  \n"))
    print("\033[92m {}\033[00m".format("After installing Anaconda run this script again!!  \n"))
    # logging.info('After installing Anaconda run this script again!!')

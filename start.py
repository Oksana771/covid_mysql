from lib.settings import *
from lib.Covid import GetCovid19

covid_19_info = GetCovid19(HOSTNAME, USERNAME, PASSWORD, COVID_19)
covid_19_info.menu()
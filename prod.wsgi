import os
import sys
sys.stdout = sys.stderr
import site

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('/home/yijia/envs/house/lib/python2.7/site-packages')

# Add the app's directory to the PYTHONPATH
sys.path.append('/home/yijia/workspace/house')

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

# Activate your virtual env
activate_env=os.path.expanduser("/home/yijia/envs/house/bin/activate_this.py")
execfile(activate_env, dict(__file__=activate_env))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

application = get_wsgi_application()

#!/usr/bin/python3

from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


from api.v1.views.index import *
from api.v1.views.states import *
<<<<<<< HEAD
from api.v1.views.amenities import *
from api.v1.views.places import *
from api.v1.views.reviews import *
from api.v1.views.users import *
from api.v1.views.cities import *
=======
<<<<<<< HEAD
=======
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.reviews import *
>>>>>>> 546c64ecf5baa2309a0ea7d2e3d797f7956414dc
>>>>>>> 3ffee77a1417f6af57eaae5bbeb0a58abf9f284d

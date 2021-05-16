from flask_restplus import Namespace

namespace = Namespace('security', description='Application security')

from . import account, auth, register, resets

# -*- coding: utf-8 -*-
"""Setup the weeehire application"""
from __future__ import print_function, unicode_literals
import transaction
from weeehire import model
from datetime import datetime
from os import environ as env


def bootstrap(command, conf, vars):
    """Place any commands to setup weeehire here"""

    # <websetup.bootstrap.before.auth
    from sqlalchemy.exc import IntegrityError
    try:
        a = model.User()
        a.user_name = env['ADMIN_USERNAME']
        a.display_name = env['ADMIN_USERNAME']
        a.email_address = env['ADMIN_EMAIL']
        a.password = env['ADMIN_PASS']
        a.created = datetime.now()

        model.DBSession.add(a)

        g = model.Group()
        g.group_name = 'managers'
        g.display_name = 'Managers Group'

        g.users.append(a)

        model.DBSession.add(g)

        p = model.Permission()
        p.permission_name = 'manage'
        p.description = 'This permission gives an administrative right'
        p.groups.append(g)

        model.DBSession.add(p)

        a = model.User()
        a.user_name = 'steino_caro'
        a.display_name = 'steino_caro'
        a.email_address = 'stefano.mendola@gmail.com'
        a.first_name = 'Stefano'
        a.last_name = 'Mendola'
        a.study_course = 'INGEGNERIA INFORMATICA'
        a.year = '3'
        a.interest = 'Programmazione'
        a.letter = 'asd'
        a.compiled = datetime.now()
        a.password = 'asd'
        a.created = datetime.now()

        model.DBSession.add(a)

        model.DBSession.flush()
        transaction.commit()
    except IntegrityError:
        print('Warning, there was a problem adding your auth data, '
              'it may have already been added:')
        import traceback
        print(traceback.format_exc())
        transaction.abort()
        print('Continuing with bootstrapping...')

    # <websetup.bootstrap.after.auth>

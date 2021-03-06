# -*- coding: utf-8 -*-
"""Soviet controller module"""

from tg import expose, flash, redirect, abort
from tg import predicates, request
from tgext.mailer import get_mailer, Message
from weeehire.lib.base import BaseController
from weeehire.model import DBSession, User, Recruiter


class SovietController(BaseController):
    allow_only = predicates.has_permission('manage')
    
    @expose('weeehire.templates.soviet')
    def index(self, filter=None, **kw):
        if filter == 'awaiting':
            users = DBSession.query(User).filter(User.user_id != 1).filter_by(status=None).all()
        elif filter == 'approved':
            users = DBSession.query(User).filter(User.user_id != 1) \
                .filter_by(status=True).filter_by(published=False).all()
        elif filter == 'rejected':
            users = DBSession.query(User).filter(User.user_id != 1).filter_by(status=False).all()
        elif filter == 'contact':
            users = DBSession.query(User).filter(User.user_id != 1) \
                .filter_by(status=True) \
                .filter_by(published=True) \
                .filter_by(recruiter=None).all()
        elif filter == 'done':
            users = DBSession.query(User).filter(User.user_id != 1) \
                .filter_by(status=True) \
                .filter_by(published=True) \
                .filter(User.recruiter).all()
        else:
            users = DBSession.query(User).filter(User.user_id != 1).all()
        return dict(page='soviet-index', users=users)

    @expose('weeehire.templates.soviet-read')
    def read(self, uid, **kw):
        if not uid:
            abort(404)
        user = User.by_user_id(uid)
        if not user:
            abort(404)
        return dict(page='soviet-read', user=user)

    @expose()
    def accept(self, uid, **kw):
        if not uid:
            abort(404)
        user = User.by_user_id(uid)
        if not user:
            abort(404)
        user.status = True
        return redirect('/soviet')

    @expose()
    def reject(self, uid, **kw):
        if not uid:
            abort(404)
        user = User.by_user_id(uid)
        if not user:
            abort(404)
        user.status = False
        return redirect('/soviet')

    @expose()
    def clear(self, uid, **kw):
        if not uid:
            abort(404)
        user = User.by_user_id(uid)
        if not user:
            abort(404)
        user.status = None
        return redirect('/soviet')

    @expose()
    def publish(self, **kw):
        approved_users = DBSession.query(User).filter_by(published=False).filter_by(status=True).all()
        rejected_users = DBSession.query(User).filter_by(published=False).filter_by(status=False).all()

        for i in range(len(approved_users)):
            approved_users[i].published = True

        for i in range(len(rejected_users)):
            rejected_users[i].published = True

        flash('Risultati pubblicati correttamente')
        return redirect('/soviet')

    @expose('weeehire.templates.soviet-contact')
    def contact(self, uid):
        if not uid:
            abort(404)
        user = User.by_user_id(uid)
        if not user:
            abort(404)

        recruiters = DBSession.query(Recruiter).all()

        return dict(page='soviet-contact', user=user, recruiters=recruiters)

    @expose()
    def send_email(self, **kw):
        user = User.by_user_id(kw['user_id'])
        if user.recruiter:  # This line avoids us to pestarci i piedi a vicenda asd
            abort(403)
        recruiter = Recruiter.by_telegram(kw['recruiter'])
        user.recruiter_id = recruiter.id
        noreply_email = User.by_user_id(1).email_address
        mailer = get_mailer(request)
        message = Message(subject="Reclutamento WEEE Open",
                          sender=noreply_email,
                          recipients=[user.email_address],
                          body=kw['mail']
                          )
        mailer.send(message)
        flash("Messaggio inviato")
        return redirect('/soviet')

    @expose()
    def delete(self, uid, **kw):
        if not uid:
            abort(404)
        user = User.by_user_id(uid)
        if not user:
            abort(404)
        DBSession.delete(user)
        return redirect('/soviet')

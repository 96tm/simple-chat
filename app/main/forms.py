from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import Required, Length
from ..models import Message


class MessageForm(FlaskForm):
    kw = {'class': 'message-field',
          'cols': '38',
          'minlength': '1',
          'maxlength': '1000',
          'autofocus': 'autofocus',
          'placeholder': 'your message...'}
    message_field = TextAreaField(validators=[Length(1, 1000)],
                                  render_kw=kw)


class UserSearchForm(FlaskForm):
    kw = {'class': 'user-search form-control',
          'type': 'search',
          'maxlength': '64',
          'placeholder': 'search...'}
    search_field = StringField(validators=[Length(1, 1000)],
                               render_kw=kw)


class ChatSearchForm(FlaskForm):
    kw = {'class': 'chat-search form-control',
          'type': 'search',
          'maxlength': '64',
          'placeholder': 'search...'}
    search_field = StringField(validators=[Length(1, 1000)],
                                render_kw=kw)

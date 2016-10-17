import logging

import jinja2

from community_share.models.user import User
from community_share.models.secret import create_secret, lookup_secret
from community_share import mail, config, store, time_format

logger = logging.getLogger(__name__)


def append_conversation_link(content, conversation):
    conversation_url = '{0}/#/conversation/{1}'.format(config.BASEURL, conversation.id)
    content = content.replace('\n', '<br/>\n')
    content = '{content}<br/><br/>\nThe email is part of a Community Share Conversation.  Simply reply to this email to continue the conversation.  If you are ready to schedule an event or to view the entire conversation go to <a href={url}>{url}</a>'.format(
        content=content,
        url=conversation_url,
    )
    return content


CONFIRM_EMAIL_REMINDER_TEMPLATE = '''<p>
You recently signed up for an account with CommunityShare, a network connecting teachers and community partners. Please click on the following link so we can activate your account. Thank you!
<p>

<p>
<a href={url}>{url}</a>.
<p>

'''

EVENT_REMINDER_TEMPLATE = jinja2.Template(
    '''<p>You have a share soon with {{other_user.name | e}}.  The share details are:</p>

Title: {{share.title | e}}<br/>
Description: {{share.description | e}}<br/>
<br/>
Educator: {{share.educator.name | e}}<br/>
Community Partner: {{share.community_partner.name | e}}<br/>
<p>
{{eventdetails}}
</p>
Go to <a href={{url}}>{{url}}</a> for more details.
''',
)

ACCOUNT_DELETION_TEMPLATE = jinja2.Template(
    '''You have requested to delete your Community Share account.
If you did not make this request, or it was done accidentally please contact an administrator
at <a href="mailto:{{admin_email}}">{{admin_email}}</a>.
''',
)

PARTNER_DELETION_TEMPLATE = jinja2.Template(
    '''<p>{{canceled_user.name | e}} has just deleted their community share account.
You have been notified because you have one upcoming event planned with them.</p>

<p>To view your conversation with {{canceled_user.name | e}} go to <a href={{url}}>{{url}}</a>.</p>
''',
)

SHARE_DELETION_TEMPLATE = jinja2.Template(
    '''<p>{{editer.name | e}} has canceled the share '{{share.title | e}}'</p>.

<p>To view the conversation go to <a href={{url}}>{{url}}</a></p>.
''',
)

SHARE_CONFIRMATION_TEMPLATE = jinja2.Template(
    '''<p>{{editer.name | e}} has confirmed the details of a share.</p>

<p>To view the share details go to <a href={{url}}>{{url}}</a>.</p>
''',
)

NOTIFY_SHARE_CREATION_TEMPLATE = jinja2.Template(
    '''<p>A share has been created.</p>
Title: {{share.title | e}}<br/>
Description: {{share.description | e}}<br/>
<br/>
Educator: {{share.educator.name | e}}<br/>
Community Partner: {{share.community_partner.name | e}}<br/>

<p>{{eventdetails}}</p>

View the details at <a href={{url}}>{{url}}</a>.
''',
)

SHARE_CREATION_TEMPLATE = jinja2.Template(
    '''<p>{{editer.name | e}} has proposed a share with you.  The details are:</p>

Title: {{share.title | e}}<br/>
Description: {{share.description | e}}<br/>
<br/>
Educator: {{share.educator.name | e}}<br/>
Community Partner: {{share.community_partner.name | e}}<br/>

<p>{{eventdetails}}</p>

To confirm this suggestion please go to <a href={{url}}>{{url}}</a> and click the confirm share button.
''',
)

SHARE_EDIT_TEMPLATE = jinja2.Template(
    '''<p>{{editer.name | e}} has edited the details of a share which you are involved in or have been invited to.  The new share details suggested are:</p>

Title: {{share.title | e}}<br/>
Description: {{share.description | e}}<br/>

Educator: {{share.educator.name | e}}<br/>
Community Partner: {{share.community_partner.name | e}}<br/>

<p>{{eventdetails}}</p>

To confirm these changes please go to <a href={{url}}>{{url}}</a> and click the confirm share button.<br/>
''',
)

EVENT_EDIT_TEMPLATE = jinja2.Template(
    '''Location: {{event.location| e}}<br/>
Starting: {{event.formatted_datetime_start}}<br/>
Stopping: {{event.formatted_datetime_stop}}<br/>
''',
)

REVIEW_REMINDER_TEMPLATE = jinja2.Template(
    '''<p>You recently participated in a Community Share.</p>

<p>Please go to <a href={{url}}>{{url}}</a> to leave a review and feedback.</p>

Title: {{share.title | e}}<br/>
Description: {{share.description | e}}<br/>
<br/>
Educator: {{share.educator.name | e}}<br/>
Community Partner: {{share.community_partner.name | e}}<br/>

<p>{{eventdetails}}</p>
''',
)


def send_review_reminder_message(user, event):
    subject = 'Review Community Share Event'
    url = event.get_url()
    event_details = EVENT_EDIT_TEMPLATE.render(event=event)
    content = REVIEW_REMINDER_TEMPLATE.render(
        url=url,
        share=event.share,
        eventdetails=event_details,
    )
    to_address = user.confirmed_email
    from_address = config.DONOTREPLY_EMAIL_ADDRESS
    if not to_address:
        error_message = '{0} is not a confirmed email address'.format(receiver.email)
    else:
        email = mail.Email(
            from_address=from_address,
            to_address=to_address,
            subject=subject,
            content=content,
            new_content=content
        )
        error_message = mail.get_mailer().send(email)
    return error_message


def send_partner_deletion_message(user, canceled_user, conversation):
    subject = 'Community Share Account Deletion'
    url = conversation.get_url()
    content = PARTNER_DELETION_TEMPLATE.render(canceled_user=canceled_user, url=url)
    if user is None:
        error_message = '{0} other user in share does not exist'
    else:
        to_address = user.confirmed_email
        from_address = config.DONOTREPLY_EMAIL_ADDRESS
        if not to_address:
            error_message = '{0} is not a confirmed email address'.format(receiver.email)
        else:
            email = mail.Email(
                from_address=from_address,
                to_address=to_address,
                subject=subject,
                content=content,
                new_content=content
            )
            error_message = mail.get_mailer().send(email)
    return error_message


def send_account_deletion_message(user):
    admin_email = config.SUPPORT_EMAIL_ADDRESS
    subject = 'Community Share Account Deletion'
    content = ACCOUNT_DELETION_TEMPLATE.render(admin_email=admin_email)
    to_address = user.confirmed_email
    from_address = config.SUPPORT_EMAIL_ADDRESS
    if not to_address:
        error_message = '{0} is not a confirmed email address'.format(user.email)
    else:
        email = mail.Email(
            from_address=from_address,
            to_address=to_address,
            subject=subject,
            content=content,
            new_content=content
        )
        error_message = mail.get_mailer().send(email)
    return error_message


def send_event_reminder_message(event):
    share = event.share
    receivers = [share.educator, share.community_partner]
    other_users = [share.community_partner, share.educator]
    from_address = config.DONOTREPLY_EMAIL_ADDRESS
    event_details = EVENT_EDIT_TEMPLATE.render(event=event)
    url = share.conversation.get_url()
    subject = 'Reminder for Share on {}'.format(time_format.to_pretty(event.datetime_start))
    error_messages = []
    for receiver, other_user in zip(receivers, other_users):
        content = EVENT_REMINDER_TEMPLATE.render(
            share=share,
            eventdetails=event_details,
            url=url,
            other_user=other_user,
        )
        to_address = receiver.confirmed_email
        if not to_address:
            logger.warning('Will not send event reminder to unconfirmed email address.')
            error_message = '{0} is not a confirmed email address'.format(receiver.email)
        else:
            email = mail.Email(
                from_address=from_address,
                to_address=to_address,
                subject=subject,
                content=content,
                new_content=content
            )
            error_message = mail.get_mailer().send(email)
        error_messages.append(error_message)
    combined_error_message = ', '.join([e for e in error_messages if e is not None])
    return combined_error_message


def send_notify_share_creation(share, requester):
    to_address = config.NOTIFY_EMAIL_ADDRESS
    from_address = config.DONOTREPLY_EMAIL_ADDRESS
    event_details = ''.join([EVENT_EDIT_TEMPLATE.render(event=event) for event in share.events])
    url = share.conversation.get_url()
    subject = 'Share Created: {0}'.format(share.title)
    content = NOTIFY_SHARE_CREATION_TEMPLATE.render(
        share=share,
        eventdetails=event_details,
        url=url,
    )
    if not to_address:
        error_message = 'Recipient has not confirmed their email address'
    else:
        email = mail.Email(
            from_address=from_address,
            to_address=to_address,
            subject=subject,
            content=content,
            new_content=content
        )
        error_message = mail.get_mailer().send(email)
    return error_message


def send_share_message(
        share,
        editer,
        new_share=False,
        is_confirmation=False,
        is_delete=False,
):
    receivers = [share.conversation.userA, share.conversation.userB]
    receivers = [r for r in receivers if (editer.id != r.id)]
    from_address = config.DONOTREPLY_EMAIL_ADDRESS
    event_details = ''.join([EVENT_EDIT_TEMPLATE.render(event=event) for event in share.events])
    url = share.conversation.get_url()
    if is_confirmation:
        subject = 'Share Details Confirmed: {0}'.format(share.title)
        content = SHARE_CONFIRMATION_TEMPLATE.render(
            share=share,
            eventdetails=event_details,
            url=url,
            editer=editer,
        )
    elif is_delete:
        subject = 'Share Canceled: {0}'.format(share.title)
        content = SHARE_DELETION_TEMPLATE.render(
            share=share,
            eventdetails=event_details,
            url=url,
            editer=editer,
        )
    elif new_share:
        subject = 'Share Details Suggested: {0}'.format(share.title)
        content = SHARE_CREATION_TEMPLATE.render(
            share=share,
            eventdetails=event_details,
            url=url,
            editer=editer,
        )
    else:
        subject = 'Share Details Edited: {0}'.format(share.title)
        content = SHARE_EDIT_TEMPLATE.render(
            share=share,
            eventdetails=event_details,
            url=url,
            editer=editer,
        )
    error_messages = []
    for receiver in receivers:
        to_address = receiver.confirmed_email
        if not to_address:
            error_message = '{0} is not a confirmed email address'.format(receiver.email)
        else:
            email = mail.Email(
                from_address=from_address,
                to_address=to_address,
                subject=subject,
                content=content,
                new_content=content
            )
            error_message = mail.get_mailer().send(email)
        error_messages.append(error_message)
    combined_error_message = ', '.join([e for e in error_messages if e is not None])
    return combined_error_message


def send_conversation_message(message):
    logger.debug('send_conversation_email begins')
    error_message = ''
    sender_user = message.sender_user
    conversation = message.get_conversation()
    subject = None
    subject = conversation.title
    from_address = message.generate_from_address()
    to_address = message.receiver_user().confirmed_email
    conversation_url = '{0}/api/conversation/{1}'.format(config.BASEURL, conversation.id)
    content = append_conversation_link(message.content, conversation)
    logger.info('Sending conversation message with content - {}'.format(content))
    if not to_address:
        error_message = 'Recipient has not confirmed their email address'
    else:
        email = mail.Email(
            from_address=from_address,
            to_address=to_address,
            subject=subject,
            content=content,
            new_content=content,
        )
        error_message = mail.get_mailer().send(email)
    return error_message


def request_signup_email_confirmation(user, template=None, subject=None):
    secret_info = {
        'userId': user.id,
        'email': user.email,
        'action': 'email_confirmation',
    }
    hours_duration = 24 * 14
    secret = create_secret(secret_info, hours_duration)
    url = '{BASEURL}/#/confirmemail?key={secret_key}'.format(
        BASEURL=config.BASEURL,
        secret_key=secret.key,
    )
    if template is None:
        template = '''<p>A community share account has been created and attached to this email address.<p>

        <p>To confirm that you created the account, please click on the following link.</p>

        <p><a href={url}>{url}</a></p>

        <p>If you did not create this account, simply ignore this email.</p>
'''
    content = template.format(url=url)
    if subject is None:
        subject = 'CommunityShare Account Creation'
    email = mail.Email(
        from_address=config.DONOTREPLY_EMAIL_ADDRESS,
        to_address=user.email,
        subject=subject,
        content=content,
        new_content=content
    )
    error_message = mail.get_mailer().send(email)
    return error_message


def request_password_reset(user):
    secret_info = {
        'userId': user.id,
        'action': 'password_reset',
    }
    hours_duration = 48
    secret = create_secret(secret_info, hours_duration)
    url = '{BASEURL}/#/resetpassword?key={secret_key}'.format(
        BASEURL=config.BASEURL,
        secret_key=secret.key,
    )
    content = '''<p>We received a request to reset your password for CommunityShare.</p>
    
<p>To reset your password please click on the following link and follow the instructions.</p>
    
<a href={url}>{url}</a>
    
<p>If you cannot click on the link copy it into the addressbar of your browser.</p>
'''
    content = content.format(url=url)
    email = mail.Email(
        from_address=config.DONOTREPLY_EMAIL_ADDRESS,
        to_address=user.email,
        subject='CommunityShare Password Reset Request',
        content=content,
        new_content=content,
    )
    error_message = mail.get_mailer().send(email)
    return error_message


def process_password_reset(secret_key, new_password):
    user = None
    error_messages = User.is_password_valid(new_password)
    if not error_messages:
        secret = lookup_secret(secret_key)
        error_message = ''
        if secret is not None:
            secret_info = secret.get_info()
            userId = secret_info.get('userId', None)
            action = secret_info.get('action', None)
            if action == 'password_reset' and userId is not None:
                user = store.session.query(User).filter_by(id=userId).first()
                if user is not None:
                    error_messages += user.set_password(new_password)
                    if not error_messages:
                        secret.used = True
                        store.session.add(user)
                        store.session.add(secret)
                        store.session.commit()
        else:
            error_messages.append('Authorization for this action is invalid or expired.')
    return (user, error_messages)


def process_confirm_email(secret_key):
    error_messages = []
    user = None
    secret = lookup_secret(secret_key)
    if secret is not None:
        secret_info = secret.get_info()
        userId = secret_info.get('userId', None)
        action = secret_info.get('action', None)
        if action == 'email_confirmation' and userId is not None:
            user = store.session.query(User).filter_by(id=userId).first()
            if user is not None:
                user.email_confirmed = True
                secret.used = True
                store.session.add(user)
                store.session.add(secret)
                store.session.commit()
            else:
                error_messages.append('Authorization is for an unknown user.')
        else:
            error_mesage('Authorization is not valid for this action.')
    else:
        error_messages.append('Authorization for this action is invalid or expired.')
    return (user, error_messages)

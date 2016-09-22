from errbot.utils import format_timedelta
from datetime import datetime
from errbot import botcmd, BotPlugin
import logging
log = logging.getLogger(__name__)

class StalkerBot(BotPlugin):

    def activate(self):
        super(StalkerBot, self).activate()
        if 'presence' not in self:
            self['presence'] = {}

    def callback_message(self, mess):
        message = mess.body
        if not message:
            return

        username = mess.frm.node
        log.debug("Recording presence of %s", username)

        presence = self['presence']
        presence[username] = {
            'time': datetime.now(),
            'msg': message,
        }
        self['presence'] = presence

    @botcmd
    def seen(self, mess, args):
        """ find out when someone last said something """
        requester = mess.frm.node
        username = str(args)
        presence = self['presence']

        log.debug('{0} looking for {1}'.format(requester, username))

        if username == requester:
            return 'I can see you now'

        if username == '':
            return 'Hmm... seen whom?'

        try:
            last_seen = presence[username]['time']
            last_msg = presence[username]['msg']
            return 'I last saw {0} {1} ago (on {2}) which said "{3}"'.format(
                username,
                format_timedelta(datetime.now() - last_seen),
                datetime.strftime(last_seen, '%A, %b %d at %H:%M'),
                last_msg
            )
        except KeyError:
            return 'I have no record of %s' % args

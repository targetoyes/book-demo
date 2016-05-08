#!/usr/bin/env  python
# -*- coding: utf-8 -*-
from optparse import OptionParser
import os
import re
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


sender = dict(
    loginname='jie.gan@baozun.com',
    password='targetoyes123',
    use='smtp.qq.com'
)


if sys.version_info[0] == 2:
    from email import Encoders as email_encoders
elif sys.version_info[0] == 3:
    from email import encoders as email_encoders
    basestring = str

    def unicode(_str, _charset):
        return str(_str.encode(_charset), _charset)
else:
    raise RuntimeError('Unsupported Python version: %d.%d.%d' % (
        sys.version_info[0], sys.version_info[1], sys.version_info[2]
    ))

from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.audio import MIMEAudio
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
import mimetypes
import os
import re


"""
envelopes.connstack
===================

This module implements SMTP connection stack management.
"""

from contextlib import contextmanager
"""
    werkzeug.local
    ~~~~~~~~~~~~~~

    This module implements context-local objects.

    :copyright: (c) 2011 by the Werkzeug Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""
# Since each thread has its own greenlet we can just use those as identifiers
# for the context.  If greenlets are not available we fall back to the
# current thread ident.

import smtplib
import socket

TimeoutException = socket.timeout

__all__ = ['SMTP', 'GMailSMTP', 'SendGridSMTP', 'MailcatcherSMTP',
           'TimeoutException']


class SMTP(object):
    """Wrapper around :py:class:`smtplib.SMTP` class."""

    def __init__(self, host=None, port=25, login=None, password=None,
                 tls=False, timeout=None):
        self._conn = None
        self._host = host
        self._port = port
        self._login = login
        self._password = password
        self._tls = tls
        self._timeout = timeout

    @property
    def is_connected(self):
        """Returns *True* if the SMTP connection is initialized and
        connected. Otherwise returns *False*"""
        try:
            self._conn.noop()
        except (AttributeError, smtplib.SMTPServerDisconnected):
            return False
        else:
            return True

    def _connect(self, replace_current=False):
        if self._conn is None or replace_current:
            try:
                self._conn.quit()
            except (AttributeError, smtplib.SMTPServerDisconnected):
                pass

            if self._timeout:
                self._conn = smtplib.SMTP(self._host, self._port,
                                          timeout=self._timeout)
            else:
                self._conn = smtplib.SMTP(self._host, self._port)

        if self._tls:
            self._conn.starttls()

        if self._login:
            self._conn.login(self._login, self._password or '')

    def send(self, envelope):
        """Sends an *envelope*."""
        if not self.is_connected:
            self._connect()

        msg = envelope.to_mime_message()
        to_addrs = [envelope._addrs_to_header([addr]) for addr in envelope._to + envelope._cc + envelope._bcc]

        return self._conn.sendmail(msg['From'], to_addrs, msg.as_string())

try:
    from greenlet import getcurrent as get_ident
except ImportError:  # noqa
    try:
        from thread import get_ident  # noqa
    except ImportError:  # noqa
        from _thread import get_ident  # noqa


def release_local(local):
    """Releases the contents of the local for the current context.
    This makes it possible to use locals without a manager.

    Example::

        >>> loc = Local()
        >>> loc.foo = 42
        >>> release_local(loc)
        >>> hasattr(loc, 'foo')
        False

    With this function one can release :class:`Local` objects as well
    as :class:`StackLocal` objects.  However it is not possible to
    release data held by proxies that way, one always has to retain
    a reference to the underlying local object in order to be able
    to release it.

    .. versionadded:: 0.6.1
    """
    local.__release_local__()


class Local(object):
    __slots__ = ('__storage__', '__ident_func__')

    def __init__(self):
        object.__setattr__(self, '__storage__', {})
        object.__setattr__(self, '__ident_func__', get_ident)

    def __iter__(self):
        return iter(self.__storage__.items())

    def __call__(self, proxy):
        """Create a proxy for a name."""
        return LocalProxy(self, proxy)

    def __release_local__(self):
        self.__storage__.pop(self.__ident_func__(), None)

    def __getattr__(self, name):
        try:
            return self.__storage__[self.__ident_func__()][name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        ident = self.__ident_func__()
        storage = self.__storage__
        try:
            storage[ident][name] = value
        except KeyError:
            storage[ident] = {name: value}

    def __delattr__(self, name):
        try:
            del self.__storage__[self.__ident_func__()][name]
        except KeyError:
            raise AttributeError(name)


class LocalStack(object):
    """This class works similar to a :class:`Local` but keeps a stack
    of objects instead.  This is best explained with an example::

        >>> ls = LocalStack()
        >>> ls.push(42)
        >>> ls.top
        42
        >>> ls.push(23)
        >>> ls.top
        23
        >>> ls.pop()
        23
        >>> ls.top
        42

    They can be force released by using a :class:`LocalManager` or with
    the :func:`release_local` function but the correct way is to pop the
    item from the stack after using.  When the stack is empty it will
    no longer be bound to the current context (and as such released).

    By calling the stack without arguments it returns a proxy that resolves to
    the topmost item on the stack.

    .. versionadded:: 0.6.1
    """

    def __init__(self):
        self._local = Local()

    def __release_local__(self):
        self._local.__release_local__()

    def _get__ident_func__(self):
        return self._local.__ident_func__

    def _set__ident_func__(self, value):  # noqa
        object.__setattr__(self._local, '__ident_func__', value)
    __ident_func__ = property(_get__ident_func__, _set__ident_func__)
    del _get__ident_func__, _set__ident_func__

    def __call__(self):
        def _lookup():
            rv = self.top
            if rv is None:
                raise RuntimeError('object unbound')
            return rv
        return LocalProxy(_lookup)

    def push(self, obj):
        """Pushes a new item to the stack"""
        rv = getattr(self._local, 'stack', None)
        if rv is None:
            self._local.stack = rv = []
        rv.append(obj)
        return rv

    def pop(self):
        """Removes the topmost item from the stack, will return the
        old value or `None` if the stack was already empty.
        """
        stack = getattr(self._local, 'stack', None)
        if stack is None:
            return None
        elif len(stack) == 1:
            release_local(self._local)
            return stack[-1]
        else:
            return stack.pop()

    @property
    def top(self):
        """The topmost item on the stack.  If the stack is empty,
        `None` is returned.
        """
        try:
            return self._local.stack[-1]
        except (AttributeError, IndexError):
            return None

    def __len__(self):
        stack = getattr(self._local, 'stack', None)
        if stack is None:
            return 0
        return len(stack)


class LocalManager(object):
    """Local objects cannot manage themselves. For that you need a local
    manager.  You can pass a local manager multiple locals or add them later
    by appending them to `manager.locals`.  Everytime the manager cleans up
    it, will clean up all the data left in the locals for this context.

    The `ident_func` parameter can be added to override the default ident
    function for the wrapped locals.

    .. versionchanged:: 0.6.1
       Instead of a manager the :func:`release_local` function can be used
       as well.

    .. versionchanged:: 0.7
       `ident_func` was added.
    """

    def __init__(self, locals=None, ident_func=None):
        if locals is None:
            self.locals = []
        elif isinstance(locals, Local):
            self.locals = [locals]
        else:
            self.locals = list(locals)
        if ident_func is not None:
            self.ident_func = ident_func
            for local in self.locals:
                object.__setattr__(local, '__ident_func__', ident_func)
        else:
            self.ident_func = get_ident

    def get_ident(self):
        """Return the context identifier the local objects use internally for
        this context.  You cannot override this method to change the behavior
        but use it to link other context local objects (such as SQLAlchemy's
        scoped sessions) to the Werkzeug locals.

        .. versionchanged:: 0.7
           Yu can pass a different ident function to the local manager that
           will then be propagated to all the locals passed to the
           constructor.
        """
        return self.ident_func()

    def cleanup(self):
        """Manually clean up the data in the locals for this context.  Call
        this at the end of the request or use `make_middleware()`.
        """
        for local in self.locals:
            release_local(local)

    def __repr__(self):
        return '<%s storages: %d>' % (
            self.__class__.__name__,
            len(self.locals)
        )


class LocalProxy(object):
    """Acts as a proxy for a werkzeug local.  Forwards all operations to
    a proxied object.  The only operations not supported for forwarding
    are right handed operands and any kind of assignment.

    Example usage::

        from werkzeug.local import Local
        l = Local()

        # these are proxies
        request = l('request')
        user = l('user')


        from werkzeug.local import LocalStack
        _response_local = LocalStack()

        # this is a proxy
        response = _response_local()

    Whenever something is bound to l.user / l.request the proxy objects
    will forward all operations.  If no object is bound a :exc:`RuntimeError`
    will be raised.

    To create proxies to :class:`Local` or :class:`LocalStack` objects,
    call the object as shown above.  If you want to have a proxy to an
    object looked up by a function, you can (as of Werkzeug 0.6.1) pass
    a function to the :class:`LocalProxy` constructor::

        session = LocalProxy(lambda: get_current_request().session)

    .. versionchanged:: 0.6.1
       The class can be instanciated with a callable as well now.
    """
    __slots__ = ('__local', '__dict__', '__name__')

    def __init__(self, local, name=None):
        object.__setattr__(self, '_LocalProxy__local', local)
        object.__setattr__(self, '__name__', name)

    def _get_current_object(self):
        """Return the current object.  This is useful if you want the real
        object behind the proxy at a time for performance reasons or because
        you want to pass the object into a different context.
        """
        if not hasattr(self.__local, '__release_local__'):
            return self.__local()
        try:
            return getattr(self.__local, self.__name__)
        except AttributeError:
            raise RuntimeError('no object bound to %s' % self.__name__)

    @property
    def __dict__(self):
        try:
            return self._get_current_object().__dict__
        except RuntimeError:
            raise AttributeError('__dict__')

    def __repr__(self):
        try:
            obj = self._get_current_object()
        except RuntimeError:
            return '<%s unbound>' % self.__class__.__name__
        return repr(obj)

    def __nonzero__(self):
        try:
            return bool(self._get_current_object())
        except RuntimeError:
            return False

    def __unicode__(self):
        try:
            return unicode(self._get_current_object())
        except RuntimeError:
            return repr(self)

    def __dir__(self):
        try:
            return dir(self._get_current_object())
        except RuntimeError:
            return []

    def __getattr__(self, name):
        if name == '__members__':
            return dir(self._get_current_object())
        return getattr(self._get_current_object(), name)

    def __setitem__(self, key, value):
        self._get_current_object()[key] = value

    def __delitem__(self, key):
        del self._get_current_object()[key]

    def __setslice__(self, i, j, seq):
        self._get_current_object()[i:j] = seq

    def __delslice__(self, i, j):
        del self._get_current_object()[i:j]

    __setattr__ = lambda x, n, v: setattr(x._get_current_object(), n, v)
    __delattr__ = lambda x, n: delattr(x._get_current_object(), n)
    __str__ = lambda x: str(x._get_current_object())
    __lt__ = lambda x, o: x._get_current_object() < o
    __le__ = lambda x, o: x._get_current_object() <= o
    __eq__ = lambda x, o: x._get_current_object() == o
    __ne__ = lambda x, o: x._get_current_object() != o
    __gt__ = lambda x, o: x._get_current_object() > o
    __ge__ = lambda x, o: x._get_current_object() >= o
    __cmp__ = lambda x, o: cmp(x._get_current_object(), o)
    __hash__ = lambda x: hash(x._get_current_object())
    __call__ = lambda x, *a, **kw: x._get_current_object()(*a, **kw)
    __len__ = lambda x: len(x._get_current_object())
    __getitem__ = lambda x, i: x._get_current_object()[i]
    __iter__ = lambda x: iter(x._get_current_object())
    __contains__ = lambda x, i: i in x._get_current_object()
    __getslice__ = lambda x, i, j: x._get_current_object()[i:j]
    __add__ = lambda x, o: x._get_current_object() + o
    __sub__ = lambda x, o: x._get_current_object() - o
    __mul__ = lambda x, o: x._get_current_object() * o
    __floordiv__ = lambda x, o: x._get_current_object() // o
    __mod__ = lambda x, o: x._get_current_object() % o
    __divmod__ = lambda x, o: x._get_current_object().__divmod__(o)
    __pow__ = lambda x, o: x._get_current_object() ** o
    __lshift__ = lambda x, o: x._get_current_object() << o
    __rshift__ = lambda x, o: x._get_current_object() >> o
    __and__ = lambda x, o: x._get_current_object() & o
    __xor__ = lambda x, o: x._get_current_object() ^ o
    __or__ = lambda x, o: x._get_current_object() | o
    __div__ = lambda x, o: x._get_current_object().__div__(o)
    __truediv__ = lambda x, o: x._get_current_object().__truediv__(o)
    __neg__ = lambda x: -(x._get_current_object())
    __pos__ = lambda x: +(x._get_current_object())
    __abs__ = lambda x: abs(x._get_current_object())
    __invert__ = lambda x: ~(x._get_current_object())
    __complex__ = lambda x: complex(x._get_current_object())
    __int__ = lambda x: int(x._get_current_object())
    __long__ = lambda x: long(x._get_current_object())
    __float__ = lambda x: float(x._get_current_object())
    __oct__ = lambda x: oct(x._get_current_object())
    __hex__ = lambda x: hex(x._get_current_object())
    __index__ = lambda x: x._get_current_object().__index__()
    __coerce__ = lambda x, o: x._get_current_object().__coerce__(x, o)
    __enter__ = lambda x: x._get_current_object().__enter__()
    __exit__ = lambda x, *a, **kw: x._get_current_object().__exit__(*a, **kw)


class NoSMTPConnectionException(Exception):
    pass


@contextmanager
def Connection(connection):
    push_connection(connection)
    try:
        yield
    finally:
        popped = pop_connection()
        assert popped == connection, \
            'Unexpected SMTP connection was popped off the stack. ' \
            'Check your SMTP connection setup.'


def push_connection(connection):
    """Pushes the given connection on the stack."""
    _connection_stack.push(connection)


def pop_connection():
    """Pops the topmost connection from the stack."""
    return _connection_stack.pop()


def use_connection(connection):
    """Clears the stack and uses the given connection.  Protects against mixed
    use of use_connection() and stacked connection contexts.
    """
    assert len(_connection_stack) <= 1, \
        'You should not mix Connection contexts with use_connection().'
    release_local(_connection_stack)
    push_connection(connection)


def get_current_connection():
    """Returns the current SMTP connection (i.e. the topmost on the
    connection stack).
    """
    return _connection_stack.top


def resolve_connection(connection=None):
    """Convenience function to resolve the given or the current connection.
    Raises an exception if it cannot resolve a connection now.
    """
    if connection is not None:
        return connection

    connection = get_current_connection()
    if connection is None:
        raise NoSMTPConnectionException(
            'Could not resolve an SMTP connection.')
    return connection


_connection_stack = LocalStack()

__all__ = [
    'Connection', 'get_current_connection', 'push_connection',
    'pop_connection', 'use_connection'
]

def encoded(_str, coding):
    if sys.version_info[0] == 3:
        return _str
    else:
        if isinstance(_str, unicode):
            return _str.encode(coding)
        else:
            return _str


class MessageEncodeError(Exception):
    pass

class Envelope(object):
    """
    The Envelope class.

    **Address formats**

    The following formats are supported for e-mail addresses:

    * ``"user@server.com"`` - just the e-mail address part as a string,
    * ``"Some User <user@server.com>"`` - name and e-mail address parts as a string,
    * ``("user@server.com", "Some User")`` - e-mail address and name parts as a tuple.

    Whenever you come to manipulate addresses feel free to use any (or all) of
    the formats above.

    :param to_addr: ``To`` address or list of ``To`` addresses
    :param from_addr: ``From`` address
    :param subject: message subject
    :param html_body: optional HTML part of the message
    :param text_body: optional plain text part of the message
    :param cc_addr: optional single CC address or list of CC addresses
    :param bcc_addr: optional single BCC address or list of BCC addresses
    :param headers: optional dictionary of headers
    :param charset: message charset
    """

    ADDR_FORMAT = '%s <%s>'
    ADDR_REGEXP = re.compile(r'^(.*) <([^@]+@[^@]+)>$')

    def __init__(self, to_addr=None, from_addr=None, subject=None,
                 html_body=None, text_body=None, cc_addr=None, bcc_addr=None,
                 headers=None, charset='utf-8'):
        if to_addr:
            if isinstance(to_addr, list):
                self._to = to_addr
            else:
                self._to = [to_addr]
        else:
            self._to = []

        self._from = from_addr
        self._subject = subject
        self._parts = []

        if text_body:
            self._parts.append(('text/plain', text_body, charset))

        if html_body:
            self._parts.append(('text/html', html_body, charset))

        if cc_addr:
            if isinstance(cc_addr, list):
                self._cc = cc_addr
            else:
                self._cc = [cc_addr]
        else:
            self._cc = []

        if bcc_addr:
            if isinstance(bcc_addr, list):
                self._bcc = bcc_addr
            else:
                self._bcc = [bcc_addr]
        else:
            self._bcc = []

        if headers:
            self._headers = headers
        else:
            self._headers = {}

        self._charset = charset

        self._addr_format = unicode(self.ADDR_FORMAT, charset)

    def __repr__(self):
        return u'<Envelope from="%s" to="%s" subject="%s">' % (
            self._addrs_to_header([self._from]),
            self._addrs_to_header(self._to),
            self._subject
        )

    @property
    def to_addr(self):
        """List of ``To`` addresses."""
        return self._to

    def add_to_addr(self, to_addr):
        """Adds a ``To`` address."""
        self._to.append(to_addr)

    def clear_to_addr(self):
        """Clears list of ``To`` addresses."""
        self._to = []

    @property
    def from_addr(self):
        return self._from

    @from_addr.setter
    def from_addr(self, from_addr):
        self._from = from_addr

    @property
    def cc_addr(self):
        """List of CC addresses."""
        return self._cc

    def add_cc_addr(self, cc_addr):
        """Adds a CC address."""
        self._cc.append(cc_addr)

    def clear_cc_addr(self):
        """Clears list of CC addresses."""
        self._cc = []

    @property
    def bcc_addr(self):
        """List of BCC addresses."""
        return self._bcc

    def add_bcc_addr(self, bcc_addr):
        """Adds a BCC address."""
        self._bcc.append(bcc_addr)

    def clear_bcc_addr(self):
        """Clears list of BCC addresses."""
        self._bcc = []

    @property
    def charset(self):
        """Message charset."""
        return self._charset

    @charset.setter
    def charset(self, charset):
        self._charset = charset

        self._addr_format = unicode(self.ADDR_FORMAT, charset)

    def _addr_tuple_to_addr(self, addr_tuple):
        addr = ''

        if len(addr_tuple) == 2 and addr_tuple[1]:
            addr = self._addr_format % (
                self._header(addr_tuple[1] or ''),
                addr_tuple[0] or ''
            )
        elif addr_tuple[0]:
            addr = addr_tuple[0]

        return addr

    @property
    def headers(self):
        """Dictionary of custom headers."""
        return self._headers

    def add_header(self, key, value):
        """Adds a custom header."""
        self._headers[key] = value

    def clear_headers(self):
        """Clears custom headers."""
        self._headers = {}

    def _addrs_to_header(self, addrs):
        _addrs = []
        for addr in addrs:
            if not addr:
                continue

            if isinstance(addr, basestring):
                if self._is_ascii(addr):
                    _addrs.append(self._encoded(addr))
                else:
                    # these headers need special care when encoding, see:
                    #   http://tools.ietf.org/html/rfc2047#section-8
                    # Need to break apart the name from the address if there are
                    # non-ascii chars
                    m = self.ADDR_REGEXP.match(addr)
                    if m:
                        t = (m.group(2), m.group(1))
                        _addrs.append(self._addr_tuple_to_addr(t))
                    else:
                        # What can we do? Just pass along what the user gave us and hope they did it right
                        _addrs.append(self._encoded(addr))
            elif isinstance(addr, tuple):
                _addrs.append(self._addr_tuple_to_addr(addr))
            else:
                self._raise(MessageEncodeError,
                            '%s is not a valid address' % str(addr))

        _header = ','.join(_addrs)
        return _header

    def _raise(self, exc_class, message):
        raise exc_class(self._encoded(message))

    def _header(self, _str):
        if self._is_ascii(_str):
            return _str
        return Header(_str, self._charset).encode()

    def _is_ascii(self, _str):
        return all(ord(c) < 128 for c in _str)

    def _encoded(self, _str):
        return encoded(_str, self._charset)

    def to_mime_message(self):
        """Returns the envelope as
        :py:class:`email.mime.multipar.MIMEMultipart`."""
        msg = MIMEMultipart('alternative')
        msg['Subject'] = self._header(self._subject or '')

        msg['From'] = self._encoded(self._addrs_to_header([self._from]))
        msg['To'] = self._encoded(self._addrs_to_header(self._to))

        if self._cc:
            msg['CC'] = self._addrs_to_header(self._cc)

        if self._headers:
            for key, value in self._headers.items():
                msg[key] = self._header(value)

        for part in self._parts:
            type_maj, type_min = part[0].split('/')
            if type_maj == 'text' and type_min in ('html', 'plain') and\
                        (isinstance(part[1], str) or isinstance(part[1], unicode)):
                msg.attach(MIMEText(part[1], type_min, self._charset))
            else:
                msg.attach(part[1])

        return msg

    def add_attachment(self, file_path, mimetype=None):
        """Attaches a file located at *file_path* to the envelope. If
        *mimetype* is not specified an attempt to guess it is made. If nothing
        is guessed then `application/octet-stream` is used."""
        if not mimetype:
            mimetype, _ = mimetypes.guess_type(file_path)

        if mimetype is None:
            mimetype = 'application/octet-stream'

        type_maj, type_min = mimetype.split('/')
        with open(file_path, 'rb') as fh:
            part_data = fh.read()

            part = MIMEBase(type_maj, type_min)
            part.set_payload(part_data)
            email_encoders.encode_base64(part)

            part_filename = os.path.basename(self._encoded(file_path))
            part.add_header('Content-Disposition', 'attachment; filename="%s"'
                            % part_filename)

            self._parts.append((mimetype, part))

    def send(self, *args, **kwargs):
        """Sends the envelope using a freshly created SMTP connection. *args*
        and *kwargs* are passed directly to :py:class:`envelopes.conn.SMTP`
        constructor.

        Returns a tuple of SMTP object and whatever its send method returns."""
        conn = SMTP(*args, **kwargs)
        send_result = conn.send(self)
        return conn, send_result


























class Sendy(object):
    def __init__(self, options):
        self.start = self.main(options)

    def semi_linedown(self, text):
        text = text.replace('\\n', '\n')
        return text

    def add_attech(self, files):
        for i in files.split(','):
            if os.path.isfile(i):
                self.envelope.add_attachment(i)
            else:
                print 'no such file named ' + i
                sys.exit(1)

    def multi_addr(self, dest):
        if re.search(',', str(dest)):
            dest = [i  for i in dest.split(',')]
        return dest

    def init_sender(self, options):
        envelope = Envelope(
                from_addr=(unicode(sender['loginname'], "utf-8")),
                to_addr=(options.dest),
                cc_addr=(options.copy_dest),
                subject=(options.subject),
                text_body=(options.text)
                )
        return envelope

    def deal_with_empty(self, args):
        try:
            args
        except NameError:
            args = ''
        return args


    def main(self, options):
        options.subject = self.deal_with_empty(options.subject)
        if options.subject:
            options.subject = self.semi_linedown(options.subject)

        options.dest = self.deal_with_empty(options.dest)
        if options.dest:
            options.dest = self.multi_addr(options.dest)

        options.copy_dest = self.deal_with_empty(options.copy_dest)
        if options.copy_dest:
            options.copy_dest = self.multi_addr(options.copy_dest)

        options.text = self.deal_with_empty(options.text)
        if options.text:
            options.text = self.semi_linedown(options.text)
        for i in xrange(3):
            try:
                self.envelope = self.init_sender(options)
                break
            except:
                if i == 2:
                    print "has tried 3 times,but send mail failed"
                pass
        if options.files:
            self.add_attech(options.files)
        self.envelope.send(sender['use'], login=sender['loginname'],
                        password=sender['password'], tls=True)


# Send the envelope using an ad-hoc connection...
if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-d", "--dest", dest="dest",
            help = "define the address where you want to send")
    parser.add_option("-s", "--subject", dest="subject",
            help = "define the subject in the envelope")
    parser.add_option("-t", "--text", dest="text",
            help = "define the text in the mail body")
    parser.add_option("-c", "--copy", dest="copy_dest",
            help = "define the copy where you want to send")
    parser.add_option("-f", "--files", dest="files",
            help = "define the attachment where you want to send")
    (options, args) = parser.parse_args()
    Sendy(options)


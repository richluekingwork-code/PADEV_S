"""Email client auto-setup for @padev.org mailboxes.

The mailboxes live on the cPanel host, but padev.org itself now points at this
website, so the host's own auto-setup (which answers "server: padev.org") sends
Outlook, Thunderbird and phones to a server that does not accept mail. These views
answer the same requests with the real mail server from settings instead.
"""
import re
from xml.sax.saxutils import escape

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Paths CanonicalHostMiddleware must not redirect: Outlook does not follow a
# redirect from the bare domain for these requests.
AUTOCONFIG_PATHS = (
    '/autodiscover/autodiscover.xml',
    '/mail/config-v1.1.xml',
    '/.well-known/autoconfig/mail/config-v1.1.xml',
)

_EMAIL_IN_REQUEST = re.compile(r'<EMailAddress>\s*([^<\s]+)\s*</EMailAddress>', re.I)


def _xml(body):
    return HttpResponse('<?xml version="1.0" encoding="utf-8"?>\n' + body, content_type='application/xml')


@csrf_exempt
def outlook_autodiscover(request):
    """Outlook's POX autodiscover (POST from Outlook, GET tolerated)."""
    match = _EMAIL_IN_REQUEST.search(request.body.decode('utf-8', 'ignore')) if request.body else None
    email = escape(match.group(1) if match else request.GET.get('email', ''))
    host = escape(settings.MAIL_SERVER_HOSTNAME)
    protocols = ''.join(
        f"""
      <Protocol>
        <Type>{kind}</Type>
        <Server>{host}</Server>
        <Port>{port}</Port>
        <DomainRequired>off</DomainRequired>
        <SPA>off</SPA>
        <SSL>on</SSL>
        <AuthRequired>on</AuthRequired>
        <LoginName>{email}</LoginName>
      </Protocol>"""
        for kind, port in (('IMAP', 993), ('SMTP', 465))
    )
    return _xml(f"""<Autodiscover xmlns="http://schemas.microsoft.com/exchange/autodiscover/responseschema/2006">
  <Response xmlns="http://schemas.microsoft.com/exchange/autodiscover/outlook/responseschema/2006a">
    <User><DisplayName>{email}</DisplayName></User>
    <Account>
      <AccountType>email</AccountType>
      <Action>settings</Action>{protocols}
    </Account>
  </Response>
</Autodiscover>
""")


def thunderbird_autoconfig(request):
    """Mozilla autoconfig, also used by Apple Mail, K-9 and other mobile apps."""
    domain = escape(settings.MAIL_DOMAIN)
    host = escape(settings.MAIL_SERVER_HOSTNAME)
    return _xml(f"""<clientConfig version="1.1">
  <emailProvider id="{domain}">
    <domain>{domain}</domain>
    <displayName>{domain} mail</displayName>
    <incomingServer type="imap">
      <hostname>{host}</hostname>
      <port>993</port>
      <socketType>SSL</socketType>
      <authentication>password-cleartext</authentication>
      <username>%EMAILADDRESS%</username>
    </incomingServer>
    <outgoingServer type="smtp">
      <hostname>{host}</hostname>
      <port>465</port>
      <socketType>SSL</socketType>
      <authentication>password-cleartext</authentication>
      <username>%EMAILADDRESS%</username>
    </outgoingServer>
  </emailProvider>
</clientConfig>
""")

import json
from reportlab.lib.units import cm
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from math import ceil

# TODO: Change to english
#response = '{"Organización":"Host Europe GmbH","Nombre de host":["lvps178-77-78-196.dedicated.hosteurope.de"],"Ciudad":"Strasbourg","País":"France","Puertos abiertos":["7001","8443","443","80","52869","50000","8888","8080","8181","81","9000","37215"],"Vulnerabilidades":[{"Identificador CVE":"CVE-2022-0778","Verificado":false,"Referencias":["https://git.openssl.org/gitweb/?p=openssl.git;a=commitdiff;h=380085481c64de749a6dd25cdf0bcf4360b30f83","https://www.openssl.org/news/secadv/20220315.txt","https://git.openssl.org/gitweb/?p=openssl.git;a=commitdiff;h=a466912611aa6cbdf550cd10601390e587451246","https://git.openssl.org/gitweb/?p=openssl.git;a=commitdiff;h=3118eb64934499d93db3230748a452351d1d9a65","https://www.debian.org/security/2022/dsa-5103","https://lists.debian.org/debian-lts-announce/2022/03/msg00024.html","https://lists.debian.org/debian-lts-announce/2022/03/msg00023.html","https://security.netapp.com/advisory/ntap-20220321-0002/","https://lists.fedoraproject.org/archives/list/package-announce@lists.fedoraproject.org/message/GDB3GQVJPXJE7X5C5JN6JAA4XUDWD6E6/","https://psirt.global.sonicwall.com/vuln-detail/SNWLID-2022-0002","https://www.tenable.com/security/tns-2022-06","https://www.tenable.com/security/tns-2022-07","https://lists.fedoraproject.org/archives/list/package-announce@lists.fedoraproject.org/message/323SNN6ZX7PRJJWP2BUAFLPUAE42XWLZ/","https://lists.fedoraproject.org/archives/list/package-announce@lists.fedoraproject.org/message/W6K3PR542DXWLEFFMFIDMME4CWMHJRMG/","https://www.tenable.com/security/tns-2022-08","https://www.oracle.com/security-alerts/cpuapr2022.html","https://www.tenable.com/security/tns-2022-09","https://security.netapp.com/advisory/ntap-20220429-0005/","https://support.apple.com/kb/HT213256","https://support.apple.com/kb/HT213255","https://support.apple.com/kb/HT213257","http://seclists.org/fulldisclosure/2022/May/38","http://seclists.org/fulldisclosure/2022/May/35","http://seclists.org/fulldisclosure/2022/May/33","http://packetstormsecurity.com/files/167344/OpenSSL-1.0.2-1.1.1-3.0-BN_mod_sqrt-Infinite-Loop.html","https://cert-portal.siemens.com/productcert/pdf/ssa-712929.pdf"],"CVSS":5,"Resumen":"The BN_mod_sqrt() function, which computes a modular square root, contains a bug that can cause it to loop forever for non-prime moduli. Internally this function is used when parsing certificates that contain elliptic curve public keys in compressed form or explicit elliptic curve parameters with a base point encoded in compressed form. It is possible to trigger the infinite loop by crafting a certificate that has invalid explicit curve parameters. Since certificate parsing happens prior to verification of the certificate signature, any process that parses an externally supplied certificate may thus be subject to a denial of service attack. The infinite loop can also be reached when parsing crafted private keys as they can contain explicit elliptic curve parameters. Thus vulnerable situations include: - TLS clients consuming server certificates - TLS servers consuming client certificates - Hosting providers taking certificates or private keys from customers - Certificate authorities parsing certification requests from subscribers - Anything else which parses ASN.1 elliptic curve parameters Also any other applications that use the BN_mod_sqrt() where the attacker can control the parameter values are vulnerable to this DoS issue. In the OpenSSL 1.0.2 version the public key is not parsed during initial parsing of the certificate which makes it slightly harder to trigger the infinite loop. However any operation which requires the public key from the certificate will trigger the infinite loop. In particular the attacker can use a self-signed certificate to trigger the loop during verification of the certificate signature. This issue affects OpenSSL versions 1.0.2, 1.1.1 and 3.0. It was addressed in the releases of 1.1.1n and 3.0.2 on the 15th March 2022. Fixed in OpenSSL 3.0.2 (Affected 3.0.0,3.0.1). Fixed in OpenSSL 1.1.1n (Affected 1.1.1-1.1.1m). Fixed in OpenSSL 1.0.2zd (Affected 1.0.2-1.0.2zc)."}]}'
#data = json.loads(response)

width, height = A4
TITLE_SIZE = 18
CONTENT_SIZE = 15
MAX_DEEP = 3 * cm


class GenerateDocument:
    def __init__(self, filename, title, content):
        self.filename = filename
        self.title = title
        self.content = content
        self.cursor = {'x': width, 'y': height}
        self.canvas = Canvas(self.filename, pagesize=A4)

    def move(self, x, y):
        self.cursor['x'] = x * cm
        self.cursor['y'] = y * cm

    def movedown(self, lines):
        if (self.cursor['y'] > MAX_DEEP):
            self.cursor['y'] -= lines * cm
        else:
            # * move to page beginning
            self.movestart()
            self.canvas.showPage()

    def movestart(self):
        self.cursor['x'] = 2 * cm
        self.cursor['y'] = 26 * cm

    def drawParagraph(self, text):
        paragraph = Paragraph(text)
        paragraph.wrapOn(self.canvas, width - 5 * cm, height)
        paragraph.drawOn(self.canvas, self.cursor['x'], self.cursor['y'])
        self.lines = len(paragraph.blPara.lines)
        self.movedown(self.lines)

    def draw(self, value):
        if (isinstance(value, bool)):
            self.drawParagraph("Si" if value else "No")
        elif (isinstance(value, int) or isinstance(value, float)):
            self.drawParagraph(str(value))
        elif (isinstance(value, str)):
            self.drawParagraph(value)
        elif (isinstance(value, list)):
            for i, v in enumerate(value):
                self.draw(v)
                # if i < len(value) - 1:
                #     print("near last list element")
                #     self.movedown()
        elif (isinstance(value, dict)):
            for i, (k, v) in enumerate(value.items()):
                self.draw(k)
                # self.movedown()
                self.draw(v)
                # if i < len(value) - 1:
                #     print("near last dict element")
                #     self.movedown()

    def generate(self):
        # * add document title
        self.canvas.setFont("Helvetica-Bold", TITLE_SIZE)
        self.move(5, 27.5)
        self.draw(self.title)
        # * move to start position
        self.movestart()
        # * content writer
        for key in self.content:
            # * set each key as label
            self.canvas.setFont("Helvetica-Bold", CONTENT_SIZE)
            self.draw(key)
            # self.movedown()
            # * set value as content
            value = self.content[key]
            self.canvas.setFont("Helvetica", CONTENT_SIZE)
            self.draw(value)
            # self.movedown()
        # * save pdf
        self.canvas.save()

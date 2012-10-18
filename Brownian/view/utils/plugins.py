import subprocess
import string
import shlex

class Plugin:
    def __init__(self, command, allowedChars, insertInitialNewline=False):
        # We replace the characters we do allow with empty strings, to get a string of all the characters we don't allow.
        self.notAllowedCharMap = str(string.maketrans(allowedChars, " "*len(allowedChars)))
        self.command = shlex.split(command)
        self.insertInitialNewline = insertInitialNewline

    def run(self, values):
        sanitizedValues = []
        for value in values:
            sanitizedValues.append(str(value).translate(None, self.notAllowedCharMap))
        result = subprocess.Popen(self.command + sanitizedValues, stdout=subprocess.PIPE)
        stdout, stderr = result.communicate()
        if self.insertInitialNewline:
            stdout = "\n" + stdout
        return stdout.replace("\n", "<br>")

whois = {"displayName": "Whois Lookup",
         "plugin": Plugin("whois -h whois.cymru.com \" -p -u\"", string.letters + string.digits + ".:-_", insertInitialNewline=True)}

dns_lookup = {"displayName": "DNS Lookup",
              "plugin": Plugin("host", string.letters + string.digits + ".:-_")}

mapping = {"addr": [whois, dns_lookup],
           "string": [dns_lookup]}
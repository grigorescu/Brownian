import subprocess
import string

class Plugin:
    def __init__(self, command, allowedChars):
        # We replace the characters we do allow with empty strings, to get a string of all the characters we don't allow.
        self.notAllowedCharMap = string.maketrans(allowedChars, " "*len(allowedChars))
        self.command = command

    def run(self, values):
        sanitizedValues = []
        for value in values:
            sanitizedValues.append(str(value).translate(None, self.notAllowedCharMap))
        result = subprocess.Popen([self.command] + sanitizedValues, stdout=subprocess.PIPE)
        stdout, stderr = result.communicate()
        return stdout

whois = {"displayName": "Whois Lookup",
         "plugin": Plugin("whois", string.letters + string.digits + ".:-_")}

dns_lookup = {"displayName": "DNS Lookup",
              "plugin": Plugin("host", string.letters + string.digits + ".:-_")}

mapping = {"addr": [whois, dns_lookup],
           "string": [dns_lookup]}
from django.utils import unittest
from django.test.client import Client, RequestFactory
from django.shortcuts import render
import utils.es

class nonElasticSearchTests(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def testStatusCodes(self):
        resp1 = self.client.get('/idontexist')
        self.assertNotEqual(resp1.status_code, 200)

    def testQueryQuote(self):
        query = """ts:[* TO 1340647651797] AND !uid:"lkaub98ab" AND (host:"google.com" OR host:yahoo.com")"""
        expectedResult = 'ts:\\u005b* TO 1340647651797\\u005d AND !uid:\\"lkaub98ab\\" AND (host:\\"google.com\\" OR host:yahoo.com\\")'
        self.assertEqual(utils.es.queryEscape(query), expectedResult)

class elasticSearchTests(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def testStatusCodes(self):
        resp1 = self.client.get('/')
        resp2 = self.client.get('/*')
        resp3 = self.client.get('/uid:GjR1jckW1y6')
        resp4 = self.client.get('/uid:GjR1jckW1y6%20AND%20status:failed')
        resp5 = self.client.get('/nope')
        self.assertEqual(resp1.status_code, 200)
        self.assertEqual(resp2.status_code, 200)
        self.assertEqual(resp3.status_code, 200)
        self.assertEqual(resp4.status_code, 200)
        self.assertNotEqual(resp5.status_code, 200)

class JSONTests(unittest.TestCase):
    def setUp(self):
        self.result = {
            u'responses':
                [{u'hits':
                    {u'hits': [], u'total': 0, u'max_score': None}, u'es_shards': {u'successful': 4, u'failed': 0, u'total': 4}, u'took': 3369, u'timed_out': False},
                    {u'hits': {u'hits': [], u'total': 0, u'max_score': None}, u'es_shards': {u'successful': 4, u'failed': 0, u'total': 4}, u'took': 2986, u'timed_out': False},
                    {u'hits': {u'hits': [
                            {u'es_id': u'j7QEXwZWTUa3G0prgCKaCQ', u'es_score': 1.0, u'es_type': u'communication', u'es_index': u'bro-06251400', u'es_source': {u'peer': u'worker-1', u'src_name': u'child', u'message': u'selects=3000000 canwrites=0 timeouts=2986503', u'ts': 1340647604358, u'level': u'info'}},
                            {u'es_id': u'O_sTSoIXRhmbT1mkJ_WaAw', u'es_score': 1.0, u'es_type': u'communication', u'es_index': u'bro-06251400', u'es_source': {u'peer': u'worker-2', u'src_name': u'child', u'message': u'selects=2900000 canwrites=0 timeouts=2886357', u'ts': 1340647615143, u'level': u'info'}},
                        ], u'total': 407, u'max_score': 1.0}, u'es_shards': {u'successful': 4, u'failed': 0, u'total': 4}, u'took': 4349, u'timed_out': False},
                    {u'hits': {u'hits': [
                            {u'es_id': u'rWIR82xHRjyjDnsBFcEkqQ', u'es_score': 1.0, u'es_type': u'conn', u'es_index': u'bro-06251400', u'es_source': {u'resp_bytes': 45, u'uid': u'SpoGdOarGy3', u'conn_state': u'SF', u'proto': u'udp', u'id.orig_p': 20961, u'id.resp_h': u'128.123.140.21', u'orig_pkts': 1, u'orig_ip_bytes': 70, u'ts': 1340647618510, u'id.orig_h': u'192.92.82.251', u'id.resp_p': 62011, u'tunnel_parents': [], u'resp_pkts': 1, u'local_orig': 0, u'missed_bytes': 0, u'duration': 0.075358, u'orig_bytes': 42, u'resp_ip_bytes': 73, u'history': u'Dd'}},
                            {u'es_id': u'Q9PyFb8aTTy2mnn-lWfwmA', u'es_score': 1.0, u'es_type': u'conn', u'es_index': u'bro-06251400', u'es_source': {u'resp_bytes': 178, u'uid': u'Kv8BEzH3L7d', u'conn_state': u'SF', u'proto': u'udp', u'id.orig_p': 22821, u'id.resp_h': u'128.0.100.9', u'orig_pkts': 4, u'orig_ip_bytes': 788, u'ts': 1340647617494, u'id.orig_h': u'12.113.6.0', u'id.resp_p': 53890, u'tunnel_parents': [], u'resp_pkts': 5, u'local_orig': 0, u'missed_bytes': 0, u'duration': 0.876488, u'orig_bytes': 676, u'resp_ip_bytes': 318, u'history': u'Dd'}},
                        ], u'total': 371817, u'max_score': 1.0}, u'es_shards': {u'successful': 4, u'failed': 0, u'total': 4}, u'took': 4572, u'timed_out': False},
                    {u'hits': {u'hits': [
                            {u'es_id': u'b1oxRcZVT9aeDFbMbDCw5g', u'es_score': 1.0, u'es_type': u'dns', u'es_index': u'bro-06251400', u'es_source': {u'AA': 0, u'RD': 1, u'rcode': 0, u'qclass_name': u'C_INTERNET', u'uid': u'OgG6MWp32o1', u'proto': u'udp', u'id.orig_p': 1087, u'id.resp_h': u'128.2.0.0', u'rcode_name': u'NOERROR', u'ts': 1340647607992, u'id.orig_h': u'23.123.21.19', u'id.resp_p': 53, u'qclass': 1, u'RA': 0, u'qtype_name': u'A', u'query': u'bro-ids.org', u'Z': 0, u'qtype': 1, u'TC': 0, u'trans_id': 1536}},
                            {u'es_id': u'giL8QVdMT-O6IbDNjLSGKA', u'es_score': 1.0, u'es_type': u'dns', u'es_index': u'bro-06251400', u'es_source': {u'AA': 0, u'RD': 1, u'rcode': 0, u'qclass_name': u'C_INTERNET', u'uid': u'OgG6MWp32o1', u'proto': u'udp', u'id.orig_p': 1087, u'id.resp_h': u'128.2.0.0', u'rcode_name': u'NOERROR', u'ts': 1340647637696, u'id.orig_h': u'8.8.35.8', u'id.resp_p': 53, u'qclass': 1, u'RA': 0, u'qtype_name': u'A', u'query': u'a1158.b.akamai.net', u'Z': 0, u'qtype': 1, u'TC': 0, u'trans_id': 13688}},
                        ], u'total': 76715, u'max_score': 1.0}, u'es_shards': {u'successful': 4, u'failed': 0, u'total': 4}, u'took': 4600, u'timed_out': False},
                    {u'hits': {u'hits': [
                            {u'es_id': u'3aCWgiH4QpioEAJZQ6achg', u'es_score': 1.0, u'es_type': u'dpd', u'es_index': u'bro-06251400', u'es_source': {u'uid': u'L1NUOOOptp2', u'proto': u'tcp', u'id.orig_p': 52162, u'id.resp_h': u'17.0.6.4', u'ts': 1340647598519, u'analyzer': u'SSL', u'failure_reason': u'unexpected Handshake message SERVER_HELLO from responder in state INITIAL', u'id.orig_h': u'128.255.255.16', u'id.resp_p': 443}},
                            {u'es_id': u'hJSrHUgFQI6ngNAU8QSImw', u'es_score': 1.0, u'es_type': u'dpd', u'es_index': u'bro-06251400', u'es_source': {u'uid': u'ZYbazGdmJc9', u'proto': u'tcp', u'id.orig_p': 56574, u'id.resp_h': u'128.2.3.4', u'ts': 1340647599095, u'analyzer': u'SSL', u'failure_reason': u'unexpected Handshake message SERVER_HELLO from responder in state INITIAL', u'id.orig_h': u'9.8.7.6', u'id.resp_p': 443}},
                        ], u'total': 896, u'max_score': 1.0}, u'es_shards': {u'successful': 4, u'failed': 0, u'total': 4}, u'took': 4309, u'timed_out': False},
                    {u'hits': {u'hits': [
                            {u'es_id': u'Ceps5reQRkmnNL0dOJ9p8g', u'es_score': 1.0, u'es_type': u'ftp', u'es_index': u'bro-06251400', u'es_source': {u'reply_msg': u'Transfer complete.', u'uid': u'J2Z55eweLj6', u'id.orig_p': 47491, u'id.resp_h': u'2.1.155.1', u'file_size': 4, u'ts': 1340647523506, u'id.orig_h': u'128.5.130.21', u'id.resp_p': 21, u'reply_code': 226, u'command': u'RETR', u'user': u'anonymous', u'arg': u'ftp://2.1.155.1/archlinux/ftpfull/extra/os/x86_64/libxfce4ui-4.10.0-1-x86_64.pkg.tar.xz', u'password': u'ftp@example.com'}},
                            {u'es_id': u'PlWSvWewSsmi-bDx3HQQ_Q', u'es_score': 1.0, u'es_type': u'ftp', u'es_index': u'bro-06251400', u'es_source': {u'reply_msg': u'Transfer complete.', u'uid': u'J2Z55eweLj6', u'id.orig_p': 47491, u'id.resp_h': u'2.1.155.2', u'file_size': 0, u'ts': 1340647526224, u'id.orig_h': u'128.5.130.21', u'id.resp_p': 21, u'reply_code': 226, u'command': u'RETR', u'user': u'anonymous', u'arg': u'ftp://2.1.155.2/archlinux/ftpfull/extra/os/x86_64/garcon-0.2.0-1-x86_64.pkg.tar.xz', u'password': u'ftp@example.com'}},
                        ], u'total': 38, u'max_score': 1.0}, u'es_shards': {u'successful': 4, u'failed': 0, u'total': 4}, u'took': 4424, u'timed_out': False},
                    {u'hits': {u'hits': [
                            {u'es_id': u'BSAn4rBpQnWtoZ7_oJ2aSg', u'es_score': 1.0, u'es_type': u'http', u'es_index': u'bro-06251400', u'es_source': {u'trans_depth': 1, u'status_code': 200, u'uid': u'dbuYW3FQVa8', u'request_body_len': 0, u'response_body_len': 73773, u'id.orig_p': 51622, u'id.resp_h': u'128.2.7.192', u'status_msg': u'OK', u'tags': [], u'ts': 1340647560439, u'uri': u'/images/detail-sprite.png', u'id.orig_h': u'16.193.137.16', u'id.resp_p': 80, u'host': u'gigapan.com', u'user_agent': u'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)', u'referrer': u'http://gigapan.com/galleries/5998/gigapans/93336', u'cookie_vars': [u'es__utmb', u'es__utma', u'es__utmc', u'es_gigapan_session', u'es__utmz'], u'uri_vars': [u'/images/detail-sprite.png'], u'method': u'GET', u'mime_type': u'image/png', u'client_header_names': [u'ACCEPT', u'REFERER', u'ACCEPT-LANGUAGE', u'USER-AGENT', u'ACCEPT-ENCODING', u'HOST', u'CONNECTION', u'COOKIE']}},
                            {u'es_id': u'TKvkppiqTyyjfPtY_7e6Jg', u'es_score': 1.0, u'es_type': u'http', u'es_index': u'bro-06251400', u'es_source': {u'trans_depth': 3, u'uid': u'shriLS4fZa9', u'request_body_len': 0, u'response_body_len': 245207, u'id.orig_p': 53860, u'id.resp_h': u'130.64.126.25', u'status_msg': u'Partial Content', u'tags': [], u'ts': 1340647561145, u'uri': u'/pdf/menus/Dinner.pdf', u'id.orig_h': u'128.237.124.18', u'id.resp_p': 80, u'host': u'www.dining.com', u'user_agent': u'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:13.0) Gecko/20100101 Firefox/13.0.1', u'status_code': 206, u'cookie_vars': [u'es__utmc', u's_sq', u'es__utma', u's_cmrun', u'es__utmb', u's_cc', u's_nr', u's_evar5', u'es__utmz', u'ASPSESSIONIDSABACRQR'], u'uri_vars': [u'/pdf/menus/Dinner.pdf'], u'method': u'GET', u'client_header_names': [u'HOST', u'USER-AGENT', u'ACCEPT', u'ACCEPT-LANGUAGE', u'ACCEPT-ENCODING', u'DNT', u'CONNECTION', u'RANGE', u'COOKIE']}},
                        ], u'total': 150255, u'max_score': 1.0}, u'es_shards': {u'successful': 4, u'failed': 0, u'total': 4}, u'took': 4595, u'timed_out': False},
                    {u'hits': {u'hits': [
                            {u'es_id': u'zblyDe_wQwuQFAUrIdCvZw', u'es_score': 1.0, u'es_type': u'irc', u'es_index': u'bro-06251400', u'es_source': {u'uid': u'dcqnFZeA4x6', u'id.orig_p': 40206, u'id.resp_h': u'128.237.112.64', u'ts': 1340647291296, u'value': u'#Cyanogenmod', u'id.orig_h': u'123.9.144.4', u'id.resp_p': 6667, u'command': u'JOIN', u'addl': u''}},
                            {u'es_id': u'KgE_2ZMNTUKUu7YCygQy2Q', u'es_score': 1.0, u'es_type': u'irc', u'es_index': u'bro-06251400', u'es_source': {u'uid': u'dcqnFZeA4x6', u'id.orig_p': 40206, u'id.resp_h': u'128.237.112.64', u'ts': 1340647321396, u'value': u'#cyanogenmod-dev', u'id.orig_h': u'123.9.144.4', u'id.resp_p': 6667, u'command': u'JOIN', u'addl': u''}},
                        ], u'total': 91, u'max_score': 1.0}, u'es_shards': {u'successful': 4, u'failed': 0, u'total': 4}, u'took': 4451, u'timed_out': False},
                    {u'hits': {u'hits': [
                            {u'es_id': u'Af_PFqc8R5CndEOMdT0Mjw', u'es_score': 1.0, u'es_type': u'known_certs', u'es_index': u'bro-06251400', u'es_source': {u'issuer_subject': u'CN=COMODO High-Assurance Secure Server CA,O=COMODO CA Limited,L=Salford,ST=Greater Manchester,C=GB', u'port_num': 443, u'ts': 1340647603095, u'host': u'128.2.105.87', u'serial': u'1BBEB37A021343B91E1DA231CCFE4126', u'subject': u'CN=calendar.andrew.cmu.edu,OU=PlatinumSSL,OU=Hosted by Carnegie Mellon University,OU=Computing Services,O=Carnegie Mellon University,streetAddress=5000 Forbes Ave,L=Pittsburgh,ST=PA,postalCode=15213,C=US'}},
                            {u'es_id': u'fw_q48I1QQ25RKJb1_ae1w', u'es_score': 1.0, u'es_type': u'known_certs', u'es_index': u'bro-06251400', u'es_source': {u'issuer_subject': u'CN=COMODO High-Assurance Secure Server CA,O=COMODO CA Limited,L=Salford,ST=Greater Manchester,C=GB', u'port_num': 443, u'ts': 1340647610354, u'host': u'128.2.229.61', u'serial': u'170031A4782B972E1ECE57371A12510A', u'subject': u'CN=hpp.web.cmu.edu,OU=PlatinumSSL,OU=Hosted by Carnegie Mellon University,OU=Health Professions Program,O=Carnegie Mellon University,streetAddress=5000 Forbes Ave,L=Pittsburgh,ST=PA,postalCode=15213,C=US'}},
                        ], u'total': 101, u'max_score': 1.0}, u'es_shards': {u'successful': 4, u'failed': 0, u'total': 4}, u'took': 4451, u'timed_out': False},
                    {u'hits': {u'hits': [
                            {u'es_id': u'0-L6DW-lRXiPi7j1vS2rFg', u'es_score': 1.0, u'es_type': u'known_hosts', u'es_index': u'bro-06251400', u'es_source': {u'host': u'128.2.5.6', u'ts': 1340647598892}},
                            {u'es_id': u'OFNta4uxR2GrRoWqVDr7HQ', u'es_score': 1.0, u'es_type': u'known_hosts', u'es_index': u'bro-06251400', u'es_source': {u'host': u'128.2.6.5', u'ts': 1340647599402}},
                        ], u'total': 5539, u'max_score': 1.0}, u'es_shards': {u'successful': 4, u'failed': 0, u'total': 4}, u'took': 4308, u'timed_out': False},
                    {u'hits': {u'hits': [
                            {u'es_id': u'2pUFZ_cBTKWTUIT0OMcyoQ', u'es_score': 1.0, u'es_type': u'known_services', u'es_index': u'bro-06251400', u'es_source': {u'port_proto': u'tcp', u'host': u'128.2.46.19', u'port_num': 3389, u'ts': 1340647299382, u'service': []}},
                            {u'es_id': u'kcJJJU_URmi0LIJqKqmR6Q', u'es_score': 1.0, u'es_type': u'known_services', u'es_index': u'bro-06251400', u'es_source': {u'port_proto': u'tcp', u'host': u'128.237.20.16', u'port_num': 46657, u'ts': 1340647300365, u'service': []}},
                        ], u'total': 1156, u'max_score': 1.0}, u'es_shards': {u'successful': 4, u'failed': 0, u'total': 4}, u'took': 4307, u'timed_out': False},
                    {u'hits': {u'hits': [], u'total': 0, u'max_score': None}, u'es_shards': {u'successful': 4, u'failed': 0, u'total': 4}, u'took': 2982, u'timed_out': False},
                    {u'hits': {u'hits': [], u'total': 0, u'max_score': None}, u'es_shards': {u'successful': 4, u'failed': 0, u'total': 4}, u'took': 3665, u'timed_out': False},
                    {u'hits': {u'hits': [], u'total': 0, u'max_score': None}, u'es_shards': {u'successful': 4, u'failed': 0, u'total': 4}, u'took': 2981, u'timed_out': False},
                    {u'hits': {u'hits': [
                            {u'es_id': u'DqY183JqTfGFzEMgLs0nhg', u'es_score': 1.0, u'es_type': u'notice', u'es_index': u'bro-06251400', u'es_source': {u'note': u'HTTP::Incorrect_File_Type', u'dropped': 0, u'uid': u'jFvD488oPPk', u'proto': u'tcp', u'id.orig_p': 2899, u'id.resp_h': u'128.2.8.13', u'dst': u'128.2.8.13', u'policy_items': [7, 6], u'ts': 1340647599222, u'p': 50308, u'id.orig_h': u'15.8.33.147', u'id.resp_p': 50308, u'peer_descr': u'worker-3', u'actions': [u'Notice::ACTION_ALARM', u'Notice::ACTION_LOG'], u'msg': u'application/x-dosexec GET http://128.2.8.13:50308/tcp/8679844E004FA5E5A28B1C15EF2839B6', u'src': u'15.8.33.147', u'suppress_for': 3600.0}},
                            {u'es_id': u'yhcrO8-6Sky8npaERDDf5g', u'es_score': 1.0, u'es_type': u'notice', u'es_index': u'bro-06251400', u'es_source': {u'note': u'DNS::External_Name', u'dropped': 0, u'uid': u'Fm5zi7Yngvj', u'proto': u'tcp', u'id.orig_p': 51250, u'id.resp_h': u'15.8.33.147', u'dst': u'15.8.33.147', u'policy_items': [7, 6], u'ts': 1340647604356, u'p': 53, u'id.orig_h': u'128.2.2.14', u'id.resp_p': 53, u'peer_descr': u'worker-1', u'actions': [u'Notice::ACTION_ALARM', u'Notice::ACTION_LOG'], u'msg': u'plab.planetlab.org is pointing to a local host - 128.2.5.5.', u'src': u'128.2.2.14', u'suppress_for': 3600.0}},
                        ], u'total': 241, u'max_score': 1.0}, u'es_shards': {u'successful': 4, u'failed': 0, u'total': 4}, u'took': 4112, u'timed_out': False},
                    {u'hits': {u'hits': [
                            {u'es_id': u'DqY183JqTfGFzEMgLs0nhg', u'es_score': 1.0, u'es_type': u'notice_alarm', u'es_index': u'bro-06251400', u'es_source': {u'note': u'HTTP::Incorrect_File_Type', u'dropped': 0, u'uid': u'jFvD488oPPk', u'proto': u'tcp', u'id.orig_p': 2899, u'id.resp_h': u'128.2.8.13', u'dst': u'128.2.8.13', u'policy_items': [7, 6], u'ts': 1340647599222, u'p': 50308, u'id.orig_h': u'15.8.33.147', u'id.resp_p': 50308, u'peer_descr': u'worker-3', u'actions': [u'Notice::ACTION_ALARM', u'Notice::ACTION_LOG'], u'msg': u'application/x-dosexec GET http://128.2.8.13:50308/tcp/8679844E004FA5E5A28B1C15EF2839B6', u'src': u'15.8.33.147', u'suppress_for': 3600.0}},
                            {u'es_id': u'yhcrO8-6Sky8npaERDDf5g', u'es_score': 1.0, u'es_type': u'notice_alarm', u'es_index': u'bro-06251400', u'es_source': {u'note': u'DNS::External_Name', u'dropped': 0, u'uid': u'Fm5zi7Yngvj', u'proto': u'tcp', u'id.orig_p': 51250, u'id.resp_h': u'15.8.33.147', u'dst': u'15.8.33.147', u'policy_items': [7, 6], u'ts': 1340647604356, u'p': 53, u'id.orig_h': u'128.2.2.14', u'id.resp_p': 53, u'peer_descr': u'worker-1', u'actions': [u'Notice::ACTION_ALARM', u'Notice::ACTION_LOG'], u'msg': u'plab.planetlab.org is pointing to a local host - 128.2.5.5.', u'src': u'128.2.2.14', u'suppress_for': 3600.0}},
                        ], u'total': 241, u'max_score': 1.0}, u'es_shards': {u'successful': 4, u'failed': 0, u'total': 4}, u'took': 4309, u'timed_out': False},
                    {u'hits': {u'hits': [], u'total': 0, u'max_score': None}, u'es_shards': {u'successful': 4, u'failed': 0, u'total': 4}, u'took': 3519, u'timed_out': False},
                    {u'hits': {u'hits': [], u'total': 0, u'max_score': None}, u'es_shards': {u'successful': 4, u'failed': 0, u'total': 4}, u'took': 2835, u'timed_out': False},
                    {u'hits': {u'hits': [
                            {u'es_id': u'b5JqQtxcQjmb3EPJdQhszg', u'es_score': 1.0, u'es_type': u'reporter', u'es_index': u'bro-06251400', u'es_source': {u'message': u'processing suspended', u'location': u'', u'ts': 1340647282484, u'level': u'Reporter::INFO'}}, {u'es_id': u'cWt1H-MuTYmGkHqhLla4zA', u'es_score': 1.0, u'es_type': u'reporter', u'es_index': u'bro-06251400', u'es_source': {u'message': u'Failed to open GeoIP database: /usr/share/GeoIP/GeoIPCity.dat', u'location': u'', u'ts': 1340647439536, u'level': u'Reporter::WARNING'}},
                            {u'es_id': u'SQm2tHbPQ9ijRCVcD26Tkw', u'es_score': 1.0, u'es_type': u'reporter', u'es_index': u'bro-06251400', u'es_source': {u'message': u'Fell back to GeoIP Country database', u'location': u'', u'ts': 1340647439536, u'level': u'Reporter::WARNING'}},
                        ], u'total': 11, u'max_score': 1.0}, u'es_shards': {u'successful': 4, u'failed': 0, u'total': 4}, u'took': 3885, u'timed_out': False},
                    {u'hits': {u'hits': [], u'total': 0, u'max_score': None}, u'es_shards': {u'successful': 4, u'failed': 0, u'total': 4}, u'took': 2834, u'timed_out': False},
                    {u'hits': {u'hits': [
                            {u'es_id': u'TS-aiV6_TJGSfbVzY4cxiQ', u'es_score': 1.0, u'es_type': u'smtp', u'es_index': u'bro-06251400', u'es_source': {u'mailfrom': u'<bot@andrew.cmu.edu>', u'trans_depth': 1, u'from': u'"A robot" <bot@andrew.cmu.edu>', u'uid': u'bJ80fNuYd4i', u'to': [u'anotherbot@google.net'], u'id.orig_p': 46212, u'id.resp_h': u'176.46.24.119', u'first_received': u'from 128.2.1.1 (proxying for 192.168.24.13)        (SquirrelMail authenticated user bot@andrew.cmu.edu)        by webmail.andrew.cmu.edu with HTTP;        Mon, 25 Jun 2012 14:06:38 -0400', u'msg_id': u'<50170e817247841935e688ee39a357b8.squirrel@webmail.andrew.cmu.edu>', u'ts': 1340647599579, u'second_received': u'from webmail.andrew.cmu.edu (WEBMAIL-03.ANDREW.CMU.EDU [128.2.105.111])\t(user=bot mech=GSSAPI (56 bits))\tby smtp.andrew.cmu.edu (8.14.4/8.14.4) with ESMTP id q5PI6cYu024152\tfor <anotherbot@google.net>; Mon, 25 Jun 2012 14:06:38 -0400', u'id.orig_h': u'128.2.11.95', u'id.resp_p': 25, u'is_webmail': 1, u'rcptto': [u'<anotherbot@google.net>'], u'user_agent': u'SquirrelMail/1.4.22', u'date': u'Mon, 25 Jun 2012 14:06:38 -0400', u'path': [u'192.168.172.18', u'12.2.65.73', u'128.2.103.12', u'128.2.4.4'], u'helo': u'smtp.andrew.cmu.edu', u'last_reply': u'250 2.0.0 Si6f1j00d232CWw06i6fYH mail accepted for delivery', u'subject': u'[Fwd: Some Spam!]'}},
                            {u'es_id': u'tvbXEWoVTlWgnYqBVaxiOg', u'es_score': 1.0, u'es_type': u'smtp', u'es_index': u'bro-06251400', u'es_source': {u'mailfrom': u'<rudolph@cmu.edu>', u'trans_depth': 1, u'from': u'"Rudolph" <rudolph@cmu.edu>', u'uid': u'XdFptTlDHEa', u'to': [u'"\'Santa\'" <santa4@aol.com>'], u'id.orig_p': 58555, u'id.resp_h': u'23.167.15.33', u'first_received': u'from Blitzen (mail.aol.com [6.4.4.6])\t(user=rudolph mech=LOGIN (0 bits))\tby smtp.mail.edu (8.14.4/8.14.4) with ESMTP id q5PI6b2O014333\t(version=TLSv1/SSLv3 cipher=AES128-SHA bits=128 verify=NOT)\tfor <santa@aol.com>; Mon, 25 Jun 2012 14:06:38 -0400', u'msg_id': u'<001c01cd52fd$425395b0$c6fac110$@cmu.edu>', u'ts': 1340647600640, u'last_reply': u'250 ok:  Message 1796213216 accepted', u'id.orig_h': u'17.5.231.224', u'id.resp_p': 25, u'is_webmail': 0, u'rcptto': [u'<santa@att.com>'], u'user_agent': u'Microsoft Outlook 14.0', u'date': u'Mon, 25 Jun 2012 14:06:34 -0400', u'path': [u'172.43.243.2', u'128.2.123.2', u'27.8.13.224'], u'helo': u'smtp.mail.edu', u'in_reply_to': u'<020801cd52fb$9b1b20e0$d151f2a0$@com>', u'subject': u'RE: About...'}},
                        ], u'total': 1484, u'max_score': 1.0}, u'es_shards': {u'successful': 4, u'failed': 0, u'total': 4}, u'took': 4159, u'timed_out': False},
                    {u'hits': {u'hits': [
                            {u'es_id': u'Q3yvzguwToaRIwuntQWlaQ', u'es_score': 1.0, u'es_type': u'smtp_entities', u'es_index': u'bro-06251400', u'es_source': {u'excerpt': u'', u'trans_depth': 1, u'uid': u'XHtqpmt34X5', u'id.orig_p': 35862, u'id.resp_h': u'128.2.67.132', u'content_len': 39750, u'ts': 1340647597467, u'id.orig_h': u'154.33.127.21', u'id.resp_p': 25, u'mime_type': u'text/html'}},
                            {u'es_id': u'sunNH3NgQ4yJndenj7FI_w', u'es_score': 1.0, u'es_type': u'smtp_entities', u'es_index': u'bro-06251400', u'es_source': {u'excerpt': u'', u'trans_depth': 1, u'uid': u'FYYqOdAqtR8', u'id.orig_p': 58902, u'id.resp_h': u'193.54.168.226', u'content_len': 411, u'ts': 1340647598641, u'id.orig_h': u'128.236.98', u'id.resp_p': 25, u'mime_type': u'text/plain'}},
                        ], u'total': 1809, u'max_score': 1.0}, u'es_shards': {u'successful': 4, u'failed': 0, u'total': 4}, u'took': 4158, u'timed_out': False},
                    {u'hits': {u'hits': [], u'total': 0, u'max_score': None}, u'es_shards': {u'successful': 4, u'failed': 0, u'total': 4}, u'took': 2833, u'timed_out': False},
                    {u'hits': {u'hits': [
                            {u'es_id': u'IRQMZJ5WT_-RqjsEXL-7TQ', u'es_score': 1.0, u'es_type': u'software', u'es_index': u'bro-06251400', u'es_source': {u'name': u'Firefox', u'unparsed_version': u'Mozilla/5.0 (Windows NT 5.1; rv:10.0.2) Gecko/20100101 Firefox/10.0.2', u'version.minor': 0, u'ts': 1340647282525, u'host': u'128.2.123.22', u'version.minor2': 2, u'software_type': u'HTTP::BROWSER', u'version.major': 10}},
                            {u'es_id': u'61GFYU28S5CD8hI9rJcYSw', u'es_score': 1.0, u'es_type': u'software', u'es_index': u'bro-06251400', u'es_source': {u'name': u'Safari', u'unparsed_version': u'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/534.56.5 (KHTML, like Gecko) Version/5.1.6 Safari/534.56.5', u'version.minor': 1, u'ts': 1340647282525, u'host': u'128.53.122.196', u'version.minor2': 6, u'software_type': u'HTTP::BROWSER', u'version.major': 5}},
                        ], u'total': 7495, u'max_score': 1.0}, u'es_shards': {u'successful': 4, u'failed': 0, u'total': 4}, u'took': 4215, u'timed_out': False},
                    {u'hits': {u'hits': [
                            {u'es_id': u'2e5V_u7rT9Cayy6aZ9dgcA', u'es_score': 1.0, u'es_type': u'ssh', u'es_index': u'bro-06251400', u'es_source': {u'status': u'failure', u'direction': u'INBOUND', u'uid': u'GjR1jckW1y6', u'id.orig_p': 57971, u'id.resp_h': u'123.69.87.17', u'ts': 1340647594375, u'server': u'SSH-2.0-OpenSSH_5.5p1 Debian-4ubuntu6', u'id.orig_h': u'122.75.87.119', u'id.resp_p': 22, u'client': u'SSH-2.0-libssh-0.1', u'resp_size': 1671}},
                            {u'es_id': u'EKnt03nwSw6NsE6n7u833A', u'es_score': 1.0, u'es_type': u'ssh', u'es_index': u'bro-06251400', u'es_source': {u'status': u'failure', u'direction': u'INBOUND', u'uid': u'jMH9eIUdLe', u'id.orig_p': 47751, u'id.resp_h': u'24.134.211.182', u'ts': 1340647598344, u'server': u'SSH-2.0-OpenSSH_5.3p1 Debian-3ubuntu7', u'id.orig_h': u'210.17.148.14', u'id.resp_p': 22, u'client': u'SSH-2.0-libssh-0.1', u'resp_size': 1671}},
                        ], u'total': 385, u'max_score': 1.0}, u'es_shards': {u'successful': 4, u'failed': 0, u'total': 4}, u'took': 4199, u'timed_out': False},
                    {u'hits': {u'hits': [
                            {u'es_id': u'1ObFkGroTl6XdJ6OLKyyiQ', u'es_score': 1.0, u'es_type': u'ssl', u'es_index': u'bro-06251400', u'es_source': {u'uid': u'PLYYVXtxoS7', u'server_name': u'mail.google.com', u'id.orig_p': 44929, u'id.resp_h': u'17.145.28.193', u'ts': 1340647651797, u'session_id': u'c32fe4de2d28fc55c20cdc1693a41d9595feaf1f941c82537cbb25b89ca0267b', u'id.orig_h': u'128.2.99.138', u'id.resp_p': 443, u'version': u'TLSv10', u'cipher': u'TLS_ECDHE_RSA_WITH_RC4_128_SHA'}},
                            {u'es_id': u'EB-Jj0avRw2a46wbhyoAoA', u'es_score': 1.0, u'es_type': u'ssl', u'es_index': u'bro-06251400', u'es_source': {u'not_valid_after': 1391057999000, u'issuer_subject': u'CN=Thawte SSL CA,O=Thawte\\, Inc.,C=US', u'uid': u'HBSDvWDLWSa', u'server_name': u'photos-5.dropbox.com', u'id.orig_p': 57865, u'id.resp_h': u'123.121.12.17', u'ts': 1340647651599, u'id.orig_h': u'128.2.237.18', u'id.resp_p': 443, u'version': u'TLSv10', u'cert_hash': u'd7bc4836e22e4e6ece99996bf05a4638', u'not_valid_before': 1322715600000, u'validation_status': u'ok', u'cipher': u'TLS_DHE_RSA_WITH_AES_256_CBC_SHA', u'subject': u'CN=*.dropbox.com,O=Dropbox\\, Inc.,L=San Francisco,ST=California,C=US'}},
                        ], u'total': 20017, u'max_score': 1.0}, u'es_shards': {u'successful': 4, u'failed': 0, u'total': 4}, u'took': 4313, u'timed_out': False},
                    {u'hits': {u'hits': [], u'total': 0, u'max_score': None}, u'es_shards': {u'successful': 4, u'failed': 0, u'total': 4}, u'took': 2831, u'timed_out': False},
                    {u'hits': {u'hits': [
                            {u'es_id': u'QqGX-5qPR6uRQr4nq0MHRg', u'es_score': 1.0, u'es_type': u'syslog', u'es_index': u'bro-06251400', u'es_source': {u'uid': u'5g5xqQAmdh2', u'proto': u'udp', u'id.orig_p': 40629, u'id.resp_h': u'128.2.12.0', u'facility': u'LOCAL0', u'ts': 1340647493276, u'id.orig_h': u'66.93.128.15', u'id.resp_p': 514, u'message': u' IP: entry duplicated 2 times @2012-06-25-13:09:53', u'severity': u'WARNING'}},
                            {u'es_id': u'mZuYoDNYTVSQF04HYMGTxQ', u'es_score': 1.0, u'es_type': u'syslog', u'es_index': u'bro-06251400', u'es_source': {u'uid': u'lhsZfvPM2s5', u'proto': u'udp', u'id.orig_p': 40631, u'id.resp_h': u'128.2.12.0', u'facility': u'LOCAL0', u'ts': 1340647551462, u'id.orig_h': u'66.93.128.15', u'id.resp_p': 514, u'message': u' IP: discard from 12.181.172.12 port 55556 to 66.93.182.15 port 54 TCP SYN (default) @2012-06-25-13:12:21', u'severity': u'WARNING'}}
                        ], u'total': 2, u'max_score': 1.0}, u'es_shards': {u'successful': 4, u'failed': 0, u'total': 4}, u'took': 3450, u'timed_out': False},
                    {u'hits': {u'hits': [
                            {u'es_id': u'askIegRiTZOpcWKmGNn3rQ', u'es_score': 1.0, u'es_type': u'tunnel', u'es_index': u'bro-06251400', u'es_source': {u'uid': u'ltygZNzxov', u'tunnel_type': u'Tunnel::IP', u'id.orig_p': 0, u'id.resp_h': u'128.2.15.155', u'ts': 1340647599658, u'id.orig_h': u'94.25.201.137', u'id.resp_p': 0, u'action': u'Tunnel::DISCOVER'}},
                            {u'es_id': u'XQdf2DnIQvWqi6FoM2uV-Q', u'es_score': 1.0, u'es_type': u'tunnel', u'es_index': u'bro-06251400', u'es_source': {u'uid': u'fy89Hx63iid', u'tunnel_type': u'Tunnel::TEREDO', u'id.orig_p': 64611, u'id.resp_h': u'65.123.18.128', u'ts': 1340647602701, u'id.orig_h': u'128.2.195.21', u'id.resp_p': 3544, u'action': u'Tunnel::DISCOVER'}},
                        ], u'total': 466, u'max_score': 1.0}, u'es_shards': {u'successful': 4, u'failed': 0, u'total': 4}, u'took': 4214, u'timed_out': False},
                    {u'hits': {u'hits': [
                            {u'es_id': u'5VfseO8aQU-OQqkhuTVohA', u'es_score': 1.0, u'es_type': u'weird', u'es_index': u'bro-06251400', u'es_source': {u'notice': 0, u'uid': u'42FJ0XejeT9', u'id.orig_p': 4850, u'id.resp_h': u'69.123.24.83', u'ts': 1340647598696, u'id.orig_h': u'128.2.18.19', u'id.resp_p': 80, u'peer': u'worker-3', u'name': u'unescaped_special_URI_char'}},
                            {u'es_id': u'4HFM97ukTEeIcmjs4aDhtg', u'es_score': 1.0, u'es_type': u'weird', u'es_index': u'bro-06251400', u'es_source': {u'notice': 0, u'uid': u'9v5DdeLTzwd', u'id.orig_p': 4378, u'id.resp_h': u'8.27.18.23', u'ts': 1340647598924, u'id.orig_h': u'128.2.17.52', u'id.resp_p': 80, u'peer': u'worker-3', u'name': u'inflate_failed'}},
                        ], u'total': 4977, u'max_score': 1.0}, u'es_shards': {u'successful': 4, u'failed': 0, u'total': 4}, u'took': 4205, u'timed_out': False}
                ]
        }
        self.factory = RequestFactory()


    def testStatusCode(self):
        data = {"query": "*", "openTab": "conn", "hits": self.result}
        request = self.factory.get("/")
        self.assertEqual(render(request, "home.html", data).status_code, 200)

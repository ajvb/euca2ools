# Software License Agreement (BSD License)
#
# Copyright (c) 2009-2012, Eucalyptus Systems, Inc.
# All rights reserved.
#
# Redistribution and use of this software in source and binary forms, with or
# without modification, are permitted provided that the following conditions
# are met:
#
#   Redistributions of source code must retain the above
#   copyright notice, this list of conditions and the
#   following disclaimer.
#
#   Redistributions in binary form must reproduce the above
#   copyright notice, this list of conditions and the
#   following disclaimer in the documentation and/or other
#   materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from requestbuilder import Arg, Filter
from . import EucalyptusRequest

class DescribeSecurityGroups(EucalyptusRequest):
    Description = '''\
        Show information about security groups

        Note that filters are matched on literal strings only, so
        "--filter ip-permission.from-port=22" will *not* match a group with a
        port range of 20 to 30.'''

    APIVersion = '2011-01-01'
    Args = [Arg('group', metavar='GROUP', nargs='*', route_to=None, default=[],
                help='limit results to one or more security groups')]
    Filters = [Filter('description', help='group description'),
               Filter('group-id'),
               Filter('group-name'),
               Filter('ip-permission.cidr',
                      help='CIDR IP range granted permission by the group'),
               Filter('ip-permission.from-port',
                      help='start of TCP/UDP port range, or ICMP type number'),
               Filter('ip-permission.group-name', help='''name of another group
                      granted permission by this group'''),
               Filter('ip-permission.protocol',
                      choices=('tcp', 'udp', 'icmp', '6', '17', '1'),
                      help='IP protocol for the permission'),
               Filter('ip-permission.to-port',
                      help='end of TCP/UDP port range, or ICMP code'),
               Filter('ip-permission.user-id',
                      help='ID of an account granted permission'),
               Filter('owner-id', help=="account ID of the group's owner"),
               Filter('tag-key', help='key of a tag assigned to the group'),
               Filter('tag-value',
                      help='value of a tag assigned to the group')]
    ListMarkers = ['securityGroupInfo', 'ipPermissions', 'ipPermissionsEgress',
                   'groups', 'ipRanges']
    ItemMarkers = ['item']

    def main(self):
        self.params = {}
        for group in self.args['group']:
            # Uncomment this during the next API version bump
            #if group.startswith('sg-'):
            #    self.params.setdefault('GroupId', [])
            #    self.params['GroupId'].append(group)
            #else:
                self.params.setdefault('GroupName', [])
                self.params['GroupName'].append(group)
        return self.send()

    def print_result(self, result):
        for group in result.get('securityGroupInfo', []):
            self.print_group(group)

    def print_group(self, group):
        print self.tabify(('GROUP', group.get('groupId'), group.get('ownerId'),
                           group.get('groupName'),
                           group.get('groupDescription')))
        for perm in group.get('ipPermissions', []):
            perm_base = ['PERMISSION', group.get('ownerId'),
                         group.get('groupName'), 'ALLOWS']
            perm_base.extend([perm.get('ipProtocol'), perm.get('fromPort'),
                              perm.get('toPort')])
            for cidr_range in perm.get('ipRanges', []):
                perm_item = ['FROM', 'CIDR', cidr_range.get('cidrIp'),
                             'ingress']
                print self.tabify(perm_base + perm_item)
            for othergroup in perm.get('groups', []):
                perm_item = ['FROM', 'USER', othergroup.get('userId')]
                if othergroup.get('groupId'):
                    perm_item.extend(['ID', othergroup['groupId']])
                else:
                    perm_item.extend(['GRPNAME', othergroup['groupName']])
                perm_item.append('ingress')
                print self.tabify(perm_base + perm_item)
        for perm in group.get('ipPermissionsEgress', []):
            perm_base = ['PERMISSION', group.get('ownerId'),
                         group.get('groupName'), 'ALLOWS']
            perm_base.extend([perm.get('ipProtocol'), perm.get('fromPort'),
                              perm.get('toPort')])
            for cidr_range in perm.get('ipRanges', []):
                perm_item = ['TO', 'CIDR', cidr_range.get('cidrIp'), 'egress']
                print self.tabify(perm_base + perm_item)
            for othergroup in perm.get('groups', []):
                perm_item = ['TO', 'USER', othergroup.get('userId')]
                if othergroup.get('groupId'):
                    perm_item.extend(['ID', othergroup['groupId']])
                else:
                    perm_item.extend(['GRPNAME', othergroup['groupName']])
                perm_item.append('egress')
                print self.tabify(perm_base + perm_item)

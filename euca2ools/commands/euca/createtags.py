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

from requestbuilder import Arg
from . import EucalyptusRequest
from .argtypes import binary_tag_def

class CreateTags(EucalyptusRequest):
    APIVersion = '2010-08-31'
    Description = 'Add or overwrite tags for one or more resources'
    Args = [Arg('ResourceId', metavar='RESOURCE', nargs='+',
                help='IDs of the resource(s) to tag'),
            Arg('--tag', dest='Tag', metavar='KEY[=VALUE]',
                type=binary_tag_def, action='append', required=True,
                help='''key and optional value of the tag to create, separated
                        by an "=" character.  If no value is given the tag's
                        value is set to an empty string.''')]

    def print_result(self, result):
        for resource_id in self.args['ResourceId']:
            for tag in self.args['Tag']:
                lc_resource_tag = {'key': tag['Key'], 'value': tag['Value']}
                self.print_resource_tag(lc_resource_tag, resource_id)

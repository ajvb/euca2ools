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

from requestbuilder import Arg, STD_AUTH_ARGS, CONNECTION
import requestbuilder.service
from .. import Euca2oolsRequest

class Euare(requestbuilder.service.BaseService):
    Description = 'Eucalyptus User, Authorization and Reporting Environment'
    APIVersion = '2010-05-08'
    EnvURL = 'EUARE_URL'

    Endpoints = {None: 'iam.amazonaws.com'}

class EuareRequest(Euca2oolsRequest):
    ServiceClass = Euare
    Args = [Arg('-U', '--url', route_to=CONNECTION,
            help='EUARE service URL')] + STD_AUTH_ARGS

    def parse_http_response(self, response_body):
        response = Euca2oolsRequest.parse_http_response(self, response_body)
        # EUARE responses enclose their useful data inside FooResponse
        # elements.  If that's all we have after stripping out ResponseMetadata
        # then just return its contents.
        useful_keys = filter(lambda x: x != 'ResponseMetadata',
                             response.keys())
        if len(useful_keys) == 1:
            return response[useful_keys[0]]
        else:
            return response

DELEGATE = Arg('--delegate', dest='DelegateAccount', metavar='ACCOUNT',
               help='''[Eucalyptus only] interpret this command as if the
                       administrator of a different account had run it (only
                       usable by cloud administrators)''')

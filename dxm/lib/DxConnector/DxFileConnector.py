#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Copyright (c) 2018 by Delphix. All rights reserved.
#
# Author  : Marcin Przepiorowski
# Date    : March 2018
# Comments: List of the Database connectors


import logging
from dxm.lib.DxConnector.DxConnector import DxConnector
from dxm.lib.DxLogging import print_error
from dxm.lib.DxLogging import print_message


class DxFileConnector(DxConnector):

    def __init__(self, engine):
        """
        Constructor
        :param engine: DxMaskingEngine object
        """
        DxConnector.__init__(self, engine)
        #FileConnector.__init__(self)
        self.__engine = engine
        self.__logger = logging.getLogger()
        self.__logger.debug("creating FileConnector object")
        if (self.__engine.version_ge('6.0.0')):
            from masking_api_60.models.file_connector import FileConnector
            from masking_api_60.api.file_connector_api import FileConnectorApi
            from masking_api_60.models.connection_info import ConnectionInfo
            from masking_api_60.rest import ApiException
        else:
            from masking_api_53.models.file_connector import FileConnector
            from masking_api_53.api.file_connector_api import FileConnectorApi
            from masking_api_53.models.connection_info import ConnectionInfo
            from masking_api_53.rest import ApiException

        self.__api = FileConnectorApi
        self.__model = FileConnector
        self.__model_connection_info = ConnectionInfo
        self.__apiexc = ApiException
        self.__obj = None


    @property
    def obj(self):
        if self.__obj is not None:
            return self.__obj
        else:
            return None

    @property
    def connectorId(self):
        return self.obj.file_connector_id

    @property
    def host(self):
        return self.obj.connection_info.host

    @property
    def port(self):
        return self.obj.connection_info.port

    @property
    def schema_name(self):
        return 'N/A'

    @property
    def connector_type(self):
        """
        connector_type
        """
        if self.obj is not None:
            if self.is_database:
                return self.obj.database_type
            else:
                return self.obj.file_type
        else:
            return None


    def from_connector(self, con):
        """
        Set a obj property using a Database Connector 
        :param con: DatabaseConnector object
        """
        self.__obj = con


    def create_connector(self, connector_name, file_type, environment_id, host, port, login_name, password, path, connection_mode):
        """
        Create an connector object
        :param connector_name
        :param database_type
        :param environment_id
        """  

        ci = self.__model_connection_info(connection_mode=connection_mode, path=path, host=host, login_name=login_name, password=password, port=port)
        self.__obj = self.__model(connector_name=connector_name, file_type=file_type, environment_id=environment_id, connection_info=ci)

    def get_type_properties(self):
        """
        Return dict with properties specific for connector type
        """
        props = {
            'login_name': self.obj.connection_info.login_name,
            'path': self.obj.connection_info.path,
            'connection_mode': self.obj.connection_info.connection_mode
        }
        return props

    def get_properties(self):
        """
        Return dict with properties required for connector type
        """

        props = {
            'host': self.obj.connection_info.host,
            'username': self.obj.connection_info.login_name,
            'connectorName': self.obj.connector_name,
            'password': self.obj.connection_info.password,
            'fileType': self.obj.file_type,
            'environmentId': self.obj.environment_id,
        }

        empty = 0
        for k in props.keys():
            if (props[k] is None):
                print_error("Property %s can't be empty" % k)
                empty = empty + 1

        if empty == 0:
            return props
        else:
            return None

    def add(self):
        """
        Add connector to engine
        Return None if OK
        """
        payload_dict = self.get_properties()
        if payload_dict is None:
            print_error('Some required property not found')
            return 1

        try:
            self.__logger.debug("create connector input %s" % str(self))

            api_instance = self.__api(self.__engine.api_client)
            response = api_instance.create_file_connector(
                self.obj,
                _request_timeout=self.__engine.get_timeout())
            self.file_connector_id = response.file_connector_id

            self.__logger.debug("connector response %s"
                                % str(response))

            print_message("Connector %s added" % self.obj.connector_name)
        except ApiException as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1

    def delete(self):
        """
        Delete connector from Masking engine and print status message
        return a None if non error
        return 1 in case of error
        """

        api_instance = self.__api(self.__engine.api_client)

        try:
            self.__logger.debug("delete connector id %s"
                                % self.connectorId)
            response = api_instance.delete_file_connector(
                self.connectorId,
                _request_timeout=self.__engine.get_timeout())
            self.__logger.debug("delete connector response %s"
                                % str(response))
            print_message("Connector %s deleted" % self.connector_name)
        except self.__apiexc as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1

    def update(self):
        """
        Update connector on engine
        Return None if OK
        """

        api_instance = self.__api(self.__engine.api_client)
        body = FileConnector()
        newci = ConnectionInfo()

        print_error("Update of file connector has a API bug - this function doesn't work")
        self.__logger.error("Update of file connector has a API bug")
        return 1

        # for k in self.attribute_map.keys():
        #     if k == 'connection_info':
        #         ci = self.connection_info
        #         for c in ci.attribute_map.keys():
        #             if getattr(ci, c) is not None:
        #                 print "settuje"
        #                 setattr(newci, c, getattr(ci, c))
        #         setattr(body, k, newci)
        #     else:
        #         if getattr(self, k) is not None:
        #             setattr(body, k, getattr(self, k))
        #
        #
        # try:
        #     self.__logger.debug("update connector input %s" % str(self))
        #     response = api_instance.update_file_connector(
        #         self.file_connector_id,
        #         body,
        #         _request_timeout=self.__engine.get_timeout())
        #     self.__logger.debug("update connector response %s"
        #                         % str(response))
        #
        #     self.file_connector_id = response.file_connector_id
        #     print_message("Connector %s updated" % self.connector_name)
        # except self.__apiexc as e:
        #     print_error(e.body)
        #     self.__logger.error(e)
        #     return 1

    def test(self):
        """
        Test connector connection to database
        Return None if OK
        """

        api_instance = self.__api(self.__engine.api_client)

        try:
            self.__logger.debug("test connector id %s"
                                % self.connectorId)

            if (self.__engine.version_ge('6.0.0')):
                response = api_instance.test_file_connector(
                    self.connectorId,
                    body=self.obj,
                    _request_timeout=self.__engine.get_timeout())
            else:
                response = api_instance.test_file_connector(
                    self.connectorId,
                    _request_timeout=self.__engine.get_timeout())
            if response.response == "Connection Failed":
                print_error("Connector test %s failed" % self.connector_name)
                return 1
            else:
                print_message("Connector test %s succeeded"
                              % self.connector_name)
                return 0
        except self.__apiexc as e:
            print_error(e.body)
            self.__logger.error(e)
            return 1

    def fetch_meta(self):
        """
        Fetch list of tables
        Return list if OK
        None if no objects
        """

        api_instance = self.__api(self.__engine.api_client)

        try:
            self.__logger.debug("fetch connector id %s"
                                % self.connectorId)
            response = api_instance.fetch_file_metadata(
                self.connectorId,
                _request_timeout=self.__engine.get_timeout())
            self.__logger.debug("list of files" + str(response))
            return response
        except self.__apiexc as e:
            print_error(e.body)
            self.__logger.error(e)
            return None

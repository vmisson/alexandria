# coding=utf-8

import pprint
import config
import json
import urllib
import requests
import types


class Driver(object):

    def __init__(self):
        self.driver_type = self.__class__.__name__
        # Get credentials from conf files for CMDB
        pass

    def get_driver_type(self):
            return self.driver_type

    def get_ci(self, ci):
        pass

    def push_ci(self, ci):
        pass


class Itop(Driver):

    def get_ci(self, ci):
        print "Get from itop"
        return True

    def push_ci(self, ci):
        username = config.alexandria.conf_file.get_driver_parameters("itop", "loginItop")
        password = config.alexandria.conf_file.get_driver_parameters("itop", "passwordItop")
        config.logger.debug("login : {}, password : {}".format(
                                                               username,
                                                               password
                                                               )
                            )
        # Craft request body and header
        urlbase = "http://10.3.8.40/itop/webservices/rest.php"
        request = '{"operation":"core/update","comment":"boulalala","class":"Server","key":{"name":"Server1"},"output_fields":"id,friendlyname,ram","fields":{"ram":"28"}}'
        
        urlparam = {'version' : '1.0',
                    'auth_user' : username,
                    'auth_pwd' : password,
                    'json_data' : request
                    }
        
        header = {'Content-type': 'application/json'}
        
        url = urlbase + '?' + urllib.urlencode(urlparam)
        
        config.logger.debug(url)
        
        #=======================================================================
        # answer = requests.post(url,
        #                      headers=header,
        #                      verify="False"
        #                     )
        #=======================================================================
        answer = requests.post(url,
                               auth=(username,password)
                               )
        
        config.logger.debug(answer.status_code)
        config.logger.debug(answer.text)
        


class Redfish(Driver):

    def get_ci(self,ci):
        print "Get from redfish"
        return True


class Ironic(Driver):
    pass


class Mondorescue(Driver):
    pass


class Fakecmdb(Driver):
    def push_ci(self, ci):
        # Determine ci type so we can do the proper action.
        pp = pprint.PrettyPrinter(indent=4)
        if ci.ci_type == "Manager":
            print "We are in Fakecmdb driver !"
            pp.pprint(ci.data)
            # Simply write a json file with ci.data content.
            with open("Fakecmdb.json", "w") as jsonfile:
                json.dump(ci.data, jsonfile, indent=4)
            jsonfile.close()

        #
        #=======================================================================

class Fakeprovider(Driver):

    def get_ci(self, ci):
        # Simulate a driver that will provide Manager data.

        # TODO a connect method must be implemented

        # Assuming the connection is ok.

        # Now create a copy of manager model from reference model.
        ci.ci_type = "Manager"
        ci.data = config.alexandria.model.get_model("Manager")

        # Update the structure with data
        # TODO : think to encapsulate to not edit ci.data directly.
        #        This could be also a way to check source of truth.
        #        If data provided by our driver is not the source of truth
        #        then discard it.


        ci.data["ManagerType"] = "BMC"
        ci.data["Model"] = "Néné Manager"
        ci.data["FirmwareVersion"] = "1.00"




        #if ci.data is config.alexandria.model.Manager:
        #    print "identical"

        pp = pprint.PrettyPrinter(indent=4)

        pp.pprint(ci.ci_type)


class DriverCollection(list):
    pass

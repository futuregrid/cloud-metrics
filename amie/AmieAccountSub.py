#!/usr/bin/env python

#
# Generated Sat Aug 11 13:45:05 2012 by generateDS.py version 2.7c.
#

import sys

import AmieAccount as supermod

etree_ = None
Verbose_import_ = False
(   XMLParser_import_none, XMLParser_import_lxml,
    XMLParser_import_elementtree
    ) = range(3)
XMLParser_import_library = None
try:
    # lxml
    from lxml import etree as etree_
    XMLParser_import_library = XMLParser_import_lxml
    if Verbose_import_:
        print("running with lxml.etree")
except ImportError:
    try:
        # cElementTree from Python 2.5+
        import xml.etree.cElementTree as etree_
        XMLParser_import_library = XMLParser_import_elementtree
        if Verbose_import_:
            print("running with cElementTree on Python 2.5+")
    except ImportError:
        try:
            # ElementTree from Python 2.5+
            import xml.etree.ElementTree as etree_
            XMLParser_import_library = XMLParser_import_elementtree
            if Verbose_import_:
                print("running with ElementTree on Python 2.5+")
        except ImportError:
            try:
                # normal cElementTree install
                import cElementTree as etree_
                XMLParser_import_library = XMLParser_import_elementtree
                if Verbose_import_:
                    print("running with cElementTree")
            except ImportError:
                try:
                    # normal ElementTree install
                    import elementtree.ElementTree as etree_
                    XMLParser_import_library = XMLParser_import_elementtree
                    if Verbose_import_:
                        print("running with ElementTree")
                except ImportError:
                    raise ImportError("Failed to import ElementTree from any known place")

def parsexml_(*args, **kwargs):
    if (XMLParser_import_library == XMLParser_import_lxml and
        'parser' not in kwargs):
        # Use the lxml ElementTree compatible parser so that, e.g.,
        #   we ignore comments.
        kwargs['parser'] = etree_.ETCompatXMLParser()
    doc = etree_.parse(*args, **kwargs)
    return doc

#
# Globals
#

ExternalEncoding = 'ascii'

#
# Data representation classes
#

class header_typeSub(supermod.header_type):
    def __init__(self, from_site_name=None, to_site_name=None, originating_site_name=None, transaction_id=None, packet_id=None, expected_reply_list=None, date=None):
        super(header_typeSub, self).__init__(from_site_name, to_site_name, originating_site_name, transaction_id, packet_id, expected_reply_list, date, )
supermod.header_type.subclass = header_typeSub
# end class header_typeSub


class amieSub(supermod.amie):
    def __init__(self, version=None, request_project_create=None, notify_project_create=None, data_project_create=None, request_account_create=None, notify_account_create=None, data_account_create=None, request_project_resources=None, notify_project_resources=None, request_project_modify=None, notify_project_modify=None, request_user_modify=None, notify_user_modify=None, request_project_inactivate=None, notify_project_inactivate=None, request_project_reactivate=None, notify_project_reactivate=None, request_account_inactivate=None, notify_account_inactivate=None, request_account_reactivate=None, notify_account_reactivate=None, request_user_suspend=None, notify_user_suspend=None, request_user_reactivate=None, notify_user_reactivate=None, notify_project_usage=None, request_user_create=None, notify_user_create=None, notify_person_ids=None, request_person_merge=None, notify_person_duplicate=None, inform_transaction_complete=None, response=None):
        super(amieSub, self).__init__(version, request_project_create, notify_project_create, data_project_create, request_account_create, notify_account_create, data_account_create, request_project_resources, notify_project_resources, request_project_modify, notify_project_modify, request_user_modify, notify_user_modify, request_project_inactivate, notify_project_inactivate, request_project_reactivate, notify_project_reactivate, request_account_inactivate, notify_account_inactivate, request_account_reactivate, notify_account_reactivate, request_user_suspend, notify_user_suspend, request_user_reactivate, notify_user_reactivate, notify_project_usage, request_user_create, notify_user_create, notify_person_ids, request_person_merge, notify_person_duplicate, inform_transaction_complete, response, )
supermod.amie.subclass = amieSub
# end class amieSub


class response_header_typeSub(supermod.response_header_type):
    def __init__(self, from_site_name=None, to_site_name=None, originating_site_name=None, transaction_id=None, packet_id=None, date=None, status_code=None, detail_code=None, message=None):
        super(response_header_typeSub, self).__init__(from_site_name, to_site_name, originating_site_name, transaction_id, packet_id, date, status_code, detail_code, message, )
supermod.response_header_type.subclass = response_header_typeSub
# end class response_header_typeSub


class expected_reply_listSub(supermod.expected_reply_list):
    def __init__(self, expected_reply=None):
        super(expected_reply_listSub, self).__init__(expected_reply, )
supermod.expected_reply_list.subclass = expected_reply_listSub
# end class expected_reply_listSub


class expected_reply_typeSub(supermod.expected_reply_type):
    def __init__(self, type_=None, timeout=None):
        super(expected_reply_typeSub, self).__init__(type_, timeout, )
supermod.expected_reply_type.subclass = expected_reply_typeSub
# end class expected_reply_typeSub


class addressSub(supermod.address):
    def __init__(self, off_address=None, str_address=None, str_address2=None, city=None, state=None, zip=None, country=None):
        super(addressSub, self).__init__(off_address, str_address, str_address2, city, state, zip, country, )
supermod.address.subclass = addressSub
# end class addressSub


class reasonSub(supermod.reason):
    def __init__(self, reason_code=None, description=None):
        super(reasonSub, self).__init__(reason_code, description, )
supermod.reason.subclass = reasonSub
# end class reasonSub


class field_of_science_typeSub(supermod.field_of_science_type):
    def __init__(self, number=None, abbr=None, description=None):
        super(field_of_science_typeSub, self).__init__(number, abbr, description, )
supermod.field_of_science_type.subclass = field_of_science_typeSub
# end class field_of_science_typeSub


class person_typeSub(supermod.person_type):
    def __init__(self, last_name=None, first_name=None, middle_name=None, email=None, title=None, organization=None, citizenship=None, country_access=None, address=None, business_phone=None, home_phone=None, fax=None, org_code=None, emp_code=None, dept=None, position=None, person_id=None, uid=None, global_id=None):
        super(person_typeSub, self).__init__(last_name, first_name, middle_name, email, title, organization, citizenship, country_access, address, business_phone, home_phone, fax, org_code, emp_code, dept, position, person_id, uid, global_id, )
supermod.person_type.subclass = person_typeSub
# end class person_typeSub


class phone_typeSub(supermod.phone_type):
    def __init__(self, number=None, extension=None, comment=None):
        super(phone_typeSub, self).__init__(number, extension, comment, )
supermod.phone_type.subclass = phone_typeSub
# end class phone_typeSub


class site_person_id_listSub(supermod.site_person_id_list):
    def __init__(self, site_person_id=None):
        super(site_person_id_listSub, self).__init__(site_person_id, )
supermod.site_person_id_list.subclass = site_person_id_listSub
# end class site_person_id_listSub


class site_person_id_typeSub(supermod.site_person_id_type):
    def __init__(self, site=None, person_id=None):
        super(site_person_id_typeSub, self).__init__(site, person_id, )
supermod.site_person_id_type.subclass = site_person_id_typeSub
# end class site_person_id_typeSub


class host_info_typeSub(supermod.host_info_type):
    def __init__(self, host=None, mb_reserved_memory=None, processors=None):
        super(host_info_typeSub, self).__init__(host, mb_reserved_memory, processors, )
supermod.host_info_type.subclass = host_info_typeSub
# end class host_info_typeSub


class attribute_typeSub(supermod.attribute_type):
    def __init__(self, name=None, value=None):
        super(attribute_typeSub, self).__init__(name, value, )
supermod.attribute_type.subclass = attribute_typeSub
# end class attribute_typeSub


class resource_login_typeSub(supermod.resource_login_type):
    def __init__(self, resource=None, login=None, uid=None):
        super(resource_login_typeSub, self).__init__(resource, login, uid, )
supermod.resource_login_type.subclass = resource_login_typeSub
# end class resource_login_typeSub


class request_project_createTypeSub(supermod.request_project_createType):
    def __init__(self, header=None, body=None):
        super(request_project_createTypeSub, self).__init__(header, body, )
supermod.request_project_createType.subclass = request_project_createTypeSub
# end class request_project_createTypeSub


class bodyTypeSub(supermod.bodyType):
    def __init__(self, record_id=None, project_id=None, alloc_type=None, su_alloc=None, pi=None, site_person_id_list=None, start_date=None, end_date=None, project_title=None, pfos=None, sfos_list=None, resource_list=None, alloc_resource=None, charge_num=None, grant_num=None, grant_type=None, proposal_num=None, abstract=None, sector=None, qualifications=None, methodologies=None, support=None, other_resources=None, statement_work=None, background=None, justification=None, deliverables=None, milestones=None, progress=None, facilities=None, languages=None, applications=None, diskspace=None, memory=None, processors=None, nsf_status_code=None, comment=None, role_list=None):
        super(bodyTypeSub, self).__init__(record_id, project_id, alloc_type, su_alloc, pi, site_person_id_list, start_date, end_date, project_title, pfos, sfos_list, resource_list, alloc_resource, charge_num, grant_num, grant_type, proposal_num, abstract, sector, qualifications, methodologies, support, other_resources, statement_work, background, justification, deliverables, milestones, progress, facilities, languages, applications, diskspace, memory, processors, nsf_status_code, comment, role_list, )
supermod.bodyType.subclass = bodyTypeSub
# end class bodyTypeSub


class piTypeSub(supermod.piType):
    def __init__(self, personal_info=None, dn_list=None, remote_site_id=None, remote_site_login=None, requester_login=None, req_login_list=None):
        super(piTypeSub, self).__init__(personal_info, dn_list, remote_site_id, remote_site_login, requester_login, req_login_list, )
supermod.piType.subclass = piTypeSub
# end class piTypeSub


class dn_listTypeSub(supermod.dn_listType):
    def __init__(self, dn=None):
        super(dn_listTypeSub, self).__init__(dn, )
supermod.dn_listType.subclass = dn_listTypeSub
# end class dn_listTypeSub


class req_login_listTypeSub(supermod.req_login_listType):
    def __init__(self, req_login=None):
        super(req_login_listTypeSub, self).__init__(req_login, )
supermod.req_login_listType.subclass = req_login_listTypeSub
# end class req_login_listTypeSub


class sfos_listTypeSub(supermod.sfos_listType):
    def __init__(self, sfos=None):
        super(sfos_listTypeSub, self).__init__(sfos, )
supermod.sfos_listType.subclass = sfos_listTypeSub
# end class sfos_listTypeSub


class resource_listTypeSub(supermod.resource_listType):
    def __init__(self, resource=None):
        super(resource_listTypeSub, self).__init__(resource, )
supermod.resource_listType.subclass = resource_listTypeSub
# end class resource_listTypeSub


class role_listTypeSub(supermod.role_listType):
    def __init__(self, role=None):
        super(role_listTypeSub, self).__init__(role, )
supermod.role_listType.subclass = role_listTypeSub
# end class role_listTypeSub


class notify_project_createTypeSub(supermod.notify_project_createType):
    def __init__(self, header=None, body=None):
        super(notify_project_createTypeSub, self).__init__(header, body, )
supermod.notify_project_createType.subclass = notify_project_createTypeSub
# end class notify_project_createTypeSub


class bodyType1Sub(supermod.bodyType1):
    def __init__(self, record_id=None, project_id=None, project_gid=None, alloc_type=None, su_alloc=None, pi=None, start_date=None, end_date=None, project_title=None, pfos=None, sfos_list=None, resource_list=None, resource_login_list=None, grant_num=None, grant_type=None, proposal_num=None, abstract=None, sector=None, qualifications=None, methodologies=None, support=None, other_resources=None, statement_work=None, background=None, justification=None, deliverables=None, milestones=None, progress=None, facilities=None, languages=None, applications=None, diskspace=None, memory=None, processors=None, nsf_status_code=None, comment=None, account_activity_time=None, board_type=None, role_list=None):
        super(bodyType1Sub, self).__init__(record_id, project_id, project_gid, alloc_type, su_alloc, pi, start_date, end_date, project_title, pfos, sfos_list, resource_list, resource_login_list, grant_num, grant_type, proposal_num, abstract, sector, qualifications, methodologies, support, other_resources, statement_work, background, justification, deliverables, milestones, progress, facilities, languages, applications, diskspace, memory, processors, nsf_status_code, comment, account_activity_time, board_type, role_list, )
supermod.bodyType1.subclass = bodyType1Sub
# end class bodyType1Sub


class piType1Sub(supermod.piType1):
    def __init__(self, personal_info=None, dn_list=None, notifier_login=None, remote_site_login=None, req_login_list=None):
        super(piType1Sub, self).__init__(personal_info, dn_list, notifier_login, remote_site_login, req_login_list, )
supermod.piType1.subclass = piType1Sub
# end class piType1Sub


class dn_listType1Sub(supermod.dn_listType1):
    def __init__(self, dn=None):
        super(dn_listType1Sub, self).__init__(dn, )
supermod.dn_listType1.subclass = dn_listType1Sub
# end class dn_listType1Sub


class req_login_listType1Sub(supermod.req_login_listType1):
    def __init__(self, req_login=None):
        super(req_login_listType1Sub, self).__init__(req_login, )
supermod.req_login_listType1.subclass = req_login_listType1Sub
# end class req_login_listType1Sub


class sfos_listType1Sub(supermod.sfos_listType1):
    def __init__(self, sfos=None):
        super(sfos_listType1Sub, self).__init__(sfos, )
supermod.sfos_listType1.subclass = sfos_listType1Sub
# end class sfos_listType1Sub


class resource_listType1Sub(supermod.resource_listType1):
    def __init__(self, resource=None):
        super(resource_listType1Sub, self).__init__(resource, )
supermod.resource_listType1.subclass = resource_listType1Sub
# end class resource_listType1Sub


class resource_login_listTypeSub(supermod.resource_login_listType):
    def __init__(self, resource_login=None):
        super(resource_login_listTypeSub, self).__init__(resource_login, )
supermod.resource_login_listType.subclass = resource_login_listTypeSub
# end class resource_login_listTypeSub


class role_listType1Sub(supermod.role_listType1):
    def __init__(self, role=None):
        super(role_listType1Sub, self).__init__(role, )
supermod.role_listType1.subclass = role_listType1Sub
# end class role_listType1Sub


class data_project_createTypeSub(supermod.data_project_createType):
    def __init__(self, header=None, body=None):
        super(data_project_createTypeSub, self).__init__(header, body, )
supermod.data_project_createType.subclass = data_project_createTypeSub
# end class data_project_createTypeSub


class bodyType2Sub(supermod.bodyType2):
    def __init__(self, dn_list=None, project_id=None, person_id=None, global_id=None, comment=None):
        super(bodyType2Sub, self).__init__(dn_list, project_id, person_id, global_id, comment, )
supermod.bodyType2.subclass = bodyType2Sub
# end class bodyType2Sub


class dn_listType2Sub(supermod.dn_listType2):
    def __init__(self, dn=None):
        super(dn_listType2Sub, self).__init__(dn, )
supermod.dn_listType2.subclass = dn_listType2Sub
# end class dn_listType2Sub


class request_account_createTypeSub(supermod.request_account_createType):
    def __init__(self, header=None, body=None):
        super(request_account_createTypeSub, self).__init__(header, body, )
supermod.request_account_createType.subclass = request_account_createTypeSub
# end class request_account_createTypeSub


class bodyType3Sub(supermod.bodyType3):
    def __init__(self, project_id=None, grant_num=None, alloc_resource=None, resource_list=None, user=None, site_person_id_list=None, nsf_status_code=None, comment=None, role_list=None):
        super(bodyType3Sub, self).__init__(project_id, grant_num, alloc_resource, resource_list, user, site_person_id_list, nsf_status_code, comment, role_list, )
supermod.bodyType3.subclass = bodyType3Sub
# end class bodyType3Sub


class resource_listType2Sub(supermod.resource_listType2):
    def __init__(self, resource=None):
        super(resource_listType2Sub, self).__init__(resource, )
supermod.resource_listType2.subclass = resource_listType2Sub
# end class resource_listType2Sub


class userTypeSub(supermod.userType):
    def __init__(self, personal_info=None, dn_list=None, password_access_enable=None, remote_site_id=None, remote_site_login=None, requester_login=None, req_login_list=None, role=None):
        super(userTypeSub, self).__init__(personal_info, dn_list, password_access_enable, remote_site_id, remote_site_login, requester_login, req_login_list, role, )
supermod.userType.subclass = userTypeSub
# end class userTypeSub


class dn_listType3Sub(supermod.dn_listType3):
    def __init__(self, dn=None):
        super(dn_listType3Sub, self).__init__(dn, )
supermod.dn_listType3.subclass = dn_listType3Sub
# end class dn_listType3Sub


class req_login_listType2Sub(supermod.req_login_listType2):
    def __init__(self, req_login=None):
        super(req_login_listType2Sub, self).__init__(req_login, )
supermod.req_login_listType2.subclass = req_login_listType2Sub
# end class req_login_listType2Sub


class role_listType2Sub(supermod.role_listType2):
    def __init__(self, role=None):
        super(role_listType2Sub, self).__init__(role, )
supermod.role_listType2.subclass = role_listType2Sub
# end class role_listType2Sub


class notify_account_createTypeSub(supermod.notify_account_createType):
    def __init__(self, header=None, body=None):
        super(notify_account_createTypeSub, self).__init__(header, body, )
supermod.notify_account_createType.subclass = notify_account_createTypeSub
# end class notify_account_createTypeSub


class bodyType4Sub(supermod.bodyType4):
    def __init__(self, project_id=None, resource_list=None, resource_login_list=None, user=None, nsf_status_code=None, comment=None, start_date=None, account_activity_time=None, role_list=None):
        super(bodyType4Sub, self).__init__(project_id, resource_list, resource_login_list, user, nsf_status_code, comment, start_date, account_activity_time, role_list, )
supermod.bodyType4.subclass = bodyType4Sub
# end class bodyType4Sub


class resource_listType3Sub(supermod.resource_listType3):
    def __init__(self, resource=None):
        super(resource_listType3Sub, self).__init__(resource, )
supermod.resource_listType3.subclass = resource_listType3Sub
# end class resource_listType3Sub


class resource_login_listType1Sub(supermod.resource_login_listType1):
    def __init__(self, resource_login=None):
        super(resource_login_listType1Sub, self).__init__(resource_login, )
supermod.resource_login_listType1.subclass = resource_login_listType1Sub
# end class resource_login_listType1Sub


class userType1Sub(supermod.userType1):
    def __init__(self, personal_info=None, password_access_enable=None, dn_list=None, notifier_login=None, remote_site_login=None, req_login_list=None, role=None):
        super(userType1Sub, self).__init__(personal_info, password_access_enable, dn_list, notifier_login, remote_site_login, req_login_list, role, )
supermod.userType1.subclass = userType1Sub
# end class userType1Sub


class dn_listType4Sub(supermod.dn_listType4):
    def __init__(self, dn=None):
        super(dn_listType4Sub, self).__init__(dn, )
supermod.dn_listType4.subclass = dn_listType4Sub
# end class dn_listType4Sub


class req_login_listType3Sub(supermod.req_login_listType3):
    def __init__(self, req_login=None):
        super(req_login_listType3Sub, self).__init__(req_login, )
supermod.req_login_listType3.subclass = req_login_listType3Sub
# end class req_login_listType3Sub


class role_listType3Sub(supermod.role_listType3):
    def __init__(self, role=None):
        super(role_listType3Sub, self).__init__(role, )
supermod.role_listType3.subclass = role_listType3Sub
# end class role_listType3Sub


class data_account_createTypeSub(supermod.data_account_createType):
    def __init__(self, header=None, body=None):
        super(data_account_createTypeSub, self).__init__(header, body, )
supermod.data_account_createType.subclass = data_account_createTypeSub
# end class data_account_createTypeSub


class bodyType5Sub(supermod.bodyType5):
    def __init__(self, dn_list=None, project_id=None, person_id=None, global_id=None, comment=None):
        super(bodyType5Sub, self).__init__(dn_list, project_id, person_id, global_id, comment, )
supermod.bodyType5.subclass = bodyType5Sub
# end class bodyType5Sub


class dn_listType5Sub(supermod.dn_listType5):
    def __init__(self, dn=None):
        super(dn_listType5Sub, self).__init__(dn, )
supermod.dn_listType5.subclass = dn_listType5Sub
# end class dn_listType5Sub


class request_project_resourcesTypeSub(supermod.request_project_resourcesType):
    def __init__(self, header=None, body=None):
        super(request_project_resourcesTypeSub, self).__init__(header, body, )
supermod.request_project_resourcesType.subclass = request_project_resourcesTypeSub
# end class request_project_resourcesTypeSub


class bodyType6Sub(supermod.bodyType6):
    def __init__(self, project_id=None, resource_list=None, changed_field_option=None, comment=None):
        super(bodyType6Sub, self).__init__(project_id, resource_list, changed_field_option, comment, )
supermod.bodyType6.subclass = bodyType6Sub
# end class bodyType6Sub


class resource_listType4Sub(supermod.resource_listType4):
    def __init__(self, resource=None):
        super(resource_listType4Sub, self).__init__(resource, )
supermod.resource_listType4.subclass = resource_listType4Sub
# end class resource_listType4Sub


class changed_field_optionTypeSub(supermod.changed_field_optionType):
    def __init__(self, su_alloc_info=None, end_date=None):
        super(changed_field_optionTypeSub, self).__init__(su_alloc_info, end_date, )
supermod.changed_field_optionType.subclass = changed_field_optionTypeSub
# end class changed_field_optionTypeSub


class su_alloc_infoTypeSub(supermod.su_alloc_infoType):
    def __init__(self, su_alloc=None, alloc_change=None, effective_date=None):
        super(su_alloc_infoTypeSub, self).__init__(su_alloc, alloc_change, effective_date, )
supermod.su_alloc_infoType.subclass = su_alloc_infoTypeSub
# end class su_alloc_infoTypeSub


class notify_project_resourcesTypeSub(supermod.notify_project_resourcesType):
    def __init__(self, header=None, body=None):
        super(notify_project_resourcesTypeSub, self).__init__(header, body, )
supermod.notify_project_resourcesType.subclass = notify_project_resourcesTypeSub
# end class notify_project_resourcesTypeSub


class bodyType7Sub(supermod.bodyType7):
    def __init__(self, project_id=None, resource_list=None, changed_field_option=None, comment=None):
        super(bodyType7Sub, self).__init__(project_id, resource_list, changed_field_option, comment, )
supermod.bodyType7.subclass = bodyType7Sub
# end class bodyType7Sub


class resource_listType5Sub(supermod.resource_listType5):
    def __init__(self, resource=None):
        super(resource_listType5Sub, self).__init__(resource, )
supermod.resource_listType5.subclass = resource_listType5Sub
# end class resource_listType5Sub


class changed_field_optionType1Sub(supermod.changed_field_optionType1):
    def __init__(self, su_alloc_info=None, end_date=None):
        super(changed_field_optionType1Sub, self).__init__(su_alloc_info, end_date, )
supermod.changed_field_optionType1.subclass = changed_field_optionType1Sub
# end class changed_field_optionType1Sub


class su_alloc_infoType1Sub(supermod.su_alloc_infoType1):
    def __init__(self, su_alloc=None, alloc_change=None, effective_date=None):
        super(su_alloc_infoType1Sub, self).__init__(su_alloc, alloc_change, effective_date, )
supermod.su_alloc_infoType1.subclass = su_alloc_infoType1Sub
# end class su_alloc_infoType1Sub


class request_project_modifyTypeSub(supermod.request_project_modifyType):
    def __init__(self, header=None, body=None):
        super(request_project_modifyTypeSub, self).__init__(header, body, )
supermod.request_project_modifyType.subclass = request_project_modifyTypeSub
# end class request_project_modifyTypeSub


class bodyType8Sub(supermod.bodyType8):
    def __init__(self, action_type=None, project_id=None, resource_list=None, project_title=None, pfos=None, sfos_list=None, abstract=None, sector=None, qualifications=None, methodologies=None, support=None, other_resources=None, statement_work=None, background=None, justification=None, deliverables=None, milestones=None, progress=None, facilities=None, languages=None, applications=None, diskspace=None, memory=None, processors=None, comment=None, pi_person_id=None):
        super(bodyType8Sub, self).__init__(action_type, project_id, resource_list, project_title, pfos, sfos_list, abstract, sector, qualifications, methodologies, support, other_resources, statement_work, background, justification, deliverables, milestones, progress, facilities, languages, applications, diskspace, memory, processors, comment, pi_person_id, )
supermod.bodyType8.subclass = bodyType8Sub
# end class bodyType8Sub


class resource_listType6Sub(supermod.resource_listType6):
    def __init__(self, resource=None):
        super(resource_listType6Sub, self).__init__(resource, )
supermod.resource_listType6.subclass = resource_listType6Sub
# end class resource_listType6Sub


class sfos_listType2Sub(supermod.sfos_listType2):
    def __init__(self, sfos=None):
        super(sfos_listType2Sub, self).__init__(sfos, )
supermod.sfos_listType2.subclass = sfos_listType2Sub
# end class sfos_listType2Sub


class notify_project_modifyTypeSub(supermod.notify_project_modifyType):
    def __init__(self, header=None, body=None):
        super(notify_project_modifyTypeSub, self).__init__(header, body, )
supermod.notify_project_modifyType.subclass = notify_project_modifyTypeSub
# end class notify_project_modifyTypeSub


class bodyType9Sub(supermod.bodyType9):
    def __init__(self, action_type=None, project_id=None, resource_list=None, project_title=None, pfos=None, sfos_list=None, abstract=None, sector=None, qualifications=None, methodologies=None, support=None, other_resources=None, statement_work=None, background=None, justification=None, deliverables=None, milestones=None, progress=None, facilities=None, languages=None, applications=None, diskspace=None, memory=None, processors=None, comment=None, pi_person_id=None):
        super(bodyType9Sub, self).__init__(action_type, project_id, resource_list, project_title, pfos, sfos_list, abstract, sector, qualifications, methodologies, support, other_resources, statement_work, background, justification, deliverables, milestones, progress, facilities, languages, applications, diskspace, memory, processors, comment, pi_person_id, )
supermod.bodyType9.subclass = bodyType9Sub
# end class bodyType9Sub


class resource_listType7Sub(supermod.resource_listType7):
    def __init__(self, resource=None):
        super(resource_listType7Sub, self).__init__(resource, )
supermod.resource_listType7.subclass = resource_listType7Sub
# end class resource_listType7Sub


class sfos_listType3Sub(supermod.sfos_listType3):
    def __init__(self, sfos=None):
        super(sfos_listType3Sub, self).__init__(sfos, )
supermod.sfos_listType3.subclass = sfos_listType3Sub
# end class sfos_listType3Sub


class request_user_modifyTypeSub(supermod.request_user_modifyType):
    def __init__(self, header=None, body=None):
        super(request_user_modifyTypeSub, self).__init__(header, body, )
supermod.request_user_modifyType.subclass = request_user_modifyTypeSub
# end class request_user_modifyTypeSub


class bodyType10Sub(supermod.bodyType10):
    def __init__(self, action_type=None, person_id=None, dn_list=None, new_dn=None, valid_cert=False, first_name=None, middle_name=None, last_name=None, email=None, fax=None, title=None, organization=None, citizenship=None, country_access=None, org_code=None, emp_code=None, dept=None, address=None, home_phone=None, business_phone=None, remote_site_login=None, requester_login=None, req_login_list=None, comment=None, position=None, nsf_status_code=None):
        super(bodyType10Sub, self).__init__(action_type, person_id, dn_list, new_dn, valid_cert, first_name, middle_name, last_name, email, fax, title, organization, citizenship, country_access, org_code, emp_code, dept, address, home_phone, business_phone, remote_site_login, requester_login, req_login_list, comment, position, nsf_status_code, )
supermod.bodyType10.subclass = bodyType10Sub
# end class bodyType10Sub


class dn_listType6Sub(supermod.dn_listType6):
    def __init__(self, dn=None):
        super(dn_listType6Sub, self).__init__(dn, )
supermod.dn_listType6.subclass = dn_listType6Sub
# end class dn_listType6Sub


class req_login_listType4Sub(supermod.req_login_listType4):
    def __init__(self, req_login=None):
        super(req_login_listType4Sub, self).__init__(req_login, )
supermod.req_login_listType4.subclass = req_login_listType4Sub
# end class req_login_listType4Sub


class notify_user_modifyTypeSub(supermod.notify_user_modifyType):
    def __init__(self, header=None, body=None):
        super(notify_user_modifyTypeSub, self).__init__(header, body, )
supermod.notify_user_modifyType.subclass = notify_user_modifyTypeSub
# end class notify_user_modifyTypeSub


class bodyType11Sub(supermod.bodyType11):
    def __init__(self, action_type=None, person_id=None, dn_list=None, new_dn=None, valid_cert=False, first_name=None, middle_name=None, last_name=None, email=None, fax=None, title=None, organization=None, citizenship=None, country_access=None, org_code=None, emp_code=None, dept=None, address=None, home_phone=None, business_phone=None, notifier_login=None, remote_site_login=None, req_login_list=None, comment=None, position=None):
        super(bodyType11Sub, self).__init__(action_type, person_id, dn_list, new_dn, valid_cert, first_name, middle_name, last_name, email, fax, title, organization, citizenship, country_access, org_code, emp_code, dept, address, home_phone, business_phone, notifier_login, remote_site_login, req_login_list, comment, position, )
supermod.bodyType11.subclass = bodyType11Sub
# end class bodyType11Sub


class dn_listType7Sub(supermod.dn_listType7):
    def __init__(self, dn=None):
        super(dn_listType7Sub, self).__init__(dn, )
supermod.dn_listType7.subclass = dn_listType7Sub
# end class dn_listType7Sub


class req_login_listType5Sub(supermod.req_login_listType5):
    def __init__(self, req_login=None):
        super(req_login_listType5Sub, self).__init__(req_login, )
supermod.req_login_listType5.subclass = req_login_listType5Sub
# end class req_login_listType5Sub


class request_project_inactivateTypeSub(supermod.request_project_inactivateType):
    def __init__(self, header=None, body=None):
        super(request_project_inactivateTypeSub, self).__init__(header, body, )
supermod.request_project_inactivateType.subclass = request_project_inactivateTypeSub
# end class request_project_inactivateTypeSub


class bodyType12Sub(supermod.bodyType12):
    def __init__(self, project_id=None, resource_list=None, comment=None, start_date=None, end_date=None, grant_num=None, alloc_resource=None, su_alloc=None, su_remain=None):
        super(bodyType12Sub, self).__init__(project_id, resource_list, comment, start_date, end_date, grant_num, alloc_resource, su_alloc, su_remain, )
supermod.bodyType12.subclass = bodyType12Sub
# end class bodyType12Sub


class resource_listType8Sub(supermod.resource_listType8):
    def __init__(self, resource=None):
        super(resource_listType8Sub, self).__init__(resource, )
supermod.resource_listType8.subclass = resource_listType8Sub
# end class resource_listType8Sub


class notify_project_inactivateTypeSub(supermod.notify_project_inactivateType):
    def __init__(self, header=None, body=None):
        super(notify_project_inactivateTypeSub, self).__init__(header, body, )
supermod.notify_project_inactivateType.subclass = notify_project_inactivateTypeSub
# end class notify_project_inactivateTypeSub


class bodyType13Sub(supermod.bodyType13):
    def __init__(self, project_id=None, resource_list=None, comment=None, account_activity_time=None):
        super(bodyType13Sub, self).__init__(project_id, resource_list, comment, account_activity_time, )
supermod.bodyType13.subclass = bodyType13Sub
# end class bodyType13Sub


class resource_listType9Sub(supermod.resource_listType9):
    def __init__(self, resource=None):
        super(resource_listType9Sub, self).__init__(resource, )
supermod.resource_listType9.subclass = resource_listType9Sub
# end class resource_listType9Sub


class request_project_reactivateTypeSub(supermod.request_project_reactivateType):
    def __init__(self, header=None, body=None):
        super(request_project_reactivateTypeSub, self).__init__(header, body, )
supermod.request_project_reactivateType.subclass = request_project_reactivateTypeSub
# end class request_project_reactivateTypeSub


class bodyType14Sub(supermod.bodyType14):
    def __init__(self, project_id=None, resource_list=None, person_id=None, comment=None, start_date=None, end_date=None, grant_num=None, alloc_resource=None, su_alloc=None, su_remain=None):
        super(bodyType14Sub, self).__init__(project_id, resource_list, person_id, comment, start_date, end_date, grant_num, alloc_resource, su_alloc, su_remain, )
supermod.bodyType14.subclass = bodyType14Sub
# end class bodyType14Sub


class resource_listType10Sub(supermod.resource_listType10):
    def __init__(self, resource=None):
        super(resource_listType10Sub, self).__init__(resource, )
supermod.resource_listType10.subclass = resource_listType10Sub
# end class resource_listType10Sub


class notify_project_reactivateTypeSub(supermod.notify_project_reactivateType):
    def __init__(self, header=None, body=None):
        super(notify_project_reactivateTypeSub, self).__init__(header, body, )
supermod.notify_project_reactivateType.subclass = notify_project_reactivateTypeSub
# end class notify_project_reactivateTypeSub


class bodyType15Sub(supermod.bodyType15):
    def __init__(self, project_id=None, resource_list=None, comment=None, account_activity_time=None):
        super(bodyType15Sub, self).__init__(project_id, resource_list, comment, account_activity_time, )
supermod.bodyType15.subclass = bodyType15Sub
# end class bodyType15Sub


class resource_listType11Sub(supermod.resource_listType11):
    def __init__(self, resource=None):
        super(resource_listType11Sub, self).__init__(resource, )
supermod.resource_listType11.subclass = resource_listType11Sub
# end class resource_listType11Sub


class request_account_inactivateTypeSub(supermod.request_account_inactivateType):
    def __init__(self, header=None, body=None):
        super(request_account_inactivateTypeSub, self).__init__(header, body, )
supermod.request_account_inactivateType.subclass = request_account_inactivateTypeSub
# end class request_account_inactivateTypeSub


class bodyType16Sub(supermod.bodyType16):
    def __init__(self, project_id=None, person_id=None, alloc_resource=None, resource_list=None, comment=None, account_activity_time=None):
        super(bodyType16Sub, self).__init__(project_id, person_id, alloc_resource, resource_list, comment, account_activity_time, )
supermod.bodyType16.subclass = bodyType16Sub
# end class bodyType16Sub


class resource_listType12Sub(supermod.resource_listType12):
    def __init__(self, resource=None):
        super(resource_listType12Sub, self).__init__(resource, )
supermod.resource_listType12.subclass = resource_listType12Sub
# end class resource_listType12Sub


class notify_account_inactivateTypeSub(supermod.notify_account_inactivateType):
    def __init__(self, header=None, body=None):
        super(notify_account_inactivateTypeSub, self).__init__(header, body, )
supermod.notify_account_inactivateType.subclass = notify_account_inactivateTypeSub
# end class notify_account_inactivateTypeSub


class bodyType17Sub(supermod.bodyType17):
    def __init__(self, project_id=None, person_id=None, resource_list=None, comment=None, account_activity_time=None):
        super(bodyType17Sub, self).__init__(project_id, person_id, resource_list, comment, account_activity_time, )
supermod.bodyType17.subclass = bodyType17Sub
# end class bodyType17Sub


class resource_listType13Sub(supermod.resource_listType13):
    def __init__(self, resource=None):
        super(resource_listType13Sub, self).__init__(resource, )
supermod.resource_listType13.subclass = resource_listType13Sub
# end class resource_listType13Sub


class request_account_reactivateTypeSub(supermod.request_account_reactivateType):
    def __init__(self, header=None, body=None):
        super(request_account_reactivateTypeSub, self).__init__(header, body, )
supermod.request_account_reactivateType.subclass = request_account_reactivateTypeSub
# end class request_account_reactivateTypeSub


class bodyType18Sub(supermod.bodyType18):
    def __init__(self, project_id=None, person_id=None, alloc_resource=None, resource_list=None, comment=None, account_activity_time=None):
        super(bodyType18Sub, self).__init__(project_id, person_id, alloc_resource, resource_list, comment, account_activity_time, )
supermod.bodyType18.subclass = bodyType18Sub
# end class bodyType18Sub


class resource_listType14Sub(supermod.resource_listType14):
    def __init__(self, resource=None):
        super(resource_listType14Sub, self).__init__(resource, )
supermod.resource_listType14.subclass = resource_listType14Sub
# end class resource_listType14Sub


class notify_account_reactivateTypeSub(supermod.notify_account_reactivateType):
    def __init__(self, header=None, body=None):
        super(notify_account_reactivateTypeSub, self).__init__(header, body, )
supermod.notify_account_reactivateType.subclass = notify_account_reactivateTypeSub
# end class notify_account_reactivateTypeSub


class bodyType19Sub(supermod.bodyType19):
    def __init__(self, project_id=None, person_id=None, resource_list=None, comment=None, account_activity_time=None):
        super(bodyType19Sub, self).__init__(project_id, person_id, resource_list, comment, account_activity_time, )
supermod.bodyType19.subclass = bodyType19Sub
# end class bodyType19Sub


class resource_listType15Sub(supermod.resource_listType15):
    def __init__(self, resource=None):
        super(resource_listType15Sub, self).__init__(resource, )
supermod.resource_listType15.subclass = resource_listType15Sub
# end class resource_listType15Sub


class request_user_suspendTypeSub(supermod.request_user_suspendType):
    def __init__(self, header=None, body=None):
        super(request_user_suspendTypeSub, self).__init__(header, body, )
supermod.request_user_suspendType.subclass = request_user_suspendTypeSub
# end class request_user_suspendTypeSub


class bodyType20Sub(supermod.bodyType20):
    def __init__(self, project_id=None, dn_list=None, reason=None, comment=None, person_id=None):
        super(bodyType20Sub, self).__init__(project_id, dn_list, reason, comment, person_id, )
supermod.bodyType20.subclass = bodyType20Sub
# end class bodyType20Sub


class dn_listType8Sub(supermod.dn_listType8):
    def __init__(self, dn=None):
        super(dn_listType8Sub, self).__init__(dn, )
supermod.dn_listType8.subclass = dn_listType8Sub
# end class dn_listType8Sub


class notify_user_suspendTypeSub(supermod.notify_user_suspendType):
    def __init__(self, header=None, body=None):
        super(notify_user_suspendTypeSub, self).__init__(header, body, )
supermod.notify_user_suspendType.subclass = notify_user_suspendTypeSub
# end class notify_user_suspendTypeSub


class bodyType21Sub(supermod.bodyType21):
    def __init__(self, project_id=None, dn_list=None, reason=None, comment=None, person_id=None):
        super(bodyType21Sub, self).__init__(project_id, dn_list, reason, comment, person_id, )
supermod.bodyType21.subclass = bodyType21Sub
# end class bodyType21Sub


class dn_listType9Sub(supermod.dn_listType9):
    def __init__(self, dn=None):
        super(dn_listType9Sub, self).__init__(dn, )
supermod.dn_listType9.subclass = dn_listType9Sub
# end class dn_listType9Sub


class request_user_reactivateTypeSub(supermod.request_user_reactivateType):
    def __init__(self, header=None, body=None):
        super(request_user_reactivateTypeSub, self).__init__(header, body, )
supermod.request_user_reactivateType.subclass = request_user_reactivateTypeSub
# end class request_user_reactivateTypeSub


class bodyType22Sub(supermod.bodyType22):
    def __init__(self, project_id=None, dn_list=None, reason=None, comment=None, person_id=None):
        super(bodyType22Sub, self).__init__(project_id, dn_list, reason, comment, person_id, )
supermod.bodyType22.subclass = bodyType22Sub
# end class bodyType22Sub


class dn_listType10Sub(supermod.dn_listType10):
    def __init__(self, dn=None):
        super(dn_listType10Sub, self).__init__(dn, )
supermod.dn_listType10.subclass = dn_listType10Sub
# end class dn_listType10Sub


class notify_user_reactivateTypeSub(supermod.notify_user_reactivateType):
    def __init__(self, header=None, body=None):
        super(notify_user_reactivateTypeSub, self).__init__(header, body, )
supermod.notify_user_reactivateType.subclass = notify_user_reactivateTypeSub
# end class notify_user_reactivateTypeSub


class bodyType23Sub(supermod.bodyType23):
    def __init__(self, project_id=None, dn_list=None, reason=None, comment=None, person_id=None):
        super(bodyType23Sub, self).__init__(project_id, dn_list, reason, comment, person_id, )
supermod.bodyType23.subclass = bodyType23Sub
# end class bodyType23Sub


class dn_listType11Sub(supermod.dn_listType11):
    def __init__(self, dn=None):
        super(dn_listType11Sub, self).__init__(dn, )
supermod.dn_listType11.subclass = dn_listType11Sub
# end class dn_listType11Sub


class notify_project_usageTypeSub(supermod.notify_project_usageType):
    def __init__(self, header=None, body=None):
        super(notify_project_usageTypeSub, self).__init__(header, body, )
supermod.notify_project_usageType.subclass = notify_project_usageTypeSub
# end class notify_project_usageTypeSub


class bodyType24Sub(supermod.bodyType24):
    def __init__(self, usage_type=None, project_id=None, machine_name=None, record_identity=None, start_time=None, end_time=None, job_identity=None, user_login=None, job_name=None, charge=None, wall_duration=None, comment=None, cpu_duration=None, node_count=None, processors=None, submit_host=None, submit_time=None, queue=None, exec_host_list=None, attribute_list=None, bytes_stored=None, bytes_read=None, bytes_written=None, number_of_files=None, files_read=None, files_written=None, user_copies=None, system_copies=None, collection_time=None, collection_interval=None, media_type=None, storage_software=None):
        super(bodyType24Sub, self).__init__(usage_type, project_id, machine_name, record_identity, start_time, end_time, job_identity, user_login, job_name, charge, wall_duration, comment, cpu_duration, node_count, processors, submit_host, submit_time, queue, exec_host_list, attribute_list, bytes_stored, bytes_read, bytes_written, number_of_files, files_read, files_written, user_copies, system_copies, collection_time, collection_interval, media_type, storage_software, )
supermod.bodyType24.subclass = bodyType24Sub
# end class bodyType24Sub


class record_identityTypeSub(supermod.record_identityType):
    def __init__(self, record_id=None, create_time=None):
        super(record_identityTypeSub, self).__init__(record_id, create_time, )
supermod.record_identityType.subclass = record_identityTypeSub
# end class record_identityTypeSub


class job_identityTypeSub(supermod.job_identityType):
    def __init__(self, local_job_id=None, global_job_id=None):
        super(job_identityTypeSub, self).__init__(local_job_id, global_job_id, )
supermod.job_identityType.subclass = job_identityTypeSub
# end class job_identityTypeSub


class cpu_durationTypeSub(supermod.cpu_durationType):
    def __init__(self, user=None, system=None):
        super(cpu_durationTypeSub, self).__init__(user, system, )
supermod.cpu_durationType.subclass = cpu_durationTypeSub
# end class cpu_durationTypeSub


class exec_host_listTypeSub(supermod.exec_host_listType):
    def __init__(self, host_info=None):
        super(exec_host_listTypeSub, self).__init__(host_info, )
supermod.exec_host_listType.subclass = exec_host_listTypeSub
# end class exec_host_listTypeSub


class attribute_listTypeSub(supermod.attribute_listType):
    def __init__(self, attribute=None):
        super(attribute_listTypeSub, self).__init__(attribute, )
supermod.attribute_listType.subclass = attribute_listTypeSub
# end class attribute_listTypeSub


class request_user_createTypeSub(supermod.request_user_createType):
    def __init__(self, header=None, body=None):
        super(request_user_createTypeSub, self).__init__(header, body, )
supermod.request_user_createType.subclass = request_user_createTypeSub
# end class request_user_createTypeSub


class bodyType25Sub(supermod.bodyType25):
    def __init__(self, nsf_status_code=None, site_person_id_list=None, user=None):
        super(bodyType25Sub, self).__init__(nsf_status_code, site_person_id_list, user, )
supermod.bodyType25.subclass = bodyType25Sub
# end class bodyType25Sub


class userType2Sub(supermod.userType2):
    def __init__(self, personal_info=None, dn_list=None):
        super(userType2Sub, self).__init__(personal_info, dn_list, )
supermod.userType2.subclass = userType2Sub
# end class userType2Sub


class dn_listType12Sub(supermod.dn_listType12):
    def __init__(self, dn=None):
        super(dn_listType12Sub, self).__init__(dn, )
supermod.dn_listType12.subclass = dn_listType12Sub
# end class dn_listType12Sub


class notify_user_createTypeSub(supermod.notify_user_createType):
    def __init__(self, header=None, body=None):
        super(notify_user_createTypeSub, self).__init__(header, body, )
supermod.notify_user_createType.subclass = notify_user_createTypeSub
# end class notify_user_createTypeSub


class bodyType26Sub(supermod.bodyType26):
    def __init__(self, nsf_status_code=None, site_person_id_list=None, user=None):
        super(bodyType26Sub, self).__init__(nsf_status_code, site_person_id_list, user, )
supermod.bodyType26.subclass = bodyType26Sub
# end class bodyType26Sub


class userType3Sub(supermod.userType3):
    def __init__(self, personal_info=None, dn_list=None):
        super(userType3Sub, self).__init__(personal_info, dn_list, )
supermod.userType3.subclass = userType3Sub
# end class userType3Sub


class dn_listType13Sub(supermod.dn_listType13):
    def __init__(self, dn=None):
        super(dn_listType13Sub, self).__init__(dn, )
supermod.dn_listType13.subclass = dn_listType13Sub
# end class dn_listType13Sub


class notify_person_idsTypeSub(supermod.notify_person_idsType):
    def __init__(self, header=None, body=None):
        super(notify_person_idsTypeSub, self).__init__(header, body, )
supermod.notify_person_idsType.subclass = notify_person_idsTypeSub
# end class notify_person_idsTypeSub


class bodyType27Sub(supermod.bodyType27):
    def __init__(self, person_id=None, primary_person_id=None, person_id_list=None, resource_login_list=None, remove_resource_list=None):
        super(bodyType27Sub, self).__init__(person_id, primary_person_id, person_id_list, resource_login_list, remove_resource_list, )
supermod.bodyType27.subclass = bodyType27Sub
# end class bodyType27Sub


class person_id_listTypeSub(supermod.person_id_listType):
    def __init__(self, person_id=None):
        super(person_id_listTypeSub, self).__init__(person_id, )
supermod.person_id_listType.subclass = person_id_listTypeSub
# end class person_id_listTypeSub


class resource_login_listType2Sub(supermod.resource_login_listType2):
    def __init__(self, resource_login=None):
        super(resource_login_listType2Sub, self).__init__(resource_login, )
supermod.resource_login_listType2.subclass = resource_login_listType2Sub
# end class resource_login_listType2Sub


class remove_resource_listTypeSub(supermod.remove_resource_listType):
    def __init__(self, resource=None):
        super(remove_resource_listTypeSub, self).__init__(resource, )
supermod.remove_resource_listType.subclass = remove_resource_listTypeSub
# end class remove_resource_listTypeSub


class request_person_mergeTypeSub(supermod.request_person_mergeType):
    def __init__(self, header=None, body=None):
        super(request_person_mergeTypeSub, self).__init__(header, body, )
supermod.request_person_mergeType.subclass = request_person_mergeTypeSub
# end class request_person_mergeTypeSub


class bodyType28Sub(supermod.bodyType28):
    def __init__(self, keep_global_id=None, keep_person_id=None, keep_portal_login=None, delete_global_id=None, delete_person_id=None, delete_portal_login=None):
        super(bodyType28Sub, self).__init__(keep_global_id, keep_person_id, keep_portal_login, delete_global_id, delete_person_id, delete_portal_login, )
supermod.bodyType28.subclass = bodyType28Sub
# end class bodyType28Sub


class notify_person_duplicateTypeSub(supermod.notify_person_duplicateType):
    def __init__(self, header=None, body=None):
        super(notify_person_duplicateTypeSub, self).__init__(header, body, )
supermod.notify_person_duplicateType.subclass = notify_person_duplicateTypeSub
# end class notify_person_duplicateTypeSub


class bodyType29Sub(supermod.bodyType29):
    def __init__(self, person_id1=None, person_id2=None, global_id1=None, global_id2=None):
        super(bodyType29Sub, self).__init__(person_id1, person_id2, global_id1, global_id2, )
supermod.bodyType29.subclass = bodyType29Sub
# end class bodyType29Sub


class inform_transaction_completeTypeSub(supermod.inform_transaction_completeType):
    def __init__(self, header=None, body=None):
        super(inform_transaction_completeTypeSub, self).__init__(header, body, )
supermod.inform_transaction_completeType.subclass = inform_transaction_completeTypeSub
# end class inform_transaction_completeTypeSub


class bodyType30Sub(supermod.bodyType30):
    def __init__(self, message=None, status_code=None, detail_code=None):
        super(bodyType30Sub, self).__init__(message, status_code, detail_code, )
supermod.bodyType30.subclass = bodyType30Sub
# end class bodyType30Sub


class responseTypeSub(supermod.responseType):
    def __init__(self, header=None):
        super(responseTypeSub, self).__init__(header, )
supermod.responseType.subclass = responseTypeSub
# end class responseTypeSub



def get_root_tag(node):
    tag = supermod.Tag_pattern_.match(node.tag).groups()[-1]
    rootClass = None
    if hasattr(supermod, tag):
        rootClass = getattr(supermod, tag)
    return tag, rootClass


def parse(inFilename):
    doc = parsexml_(inFilename)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'header_type'
        rootClass = supermod.header_type
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    sys.stdout.write('<?xml version="1.0" ?>\n')
    rootObj.export(sys.stdout, 0, name_=rootTag,
        namespacedef_='',
        pretty_print=True)
    doc = None
    return rootObj


def parseString(inString):
    from StringIO import StringIO
    doc = parsexml_(StringIO(inString))
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'header_type'
        rootClass = supermod.header_type
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    sys.stdout.write('<?xml version="1.0" ?>\n')
    rootObj.export(sys.stdout, 0, name_=rootTag,
        namespacedef_='')
    return rootObj


def parseLiteral(inFilename):
    doc = parsexml_(inFilename)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'header_type'
        rootClass = supermod.header_type
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    sys.stdout.write('#from AmieAccount import *\n\n')
    sys.stdout.write('import AmieAccount as model_\n\n')
    sys.stdout.write('rootObj = model_.header_type(\n')
    rootObj.exportLiteral(sys.stdout, 0, name_="header_type")
    sys.stdout.write(')\n')
    return rootObj


USAGE_TEXT = """
Usage: python ???.py <infilename>
"""

def usage():
    print USAGE_TEXT
    sys.exit(1)


def main():
    args = sys.argv[1:]
    if len(args) != 1:
        usage()
    infilename = args[0]
    root = parse(infilename)


if __name__ == '__main__':
    #import pdb; pdb.set_trace()
    main()



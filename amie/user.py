''' Gregor von Laszewski, http://gregor.cyberaide.org '''

import sys
import AmieAccount as account

def header_msg(name):
    print "\n", 60 * '-', "\n   ", name, '\n', 60 * '-'
    return

def test(object, label=object):
    header_msg(label)
    object.export(sys.stdout,0)
    return

'''
mixedcontainer = account.MixedContainer (category, 
                                      content_type, 
                                      name, 
                                      value)

MemberSpec_ = account.MemberSpec_ (name='', 
                                data_type='', 
                                container=0)
'''

address = account.address (off_address = "off_address",
                           str_address = "str_address",
                           str_address2 = "str_address2",
                           city = "city",
                           state = "state",
                           zip = "zip",
                           country = "country")

test(address,'address')


phone_type = account.phone_type (number = "number",
                              extension = "extension",
                              comment = "comment")

test(phone_type)

person_type = account.person_type (last_name = "last_name",
                                first_name = "first_name",
                                middle_name = "middle_name",
                                email = "email",
                                title = "title",
                                organization = "organization",
                                citizenship = "citizenship",
                                country_access = "country_access",
                                address = address,
                                business_phone = phone_type,
                                home_phone = phone_type,
                                fax = "fax",
                                org_code = "org_code",
                                emp_code = "emp_code",
                                dept = "dept",
                                position = "position",
                                person_id = "person_id",
                                uid = 101,
                                global_id = "global_id")

test(person_type)



reason = account.reason (reason_code = 1,
                         description = "description")
test(reason,'reason')

field_of_science_type = account.field_of_science_type (number = "number",
                                                    abbr = "abbr",
                                                    description = "description")


test(field_of_science_type, 'field_of_science_type')


site_person_id = account.site_person_id_type (site = "site",
                                                person_id = "person_id")
test(site_person_id,'site_person_id_type')

site_person_id_list = account.site_person_id_list (site_person_id = [site_person_id])
test(site_person_id_list,'site_person_id_list')


host_info = account.host_info_type (host = "host",
                                      mb_reserved_memory = 10.3,
                                      processors = 3)
test(host_info,'host_info_type')

attribute_type = account.attribute_type (name = "name",
                                      value = "value")
test(attribute_type,'attribute_type')

resource_login = account.resource_login_type (resource = "resource",
                                                login = "login",
                                                uid = 101)
test(resource_login,'resource_login_type')


bodyType = account.bodyType (record_id = "record_id",
                          project_id = "project_id",
                          alloc_type = "alloc_type",
                          su_alloc = 10.3,
                          #pi = "pi",
                          site_person_id_list = site_person_id_list,
                          start_date = "start_date",
                          end_date = "end_date",
                          project_title = "project_title",
                          #pfos = "pfos",
                          #sfos_list = "sfos_list",
                          resource_list = "resource_list",
                          alloc_resource = "alloc_resource",
                          charge_num = "charge_num",
                          grant_num = "grant_num",
                          grant_type = "grant_type",
                          proposal_num = "proposal_num",
                          abstract = "abstract",
                          sector = "sector",
                          qualifications = "qualifications",
                          methodologies = "methodologies",
                          support = "support",
                          other_resources = "other_resources",
                          statement_work = "statement_work",
                          background = "background",
                          justification = "justification",
                          deliverables = "deliverables",
                          milestones = "milestones",
                          progress = "progress",
                          facilities = "facilities",
                          languages = "languages",
                          applications = "applications",
                          diskspace = "diskspace",
                          memory = "memory",
                          processors = "processors",
                          nsf_status_code = "nsf_status_code",
                          comment = "comment",
                          role_list = "role_list")
test(bodyType,'bodyType')

piType = account.piType (personal_info = "personal_info",
                      dn_list = "dn_list",
                      remote_site_id = "remote_site_id",
                      remote_site_login = "remote_site_login",
                      requester_login = "requester_login",
                      req_login_list = "req_login_list")
test(piType,'piType')

dn_listType = account.dn_listType (dn = "dn")
test(dn_listType,'dn_listType')

req_login_listType = account.req_login_listType (req_login = "req_login")
test(req_login_listType,'req_login_listType')

sfos_listType = account.sfos_listType (sfos = "sfos")
test(sfos_listType,'sfos_listType')

resource_listType = account.resource_listType (resource = "resource")
test(resource_listType,'resource_listType')

role_listType = account.role_listType (role = "role")
test(role_listType,'role_listType')

notify_project_createType = account.notify_project_createType (header = "header",
                                                            body = "body")
test(notify_project_createType,'notify_project_createType')

bodyType1 = account.bodyType1 (record_id = "record_id",
                            project_id = "project_id",
                            project_gid = "project_gid",
                            alloc_type = "alloc_type",
                            su_alloc = "su_alloc",
                            pi = "pi",
                            start_date = "start_date",
                            end_date = "end_date",
                            project_title = "project_title",
                            pfos = "pfos",
                            sfos_list = "sfos_list",
                            resource_list = "resource_list",
                            resource_login_list = "resource_login_list",
                            grant_num = "grant_num",
                            grant_type = "grant_type",
                            proposal_num = "proposal_num",
                            abstract = "abstract",
                            sector = "sector",
                            qualifications = "qualifications",
                            methodologies = "methodologies",
                            support = "support",
                            other_resources = "other_resources",
                            statement_work = "statement_work",
                            background = "background",
                            justification = "justification",
                            deliverables = "deliverables",
                            milestones = "milestones",
                            progress = "progress",
                            facilities = "facilities",
                            languages = "languages",
                            applications = "applications",
                            diskspace = "diskspace",
                            memory = "memory",
                            processors = "processors",
                            nsf_status_code = "nsf_status_code",
                            comment = "comment",
                            account_activity_time = "account_activity_time",
                            board_type = "board_type",
                            role_list = "role_list")
test(bodyType1,'bodyType1')

piType1 = account.piType1 (personal_info = "personal_info",
                        dn_list = "dn_list",
                        notifier_login = "notifier_login",
                        remote_site_login = "remote_site_login",
                        req_login_list = "req_login_list")
test(piType1,'piType1')

dn_listType1 = account.dn_listType1 (dn = "dn")
test(dn_listType1,'dn_listType1')

req_login_listType1 = account.req_login_listType1 (req_login = "req_login")
test(req_login_listType1,'req_login_listType1')

sfos_listType1 = account.sfos_listType1 (sfos = "sfos")
test(sfos_listType1,'sfos_listType1')

resource_listType1 = account.resource_listType1 (resource = "resource")
test(resource_listType1,'resource_listType1')

resource_login_listType = account.resource_login_listType (resource_login = "resource_login")
test(resource_login_listType,'resource_login_listType')

role_listType1 = account.role_listType1 (role = "role")
test(role_listType1,'role_listType1')

data_project_createType = account.data_project_createType (header = "header",
                                                        body = "body")
test(data_project_createType,'data_project_createType')

bodyType2 = account.bodyType2 (dn_list = "dn_list",
                            project_id = "project_id",
                            person_id = "person_id",
                            global_id = "global_id",
                            comment = "comment")
test(bodyType2,'bodyType2')

dn_listType2 = account.dn_listType2 (dn = "dn")
test(dn_listType2,'dn_listType2')

request_account_createType = account.request_account_createType (header = "header",
                                                              body = "body")
test(request_account_createType,'request_account_createType')

bodyType3 = account.bodyType3 (project_id = "project_id",
                            grant_num = "grant_num",
                            alloc_resource = "alloc_resource",
                            resource_list = "resource_list",
                            user = "user",
                            site_person_id_list = "site_person_id_list",
                            nsf_status_code = "nsf_status_code",
                            comment = "comment",
                            role_list = "role_list")
test(bodyType3,'bodyType3')

resource_listType2 = account.resource_listType2 (resource = "resource")
test(resource_listType2,'resource_listType2')

userType = account.userType (personal_info = "personal_info",
                          dn_list = "dn_list",
                          password_access_enable = "password_access_enable",
                          remote_site_id = "remote_site_id",
                          remote_site_login = "remote_site_login",
                          requester_login = "requester_login",
                          req_login_list = "req_login_list",
                          role = "role")
test(userType,'userType')

dn_listType3 = account.dn_listType3 (dn = "dn")
test(dn_listType3,'dn_listType3')

req_login_listType2 = account.req_login_listType2 (req_login = "req_login")
test(req_login_listType2,'req_login_listType2')

role_listType2 = account.role_listType2 (role = "role")
test(role_listType2,'role_listType2')

notify_account_createType = account.notify_account_createType (header = "header",
                                                            body = "body")
test(notify_account_createType,'notify_account_createType')

bodyType4 = account.bodyType4 (project_id = "project_id",
                            resource_list = "resource_list",
                            resource_login_list = "resource_login_list",
                            user = "user",
                            nsf_status_code = "nsf_status_code",
                            comment = "comment",
                            start_date = "start_date",
                            account_activity_time = "account_activity_time",
                            role_list = "role_list")
test(bodyType4,'bodyType4')

resource_listType3 = account.resource_listType3 (resource = "resource")
test(resource_listType3,'resource_listType3')

resource_login_listType1 = account.resource_login_listType1 (resource_login = "resource_login")
test(resource_login_listType1,'resource_login_listType1')

userType1 = account.userType1 (personal_info = "personal_info",
                            password_access_enable = "password_access_enable",
                            dn_list = "dn_list",
                            notifier_login = "notifier_login",
                            remote_site_login = "remote_site_login",
                            req_login_list = "req_login_list",
                            role = "role")
test(userType1,'userType1')

dn_listType4 = account.dn_listType4 (dn = "dn")
test(dn_listType4,'dn_listType4')

req_login_listType3 = account.req_login_listType3 (req_login = "req_login")
test(req_login_listType3,'req_login_listType3')

role_listType3 = account.role_listType3 (role = "role")
test(role_listType3,'role_listType3')

data_account_createType = account.data_account_createType (header = "header",
                                                        body = "body")
test(data_account_createType,'data_account_createType')

bodyType5 = account.bodyType5 (dn_list = "dn_list",
                            project_id = "project_id",
                            person_id = "person_id",
                            global_id = "global_id",
                            comment = "comment")
test(bodyType5,'bodyType5')

dn_listType5 = account.dn_listType5 (dn = "dn")
test(dn_listType5,'dn_listType5')

request_project_resourcesType = account.request_project_resourcesType (header = "header",
                                                                    body = "body")
test(request_project_resourcesType,'request_project_resourcesType')

bodyType6 = account.bodyType6 (project_id = "project_id",
                            resource_list = "resource_list",
                            changed_field_option = "changed_field_option",
                            comment = "comment")
test(bodyType6,'bodyType6')

resource_listType4 = account.resource_listType4 (resource = "resource")
test(resource_listType4,'resource_listType4')

changed_field_optionType = account.changed_field_optionType (su_alloc_info = "su_alloc_info",
                                                          end_date = "end_date")
test(changed_field_optionType,'changed_field_optionType')

su_alloc_infoType = account.su_alloc_infoType (su_alloc = "su_alloc",
                                            alloc_change = "alloc_change",
                                            effective_date = "effective_date")
test(su_alloc_infoType,'su_alloc_infoType')

notify_project_resourcesType = account.notify_project_resourcesType (header = "header",
                                                                  body = "body")
test(notify_project_resourcesType,'notify_project_resourcesType')

bodyType7 = account.bodyType7 (project_id = "project_id",
                            resource_list = "resource_list",
                            changed_field_option = "changed_field_option",
                            comment = "comment")
test(bodyType7,'bodyType7')

resource_listType5 = account.resource_listType5 (resource = "resource")
test(resource_listType5,'resource_listType5')

changed_field_optionType1 = account.changed_field_optionType1 (su_alloc_info = "su_alloc_info",
                                                            end_date = "end_date")
test(changed_field_optionType1,'changed_field_optionType1')

su_alloc_infoType1 = account.su_alloc_infoType1 (su_alloc = "su_alloc",
                                              alloc_change = "alloc_change",
                                              effective_date = "effective_date")
test(su_alloc_infoType1,'su_alloc_infoType1')

request_project_modifyType = account.request_project_modifyType (header = "header",
                                                              body = "body")
test(request_project_modifyType,'request_project_modifyType')

bodyType8 = account.bodyType8 (action_type = "action_type",
                            project_id = "project_id",
                            resource_list = "resource_list",
                            project_title = "project_title",
                            pfos = "pfos",
                            sfos_list = "sfos_list",
                            abstract = "abstract",
                            sector = "sector",
                            qualifications = "qualifications",
                            methodologies = "methodologies",
                            support = "support",
                            other_resources = "other_resources",
                            statement_work = "statement_work",
                            background = "background",
                            justification = "justification",
                            deliverables = "deliverables",
                            milestones = "milestones",
                            progress = "progress",
                            facilities = "facilities",
                            languages = "languages",
                            applications = "applications",
                            diskspace = "diskspace",
                            memory = "memory",
                            processors = "processors",
                            comment = "comment",
                            pi_person_id = "pi_person_id")
test(bodyType8,'bodyType8')

resource_listType6 = account.resource_listType6 (resource = "resource")
test(resource_listType6,'resource_listType6')

sfos_listType2 = account.sfos_listType2 (sfos = "sfos")
test(sfos_listType2,'sfos_listType2')

notify_project_modifyType = account.notify_project_modifyType (header = "header",
                                                            body = "body")
test(notify_project_modifyType,'notify_project_modifyType')

bodyType9 = account.bodyType9 (action_type = "action_type",
                            project_id = "project_id",
                            resource_list = "resource_list",
                            project_title = "project_title",
                            pfos = "pfos",
                            sfos_list = "sfos_list",
                            abstract = "abstract",
                            sector = "sector",
                            qualifications = "qualifications",
                            methodologies = "methodologies",
                            support = "support",
                            other_resources = "other_resources",
                            statement_work = "statement_work",
                            background = "background",
                            justification = "justification",
                            deliverables = "deliverables",
                            milestones = "milestones",
                            progress = "progress",
                            facilities = "facilities",
                            languages = "languages",
                            applications = "applications",
                            diskspace = "diskspace",
                            memory = "memory",
                            processors = "processors",
                            comment = "comment",
                            pi_person_id = "pi_person_id")
test(bodyType9,'bodyType9')

resource_listType7 = account.resource_listType7 (resource = "resource")
test(resource_listType7,'resource_listType7')

sfos_listType3 = account.sfos_listType3 (sfos = "sfos")
test(sfos_listType3,'sfos_listType3')

request_user_modifyType = account.request_user_modifyType (header = "header",
                                                        body = "body")
test(request_user_modifyType,'request_user_modifyType')

bodyType10 = account.bodyType10 (action_type = "action_type",
                              person_id = "person_id",
                              dn_list = "dn_list",
                              new_dn = "new_dn",
                              valid_cert=False, 
                              first_name = "first_name",
                              middle_name = "middle_name",
                              last_name = "last_name",
                              email = "email",
                              fax = "fax",
                              title = "title",
                              organization = "organization",
                              citizenship = "citizenship",
                              country_access = "country_access",
                              org_code = "org_code",
                              emp_code = "emp_code",
                              dept = "dept",
                              address = "address",
                              home_phone = "home_phone",
                              business_phone = "business_phone",
                              remote_site_login = "remote_site_login",
                              requester_login = "requester_login",
                              req_login_list = "req_login_list",
                              comment = "comment",
                              position = "position",
                              nsf_status_code = "nsf_status_code")
test(bodyType10,'bodyType10')

dn_listType6 = account.dn_listType6 (dn = "dn")
test(dn_listType6,'dn_listType6')

req_login_listType4 = account.req_login_listType4 (req_login = "req_login")
test(req_login_listType4,'req_login_listType4')

notify_user_modifyType = account.notify_user_modifyType (header = "header",
                                                      body = "body")
test(notify_user_modifyType,'notify_user_modifyType')

bodyType11 = account.bodyType11 (action_type = "action_type",
                              person_id = "person_id",
                              dn_list = "dn_list",
                              new_dn = "new_dn",
                              valid_cert=False, 
                              first_name = "first_name",
                              middle_name = "middle_name",
                              last_name = "last_name",
                              email = "email",
                              fax = "fax",
                              title = "title",
                              organization = "organization",
                              citizenship = "citizenship",
                              country_access = "country_access",
                              org_code = "org_code",
                              emp_code = "emp_code",
                              dept = "dept",
                              address = "address",
                              home_phone = "home_phone",
                              business_phone = "business_phone",
                              notifier_login = "notifier_login",
                              remote_site_login = "remote_site_login",
                              req_login_list = "req_login_list",
                              comment = "comment",
                              position = "position")
test(bodyType11,'bodyType11')

dn_listType7 = account.dn_listType7 (dn = "dn")
test(dn_listType7,'dn_listType7')

req_login_listType5 = account.req_login_listType5 (req_login = "req_login")
test(req_login_listType5,'req_login_listType5')

request_project_inactivateType = account.request_project_inactivateType (header = "header",
                                                                      body = "body")
test(request_project_inactivateType,'request_project_inactivateType')

bodyType12 = account.bodyType12 (project_id = "project_id",
                              resource_list = "resource_list",
                              comment = "comment",
                              start_date = "start_date",
                              end_date = "end_date",
                              grant_num = "grant_num",
                              alloc_resource = "alloc_resource",
                              su_alloc = "su_alloc",
                              su_remain = "su_remain")
test(bodyType12,'bodyType12')

resource_listType8 = account.resource_listType8 (resource = "resource")
test(resource_listType8,'resource_listType8')

notify_project_inactivateType = account.notify_project_inactivateType (header = "header",
                                                                    body = "body")
test(notify_project_inactivateType,'notify_project_inactivateType')

bodyType13 = account.bodyType13 (project_id = "project_id",
                              resource_list = "resource_list",
                              comment = "comment",
                              account_activity_time = "account_activity_time")
test(bodyType13,'bodyType13')

resource_listType9 = account.resource_listType9 (resource = "resource")
test(resource_listType9,'resource_listType9')

request_project_reactivateType = account.request_project_reactivateType (header = "header",
                                                                      body = "body")
test(request_project_reactivateType,'request_project_reactivateType')

bodyType14 = account.bodyType14 (project_id = "project_id",
                              resource_list = "resource_list",
                              person_id = "person_id",
                              comment = "comment",
                              start_date = "start_date",
                              end_date = "end_date",
                              grant_num = "grant_num",
                              alloc_resource = "alloc_resource",
                              su_alloc = "su_alloc",
                              su_remain = "su_remain")
test(bodyType14,'bodyType14')

resource_listType10 = account.resource_listType10 (resource = "resource")
test(resource_listType10,'resource_listType10')

notify_project_reactivateType = account.notify_project_reactivateType (header = "header",
                                                                    body = "body")
test(notify_project_reactivateType,'notify_project_reactivateType')

bodyType15 = account.bodyType15 (project_id = "project_id",
                              resource_list = "resource_list",
                              comment = "comment",
                              account_activity_time = "account_activity_time")
test(bodyType15,'bodyType15')

resource_listType11 = account.resource_listType11 (resource = "resource")
test(resource_listType11,'resource_listType11')

request_account_inactivateType = account.request_account_inactivateType (header = "header",
                                                                      body = "body")
test(request_account_inactivateType,'request_account_inactivateType')

bodyType16 = account.bodyType16 (project_id = "project_id",
                              person_id = "person_id",
                              alloc_resource = "alloc_resource",
                              resource_list = "resource_list",
                              comment = "comment",
                              account_activity_time = "account_activity_time")
test(bodyType16,'bodyType16')

resource_listType12 = account.resource_listType12 (resource = "resource")
test(resource_listType12,'resource_listType12')

notify_account_inactivateType = account.notify_account_inactivateType (header = "header",
                                                                    body = "body")
test(notify_account_inactivateType,'notify_account_inactivateType')

bodyType17 = account.bodyType17 (project_id = "project_id",
                              person_id = "person_id",
                              resource_list = "resource_list",
                              comment = "comment",
                              account_activity_time = "account_activity_time")
test(bodyType17,'bodyType17')

resource_listType13 = account.resource_listType13 (resource = "resource")
test(resource_listType13,'resource_listType13')

request_account_reactivateType = account.request_account_reactivateType (header = "header",
                                                                      body = "body")
test(request_account_reactivateType,'request_account_reactivateType')

bodyType18 = account.bodyType18 (project_id = "project_id",
                              person_id = "person_id",
                              alloc_resource = "alloc_resource",
                              resource_list = "resource_list",
                              comment = "comment",
                              account_activity_time = "account_activity_time")
test(bodyType18,'bodyType18')

resource_listType14 = account.resource_listType14 (resource = "resource")
test(resource_listType14,'resource_listType14')

notify_account_reactivateType = account.notify_account_reactivateType (header = "header",
                                                                    body = "body")
test(notify_account_reactivateType,'notify_account_reactivateType')

bodyType19 = account.bodyType19 (project_id = "project_id",
                              person_id = "person_id",
                              resource_list = "resource_list",
                              comment = "comment",
                              account_activity_time = "account_activity_time")
test(bodyType19,'bodyType19')

resource_listType15 = account.resource_listType15 (resource = "resource")
test(resource_listType15,'resource_listType15')

request_user_suspendType = account.request_user_suspendType (header = "header",
                                                          body = "body")
test(request_user_suspendType,'request_user_suspendType')

bodyType20 = account.bodyType20 (project_id = "project_id",
                              dn_list = "dn_list",
                              reason = "reason",
                              comment = "comment",
                              person_id = "person_id")
test(bodyType20,'bodyType20')

dn_listType8 = account.dn_listType8 (dn = "dn")
test(dn_listType8,'dn_listType8')

notify_user_suspendType = account.notify_user_suspendType (header = "header",
                                                        body = "body")
test(notify_user_suspendType,'notify_user_suspendType')

bodyType21 = account.bodyType21 (project_id = "project_id",
                              dn_list = "dn_list",
                              reason = "reason",
                              comment = "comment",
                              person_id = "person_id")
test(bodyType21,'bodyType21')

dn_listType9 = account.dn_listType9 (dn = "dn")
test(dn_listType9,'dn_listType9')

request_user_reactivateType = account.request_user_reactivateType (header = "header",
                                                                body = "body")
test(request_user_reactivateType,'request_user_reactivateType')

bodyType22 = account.bodyType22 (project_id = "project_id",
                              dn_list = "dn_list",
                              reason = "reason",
                              comment = "comment",
                              person_id = "person_id")
test(bodyType22,'bodyType22')

dn_listType10 = account.dn_listType10 (dn = "dn")
test(dn_listType10,'dn_listType10')

notify_user_reactivateType = account.notify_user_reactivateType (header = "header",
                                                              body = "body")
test(notify_user_reactivateType,'notify_user_reactivateType')

bodyType23 = account.bodyType23 (project_id = "project_id",
                              dn_list = "dn_list",
                              reason = "reason",
                              comment = "comment",
                              person_id = "person_id")
test(bodyType23,'bodyType23')

dn_listType11 = account.dn_listType11 (dn = "dn")
test(dn_listType11,'dn_listType11')

notify_project_usageType = account.notify_project_usageType (header = "header",
                                                          body = "body")
test(notify_project_usageType,'notify_project_usageType')

bodyType24 = account.bodyType24 (usage_type = "usage_type",
                              project_id = "project_id",
                              machine_name = "machine_name",
                              record_identity = "record_identity",
                              start_time = "start_time",
                              end_time = "end_time",
                              job_identity = "job_identity",
                              user_login = "user_login",
                              job_name = "job_name",
                              charge = "charge",
                              wall_duration = "wall_duration",
                              comment = "comment",
                              cpu_duration = "cpu_duration",
                              node_count = "node_count",
                              processors = "processors",
                              submit_host = "submit_host",
                              submit_time = "submit_time",
                              queue = "queue",
                              exec_host_list = "exec_host_list",
                              attribute_list = "attribute_list",
                              bytes_stored = "bytes_stored",
                              bytes_read = "bytes_read",
                              bytes_written = "bytes_written",
                              number_of_files = "number_of_files",
                              files_read = "files_read",
                              files_written = "files_written",
                              user_copies = "user_copies",
                              system_copies = "system_copies",
                              collection_time = "collection_time",
                              collection_interval = "collection_interval",
                              media_type = "media_type",
                              storage_software = "storage_software")
test(bodyType24,'bodyType24')

record_identityType = account.record_identityType (record_id = "record_id",
                                                create_time = "create_time")
test(record_identityType,'record_identityType')

job_identityType = account.job_identityType (local_job_id = "local_job_id",
                                          global_job_id = "global_job_id")
test(job_identityType,'job_identityType')

cpu_durationType = account.cpu_durationType (user = "user",
                                          system = "system")
test(cpu_durationType,'cpu_durationType')

exec_host_listType = account.exec_host_listType (host_info = "host_info")
test(exec_host_listType,'exec_host_listType')

attribute_listType = account.attribute_listType (attribute = "attribute")
test(attribute_listType,'attribute_listType')

request_user_createType = account.request_user_createType (header = "header",
                                                        body = "body")
test(request_user_createType,'request_user_createType')

bodyType25 = account.bodyType25 (nsf_status_code = "nsf_status_code",
                              site_person_id_list = "site_person_id_list",
                              user = "user")
test(bodyType25,'bodyType25')

userType2 = account.userType2 (personal_info = "personal_info",
                            dn_list = "dn_list")
test(userType2,'userType2')

dn_listType12 = account.dn_listType12 (dn = "dn")
test(dn_listType12,'dn_listType12')

notify_user_createType = account.notify_user_createType (header = "header",
                                                      body = "body")
test(notify_user_createType,'notify_user_createType')

bodyType26 = account.bodyType26 (nsf_status_code = "nsf_status_code",
                              site_person_id_list = "site_person_id_list",
                              user = "user")
test(bodyType26,'bodyType26')

userType3 = account.userType3 (personal_info = "personal_info",
                            dn_list = "dn_list")
test(userType3,'userType3')

dn_listType13 = account.dn_listType13 (dn = "dn")
test(dn_listType13,'dn_listType13')

notify_person_idsType = account.notify_person_idsType (header = "header",
                                                    body = "body")
test(notify_person_idsType,'notify_person_idsType')

bodyType27 = account.bodyType27 (person_id = "person_id",
                              primary_person_id = "primary_person_id",
                              person_id_list = "person_id_list",
                              resource_login_list = "resource_login_list",
                              remove_resource_list = "remove_resource_list")
test(bodyType27,'bodyType27')

person_id_listType = account.person_id_listType (person_id = "person_id")
test(person_id_listType,'person_id_listType')

resource_login_listType2 = account.resource_login_listType2 (resource_login = "resource_login")
test(resource_login_listType2,'resource_login_listType2')

remove_resource_listType = account.remove_resource_listType (resource = "resource")
test(remove_resource_listType,'remove_resource_listType')

request_person_mergeType = account.request_person_mergeType (header = "header",
                                                          body = "body")
test(request_person_mergeType,'request_person_mergeType')

bodyType28 = account.bodyType28 (keep_global_id = "keep_global_id",
                              keep_person_id = "keep_person_id",
                              keep_portal_login = "keep_portal_login",
                              delete_global_id = "delete_global_id",
                              delete_person_id = "delete_person_id",
                              delete_portal_login = "delete_portal_login")
test(bodyType28,'bodyType28')

notify_person_duplicateType = account.notify_person_duplicateType (header = "header",
                                                                body = "body")
test(notify_person_duplicateType,'notify_person_duplicateType')

bodyType29 = account.bodyType29 (person_id1 = "person_id1",
                              person_id2 = "person_id2",
                              global_id1 = "global_id1",
                              global_id2 = "global_id2")
test(bodyType29,'bodyType29')

inform_transaction_completeType = account.inform_transaction_completeType (header = "header",
                                                                        body = "body")
test(inform_transaction_completeType,'inform_transaction_completeType')

bodyType30 = account.bodyType30 (message = "message",
                              status_code = "status_code",
                              detail_code = "detail_code")
test(bodyType30,'bodyType30')

responseType = account.responseType (header = "header")
test(responseType,'responseType')


amie = account.amie (version = "version",
                  request_project_create = "request_project_create",
                  notify_project_create = "notify_project_create",
                  data_project_create = "data_project_create",
                  request_account_create = "request_account_create",
                  notify_account_create = "notify_account_create",
                  data_account_create = "data_account_create",
                  request_project_resources = "request_project_resources",
                  notify_project_resources = "notify_project_resources",
                  request_project_modify = "request_project_modify",
                  notify_project_modify = "notify_project_modify",
                  request_user_modify = "request_user_modify",
                  notify_user_modify = "notify_user_modify",
                  request_project_inactivate = "request_project_inactivate",
                  notify_project_inactivate = "notify_project_inactivate",
                  request_project_reactivate = "request_project_reactivate",
                  notify_project_reactivate = "notify_project_reactivate",
                  request_account_inactivate = "request_account_inactivate",
                  notify_account_inactivate = "notify_account_inactivate",
                  request_account_reactivate = "request_account_reactivate",
                  notify_account_reactivate = "notify_account_reactivate",
                  request_user_suspend = "request_user_suspend",
                  notify_user_suspend = "notify_user_suspend",
                  request_user_reactivate = "request_user_reactivate",
                  notify_user_reactivate = "notify_user_reactivate",
                  notify_project_usage = "notify_project_usage",
                  request_user_create = "request_user_create",
                  notify_user_create = "notify_user_create",
                  notify_person_ids = "notify_person_ids",
                  request_person_merge = "request_person_merge",
                  notify_person_duplicate = "notify_person_duplicate",
                  inform_transaction_complete = "inform_transaction_complete",
                  response = "response")
test(amie,'amie')

expected_reply_list =  account.expected_reply_list  (expected_reply = "expected_reply")
test(expected_reply_list,'expected_reply_list')

expected_reply_type = account.expected_reply_type (type_ = "type_",
                                                timeout = "timeout")
test(expected_reply_type,'expected_reply_type')


header = account.header_type (from_site_name = "from_site_name",
                              to_site_name = "to_site_name",
                              originating_site_name = "originating_site_name",
                              transaction_id = 101,
                              packet_id = 102,
                              expected_reply_list = expected_reply_list,
                              date = "date")
test(header,'header')

test(header,'header')



response_header_type =  account.response_header_type (from_site_name = "from_site_name",
                                                   to_site_name = "to_site_name",
                                                   originating_site_name = "originating_site_name",
                                                   transaction_id = "transaction_id",
                                                   packet_id = "packet_id",
                                                   date = "date",
                                                   status_code = "status_code",
                                                   detail_code = "detail_code",
                                                   message = "message")
test(response_header_type,'response_header_type')

request_project_createType = account.request_project_createType (header = "header",
                                                              body = "body")
test(request_project_createType,'request_project_createType')





print
print 'REST IS STILL BROKEN'
print
#test(mixedcontainer,'mixedcontainer')

test(amie,'amie')


test(response_header_type,'response_header_type')

test(expected_reply_list,'expected_reply_list')

test(expected_reply_type,'expected_reply_type')

test(reason,'reason')

test(field_of_science_type,'field_of_science_type')

test(person_type,'person_type')

test(phone_type,'phone_type')

test(site_person_id_list,'site_person_id_list')

test(site_person_id_type,'site_person_id_type')

test(host_info_type,'host_info_type')

test(attribute_type,'attribute_type')

test(resource_login_type,'resource_login_type')

test(request_project_createType,'request_project_createType')

test(bodyType,'bodyType')

test(piType,'piType')

test(dn_listType,'dn_listType')

test(req_login_listType,'req_login_listType')

test(sfos_listType,'sfos_listType')

test(resource_listType,'resource_listType')

test(role_listType,'role_listType')

test(notify_project_createType,'notify_project_createType')

test(bodyType1,'bodyType1')

test(piType1,'piType1')

test(dn_listType1,'dn_listType1')

test(req_login_listType1,'req_login_listType1')

test(sfos_listType1,'sfos_listType1')

test(resource_listType1,'resource_listType1')

test(resource_login_listType,'resource_login_listType')

test(role_listType1,'role_listType1')

test(data_project_createType,'data_project_createType')

test(bodyType2,'bodyType2')

test(dn_listType2,'dn_listType2')

test(request_account_createType,'request_account_createType')

test(bodyType3,'bodyType3')

test(resource_listType2,'resource_listType2')

test(userType,'userType')

test(dn_listType3,'dn_listType3')

test(req_login_listType2,'req_login_listType2')

test(role_listType2,'role_listType2')

test(notify_account_createType,'notify_account_createType')

test(bodyType4,'bodyType4')

test(resource_listType3,'resource_listType3')

test(resource_login_listType1,'resource_login_listType1')

test(userType1,'userType1')

test(dn_listType4,'dn_listType4')

test(req_login_listType3,'req_login_listType3')

test(role_listType3,'role_listType3')

test(data_account_createType,'data_account_createType')

test(bodyType5,'bodyType5')

test(dn_listType5,'dn_listType5')

test(request_project_resourcesType,'request_project_resourcesType')

test(bodyType6,'bodyType6')

test(resource_listType4,'resource_listType4')

test(changed_field_optionType,'changed_field_optionType')

test(su_alloc_infoType,'su_alloc_infoType')

test(notify_project_resourcesType,'notify_project_resourcesType')

test(bodyType7,'bodyType7')

test(resource_listType5,'resource_listType5')

test(changed_field_optionType1,'changed_field_optionType1')

test(su_alloc_infoType1,'su_alloc_infoType1')

test(request_project_modifyType,'request_project_modifyType')

test(bodyType8,'bodyType8')

test(resource_listType6,'resource_listType6')

test(sfos_listType2,'sfos_listType2')

test(notify_project_modifyType,'notify_project_modifyType')

test(bodyType9,'bodyType9')

test(resource_listType7,'resource_listType7')

test(sfos_listType3,'sfos_listType3')

test(request_user_modifyType,'request_user_modifyType')

test(bodyType10,'bodyType10')

test(dn_listType6,'dn_listType6')

test(req_login_listType4,'req_login_listType4')

test(notify_user_modifyType,'notify_user_modifyType')

test(bodyType11,'bodyType11')

test(dn_listType7,'dn_listType7')

test(req_login_listType5,'req_login_listType5')

test(request_project_inactivateType,'request_project_inactivateType')

test(bodyType12,'bodyType12')

test(resource_listType8,'resource_listType8')

test(notify_project_inactivateType,'notify_project_inactivateType')

test(bodyType13,'bodyType13')

test(resource_listType9,'resource_listType9')

test(request_project_reactivateType,'request_project_reactivateType')

test(bodyType14,'bodyType14')

test(resource_listType10,'resource_listType10')

test(notify_project_reactivateType,'notify_project_reactivateType')

test(bodyType15,'bodyType15')

test(resource_listType11,'resource_listType11')

test(request_account_inactivateType,'request_account_inactivateType')

test(bodyType16,'bodyType16')

test(resource_listType12,'resource_listType12')

test(notify_account_inactivateType,'notify_account_inactivateType')

test(bodyType17,'bodyType17')

test(resource_listType13,'resource_listType13')

test(request_account_reactivateType,'request_account_reactivateType')

test(bodyType18,'bodyType18')

test(resource_listType14,'resource_listType14')

test(notify_account_reactivateType,'notify_account_reactivateType')

test(bodyType19,'bodyType19')

test(resource_listType15,'resource_listType15')

test(request_user_suspendType,'request_user_suspendType')

test(bodyType20,'bodyType20')

test(dn_listType8,'dn_listType8')

test(notify_user_suspendType,'notify_user_suspendType')

test(bodyType21,'bodyType21')

test(dn_listType9,'dn_listType9')

test(request_user_reactivateType,'request_user_reactivateType')

test(bodyType22,'bodyType22')

test(dn_listType10,'dn_listType10')

test(notify_user_reactivateType,'notify_user_reactivateType')

test(bodyType23,'bodyType23')

test(dn_listType11,'dn_listType11')

test(notify_project_usageType,'notify_project_usageType')

test(bodyType24,'bodyType24')

test(record_identityType,'record_identityType')

test(job_identityType,'job_identityType')

test(cpu_durationType,'cpu_durationType')

test(exec_host_listType,'exec_host_listType')

test(attribute_listType,'attribute_listType')

test(request_user_createType,'request_user_createType')

test(bodyType25,'bodyType25')

test(userType2,'userType2')

test(dn_listType12,'dn_listType12')

test(notify_user_createType,'notify_user_createType')

test(bodyType26,'bodyType26')

test(userType3,'userType3')

test(dn_listType13,'dn_listType13')

test(notify_person_idsType,'notify_person_idsType')

test(bodyType27,'bodyType27')

test(person_id_listType,'person_id_listType')

test(resource_login_listType2,'resource_login_listType2')

test(remove_resource_listType,'remove_resource_listType')

test(request_person_mergeType,'request_person_mergeType')

test(bodyType28,'bodyType28')

test(notify_person_duplicateType,'notify_person_duplicateType')

test(bodyType29,'bodyType29')

test(inform_transaction_completeType,'inform_transaction_completeType')

test(bodyType30,'bodyType30')

test(responseType,'responseType')



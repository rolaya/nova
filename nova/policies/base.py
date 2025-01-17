#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from oslo_policy import policy

RULE_ADMIN_OR_OWNER = 'rule:admin_or_owner'
RULE_ADMIN_API = 'rule:admin_api'
RULE_ANY = '@'

# TODO(gmann): # Special string ``system_scope:all`` is added for system
# scoped policies for backwards compatibility where ``nova.conf [oslo_policy]
# enforce_scope = False``.
# Otherwise, this might open up APIs to be more permissive unintentionally if a
# deployment isn't enforcing scope. For example, the 'list all servers'
# policy will be System Scoped Reader with ``role:reader`` and
# scope_type=['system'] Until enforce_scope=True by default, it would
# be possible for users with the ``reader`` role on a project to access the
# 'list all servers' API. Once nova defaults ``nova.conf [oslo_policy]
# enforce_scope=True``, the ``system_scope:all`` bits of these check strings
# can be removed since that will be handled automatically by scope_types in
# oslo.policy's RuleDefault objects.
SYSTEM_ADMIN = 'rule:system_admin_api'
SYSTEM_READER = 'rule:system_reader_api'
PROJECT_MEMBER = 'rule:project_member_api'
PROJECT_READER = 'rule:project_reader_api'
PROJECT_MEMBER_OR_SYSTEM_ADMIN = 'rule:system_admin_or_owner'
PROJECT_READER_OR_SYSTEM_READER = 'rule:system_or_project_reader'

# NOTE(gmann): Below is the mapping of new roles and scope_types
# with legacy roles::

# Legacy Rule        |    New Rules                     |Operation |scope_type|
# -------------------+----------------------------------+----------+-----------
#                    |-> SYSTEM_ADMIN                   |Global    | [system]
# RULE_ADMIN_API     |                                   Write
#                    |-> SYSTEM_READER                  |Global    | [system]
#                    |                                  |Read      |
#
#                    |-> PROJECT_MEMBER_OR_SYSTEM_ADMIN |Project   | [system,
# RULE_ADMIN_OR_OWNER|                                  |Write     |  project]
#                    |-> PROJECT_READER_OR_SYSTEM_READER|Project   | [system,
#                                                       |Read      |  project]

# NOTE(johngarbutt) The base rules here affect so many APIs the list
# of related API operations has not been populated. It would be
# crazy hard to manually maintain such a list.

# NOTE(gmann): Keystone already support implied roles means assignment
# of one role implies the assignment of another. New defaults roles
# `reader`, `member` also has been added in bootstrap. If the bootstrap
# process is re-run, and a `reader`, `member`, or `admin` role already
# exists, a role implication chain will be created: `admin` implies
# `member` implies `reader`.
# For example: If we give access to 'reader' it means the 'admin' and
# 'member' also get access.
rules = [
    policy.RuleDefault(
        "context_is_admin",
        "role:admin",
        "Decides what is required for the 'is_admin:True' check to succeed."),
    policy.RuleDefault(
        "admin_or_owner",
        "is_admin:True or project_id:%(project_id)s",
        "Default rule for most non-Admin APIs."),
    policy.RuleDefault(
        "admin_api",
        "is_admin:True",
        "Default rule for most Admin APIs."),
    policy.RuleDefault(
        "system_admin_api",
        'role:admin and system_scope:all',
        "Default rule for System Admin APIs."),
    policy.RuleDefault(
        "system_reader_api",
        "role:reader and system_scope:all",
        "Default rule for System level read only APIs."),
    policy.RuleDefault(
        "project_member_api",
        "role:member and project_id:%(project_id)s",
        "Default rule for Project level non admin APIs."),
    policy.RuleDefault(
        "project_reader_api",
        "role:reader and project_id:%(project_id)s",
        "Default rule for Project level read only APIs."),
    policy.RuleDefault(
        "system_admin_or_owner",
        "rule:system_admin_api or rule:project_member_api",
        "Default rule for System admin+owner APIs."),
    policy.RuleDefault(
        "system_or_project_reader",
        "rule:system_reader_api or rule:project_reader_api",
        "Default rule for System+Project read only APIs.")
]


def list_rules():
    return rules

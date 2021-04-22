from .users import UserApi, UsersApi, LoginApi, ProtectedApi, RefreshTokenApi
from .institutions import InstitutionsApi, InstitutionApi
from .roles import RolesApi, RoleApi, UserRoleApi, UserRolesApi
from .groups import GroupApi, GroupsApi, UserGroupsApi, UserGroupApi
from .activities import ActivitiesApi, ActivityApi
from .dishes import DishApi, DishesApi, DishMenuApi, DishMenusApi
from .conversations import ConversationsApi, ConversationReplyApi, ConversationRepliesApi


def initialize_routes(api):
    api.add_resource(UsersApi, '/user')
    api.add_resource(UserApi, '/user/<id>')

    api.add_resource(InstitutionsApi, '/institution')
    api.add_resource(InstitutionApi, '/institution/<id>')

    api.add_resource(ActivitiesApi, '/activity')
    api.add_resource(ActivityApi, '/activity/<id>')

    api.add_resource(RolesApi, '/role')
    api.add_resource(RoleApi, '/role/<id>')
    api.add_resource(UserRolesApi, '/userrole/<userid>')
    api.add_resource(UserRoleApi, '/userrole')

    api.add_resource(DishesApi, '/dish')
    api.add_resource(DishApi, '/dish/<id>')
    api.add_resource(DishMenuApi, '/dishmenu/<id>')
    api.add_resource(DishMenusApi, '/dishmenu')

    api.add_resource(GroupsApi, '/group')
    api.add_resource(GroupApi, '/group/<id>')
    api.add_resource(UserGroupsApi, '/usergroup/<userid>')
    api.add_resource(UserGroupApi, '/usergroup')

    api.add_resource(ConversationsApi, '/conversation')
    api.add_resource(ConversationReplyApi, '/conversation_reply')
    api.add_resource(ConversationRepliesApi, '/conversation_reply/<conv_id>')

    api.add_resource(LoginApi, '/login')
    api.add_resource(RefreshTokenApi, '/refresh')
    api.add_resource(ProtectedApi, '/protected')

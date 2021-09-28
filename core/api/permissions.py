from rest_framework import permissions

from rest_framework.permissions import IsAdminUser, IsAuthenticated

# from megamify.core.models import Game, Player, Account 

# class GamePermission(permissions.BasePermission):
     
#     def has_object_permission(self, request, view, obj):

#         account = Account.objects.get(user=request.user)   
#         return obj.account == account


# class GameDataPermission(permissions.BasePermission):
     
#     def has_object_permission(self, request, view, obj):
#         account = Account.objects.get(user=request.user)    
#         return Game.objects.filter(account=account).filter(pk=obj.game_id).exists()
         
# class PlayerPermission(permissions.BasePermission):
     
#     def has_object_permission(self, request, view, obj):
#         account = Account.objects.get(user=request.user)    
#         player = Player.objects.get(pk=obj.player_id) 
#         return Game.objects.filter(account=account).filter(pk=player.game_id).exists()
 

class IsSuperUser(IsAdminUser):
    """
    Check whether the current user is Super user or not
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsUser(IsAuthenticated):
    """
    Check whether the current user exist or not
    """

    def has_permission(self, request, view):
         
        return bool(request.user and request.user.groups.filter(name='User').exists())
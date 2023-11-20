from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.core.exceptions import PermissionDenied  

class ClientOwnPer(PermissionRequiredMixin):
    """ Only Client and Freelancer User has access to Profile View
    """

    def has_permission(self):
        """
        Override this method to customize the way permissions are checked.
        """
        perms = self.get_permission_required()

        if self.request.user.id == self.kwargs.get('pk') and self.request.user.has_perm('accounts.is_client'):
            perms = ('accounts.is_client',)
            return perms
        
        if self.request.user.has_perm('accounts.is_freelancer'):
            perms = ('accounts.is_freelancer',)
            return perms
        return self.request.user.has_perms(perms)

class FreeelancerOwnPer(PermissionRequiredMixin):
    def has_permission(self):
        """
        Override this method to customize the way permissions are checked.
        """
        perms = self.get_permission_required()
        if self.request.user.id == self.kwargs.get('pk') and self.request.user.has_perm('accounts.is_freelancer'):
            perms = ('accounts.is_freelancer',)
            return perms
        
        elif self.request.user.has_perm('accounts.is_client'):
            perms = ('accounts.is_client',)
            return perms
        else:
            raise PermissionDenied('login')
        return self.request.user.has_perms(perms)
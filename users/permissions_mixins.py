from abc import ABC, abstractmethod

from django.contrib.auth.mixins import UserPassesTestMixin


class GroupRequiredMixin(UserPassesTestMixin, ABC):

    @property
    @abstractmethod
    def group_name(self):
        pass

    def test_func(self):
        if self.request.user.groups.filter(name=self.group_name).exists() | self.request.user.is_superuser:
            return True
        return False


class ManagerRequiredMixin(GroupRequiredMixin):

    @property
    def group_name(self):
        return 'manager'
